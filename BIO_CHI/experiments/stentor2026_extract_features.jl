#!/usr/bin/env julia
using JLD2
using Statistics
using SHA

const SOURCE = get(ENV, "STENTOR_COLLATED_PATH", "stentor_upstream/processed_data/collated.jld2")
const OUTDIR = joinpath(@__DIR__, "stentor2026_cross_system_results")
mkpath(OUTDIR)

expected_sha = "b84054675f8a608471da1d9cccd051c1fb9503d35b3c9b5b9f6ebc378e75054f"
expected_size = 13922257

function sha256hex(path)
    open(path, "r") do io
        return bytes2hex(sha256(io))
    end
end

function csv_escape(x)
    s = string(x)
    if occursin(",", s) || occursin("\"", s) || occursin("\n", s)
        return "\"" * replace(s, "\"" => "\"\"") * "\""
    end
    return s
end

try
    isfile(SOURCE) || error("collated source missing: $SOURCE")
    actual_sha = sha256hex(SOURCE)
    actual_size = filesize(SOURCE)
    actual_sha == expected_sha || error("collated SHA-256 mismatch: $actual_sha")
    actual_size == expected_size || error("collated size mismatch: $actual_size")

    loaded = JLD2.load(SOURCE)
    haskey(loaded, "data") || error("JLD2 key 'data' missing")
    data = loaded["data"]

    rows = Vector{Vector{Any}}()
    failures = Vector{Vector{Any}}()
    conds = Vector{Vector{Any}}()

    for isi in (60, 120, 180)
        for iti in (3600, 7200, 10800, 18000)
            key = "hab_ISI$(isi)_ITI$(iti)"
            if !haskey(data, key)
                push!(failures, Any[key, isi, iti, "", "missing_condition_key"])
                continue
            end
            obj = data[key]
            if !haskey(obj, "control_data")
                push!(failures, Any[key, isi, iti, "", "control_data_missing"])
                continue
            end
            mat = Array{Float64}(obj["control_data"])
            nr, nc = size(mat)
            push!(conds, Any[key, isi, iti, nr, nc])
            if nr < 120
                push!(failures, Any[key, isi, iti, "", "fewer_than_120_rows:$nr"])
                continue
            end

            for c in 1:nc
                traj = mat[1:120, c]
                if any(!isfinite, traj)
                    push!(failures, Any[key, isi, iti, c, "nonfinite_trajectory"])
                    continue
                end

                t1_early = mean(traj[1:10])
                t1_late = mean(traj[51:60])
                t2_early = mean(traj[61:70])
                t2_late = mean(traj[111:120])
                t1_auc = mean(traj[1:60])
                t2_auc = mean(traj[61:120])

                h1_depth = t1_early - t1_late
                recovery = t2_early - t1_late
                h2_depth = t2_early - t2_late
                auc_shift = t1_auc - t2_auc

                vals = (h1_depth, recovery, h2_depth, auc_shift)
                if any(!isfinite, vals)
                    push!(failures, Any[key, isi, iti, c, "nonfinite_feature"])
                    continue
                end

                push!(rows, Any[key, isi, iti, c, h1_depth, recovery, h2_depth, auc_shift,
                               t1_early, t1_late, t2_early, t2_late, t1_auc, t2_auc])
            end
        end
    end

    open(joinpath(OUTDIR, "stentor_cell_features.csv"), "w") do io
        println(io, "condition,isi_s,iti_s,cell,H1_depth,Recovery,H2_depth,AUC_shift,T1_early,T1_late,T2_early,T2_late,T1_auc,T2_auc")
        for r in rows
            println(io, join(csv_escape.(r), ","))
        end
    end

    open(joinpath(OUTDIR, "stentor_failure_ledger.csv"), "w") do io
        println(io, "condition,isi_s,iti_s,cell,failure")
        for r in failures
            println(io, join(csv_escape.(r), ","))
        end
    end

    open(joinpath(OUTDIR, "stentor_condition_inventory.csv"), "w") do io
        println(io, "condition,isi_s,iti_s,n_rows,n_cells")
        for r in conds
            println(io, join(csv_escape.(r), ","))
        end
    end

    open(joinpath(OUTDIR, "stentor_source_manifest.txt"), "w") do io
        println(io, "source_repository=tejasramdas/stentor_habituation")
        println(io, "source_commit=8704c114555af3477a1dd7471beedde205fed263")
        println(io, "source_path=processed_data/collated.jld2")
        println(io, "lfs_sha256=$(actual_sha)")
        println(io, "bytes=$(actual_size)")
        println(io, "rows_eligible=$(length(rows))")
        println(io, "failures=$(length(failures))")
        println(io, "conditions_seen=$(length(conds))")
    end

    println("STENTOR_EXTRACTION_OK rows=$(length(rows)) failures=$(length(failures))")
catch e
    open(joinpath(OUTDIR, "STENTOR2026_EXTRACTION_FAILURE.txt"), "w") do io
        println(io, "status=EXECUTION_FAILURE_PRESERVED")
        println(io, "error_type=$(typeof(e))")
        println(io, "error=$(sprint(showerror, e))")
    end
    rethrow()
end
