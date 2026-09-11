param(
    [Parameter(Mandatory=$false)]
    [string]$Root = ".",

    [Parameter(Mandatory=$false)]
    [string]$OutDir = "GRI_CAPACITY_FREEZE_SEARCH"
)

$ErrorActionPreference = "Stop"

$rootPath = (Resolve-Path -LiteralPath $Root).Path
$outPath = Join-Path $rootPath $OutDir
New-Item -ItemType Directory -Force -Path $outPath | Out-Null

$patterns = @(
    "equal-dimensional",
    "equal dimensional",
    "dimensionality-matched",
    "dimension matched",
    "capacity-matched",
    "capacity matched",
    "capacity-control",
    "capacity control",
    "non-Hallmark",
    "non Hallmark",
    "methylation PC",
    "methylation PCA",
    "random probe",
    "Hallmark membership shuffled",
    "post-FINAL",
    "POST_FINAL",
    "FINAL_HOLDOUT"
)

$extensions = @(
    ".py", ".ps1", ".bat", ".cmd", ".json", ".yaml", ".yml", ".toml",
    ".ini", ".cfg", ".txt", ".md", ".csv", ".tsv", ".tex", ".log"
)

$files = Get-ChildItem -LiteralPath $rootPath -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $extensions -contains $_.Extension.ToLowerInvariant() -and
        $_.FullName -notlike "*$OutDir*"
    }

$hits = New-Object System.Collections.Generic.List[object]
foreach ($file in $files) {
    try {
        $matches = Select-String -LiteralPath $file.FullName -Pattern $patterns -SimpleMatch -CaseSensitive:$false -ErrorAction Stop
        foreach ($m in $matches) {
            $hits.Add([pscustomobject]@{
                Path = $file.FullName
                LastWriteTimeUtc = $file.LastWriteTimeUtc.ToString("o")
                Length = $file.Length
                LineNumber = $m.LineNumber
                Pattern = $m.Pattern
                Line = $m.Line.Trim()
            })
        }
    } catch {
        # Preserve search progress; unreadable/non-text files are excluded by extension gate.
    }
}

$hitsCsv = Join-Path $outPath "capacity_freeze_text_hits.csv"
$hits | Sort-Object Path, LineNumber | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $hitsCsv

$candidatePaths = $hits | Select-Object -ExpandProperty Path -Unique
$candidateRows = New-Object System.Collections.Generic.List[object]
foreach ($path in $candidatePaths) {
    try {
        $item = Get-Item -LiteralPath $path
        $sha = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
        $candidateRows.Add([pscustomobject]@{
            Path = $item.FullName
            LastWriteTimeUtc = $item.LastWriteTimeUtc.ToString("o")
            CreationTimeUtc = $item.CreationTimeUtc.ToString("o")
            Length = $item.Length
            SHA256 = $sha
        })
    } catch {
    }
}

$candidatesCsv = Join-Path $outPath "capacity_freeze_candidate_files.csv"
$candidateRows | Sort-Object LastWriteTimeUtc, Path | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $candidatesCsv

$gitResults = New-Object System.Collections.Generic.List[string]
$git = Get-Command git -ErrorAction SilentlyContinue
if ($null -ne $git) {
    try {
        $repoRoot = (& git -C $rootPath rev-parse --show-toplevel 2>$null).Trim()
        if ($repoRoot) {
            $queries = @(
                "equal-dimensional",
                "dimensionality-matched",
                "capacity-matched",
                "capacity-control",
                "non-Hallmark",
                "POST_FINAL"
            )
            foreach ($q in $queries) {
                $gitResults.Add("===== git log -S '$q' =====")
                $lines = & git -C $repoRoot log --all --date=iso-strict --pretty=format:"%H`t%ad`t%s" -S $q -- 2>$null
                if ($lines) {
                    foreach ($line in $lines) { $gitResults.Add($line) }
                } else {
                    $gitResults.Add("NO MATCH")
                }
            }
        }
    } catch {
        $gitResults.Add("Git history search unavailable: $($_.Exception.Message)")
    }
} else {
    $gitResults.Add("Git executable not found; history search skipped.")
}

$gitOut = Join-Path $outPath "capacity_freeze_git_history.txt"
$gitResults | Set-Content -Encoding UTF8 -Path $gitOut

$summary = [ordered]@{
    generated_utc = [DateTime]::UtcNow.ToString("o")
    root = $rootPath
    text_hit_count = @($hits).Count
    unique_candidate_file_count = @($candidateRows).Count
    outputs = [ordered]@{
        text_hits = $hitsCsv
        candidate_files = $candidatesCsv
        git_history = $gitOut
    }
    interpretation = "Candidates are provenance leads only. A historical freeze is verified only if content, timestamp/commit/hash provenance, and pre-result status can be established. Do not treat filename similarity as proof."
}

$summaryPath = Join-Path $outPath "capacity_freeze_search_summary.json"
$summary | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 -Path $summaryPath

Write-Host "Search complete."
Write-Host "Text hits: $(@($hits).Count)"
Write-Host "Unique candidate files: $(@($candidateRows).Count)"
Write-Host "Output directory: $outPath"
Write-Host "Review capacity_freeze_candidate_files.csv and capacity_freeze_text_hits.csv before accepting any candidate as the historical freeze."
