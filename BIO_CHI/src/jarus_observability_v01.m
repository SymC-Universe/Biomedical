% P0-Q local observability/identifiability gate for the frozen Jaruszewicz-Blonska NF-kB model.
% Scientific rules are frozen in JARUS_OBSERVABILITY_IDENTIFIABILITY_FREEZE_v0_1.json.
% This script does not construct or admit chi_bio.

biochi_this = mfilename('fullpath');
biochi_src = fileparts(biochi_this);
biochi_bio = fileparts(biochi_src);
cases_root = fullfile(biochi_bio,'artifacts','generated','jarus_fig8_cases');
source_json = fullfile(biochi_bio,'artifacts','generated','jarus_observability_source','local_stability_v0_3.json');
outdir = fullfile(biochi_bio,'artifacts','generated','jarus_observability_v01');
if exist(outdir,'dir'), rmdir(outdir,'s'); end
mkdir(outdir);

src = jsondecode(fileread(source_json));
case_ids = {'FIG8A_NOMINAL_DAMPED','FIG8B_LIMIT_CYCLE','FIG8C_RELAXATION_OSCILLATION'};
multipliers = [1.0 0.5 0.25];
C = [0 0 1 0 0 0];
case_results = struct([]);

for ci = 1:numel(case_ids)
    case_id = case_ids{ci};
    case_src = fullfile(cases_root,case_id,'source');
    clear reduced;
    addpath(case_src,'-begin');

    idx = find(strcmp({src.cases.case_id},case_id),1);
    if isempty(idx), error('BIO_CHI_OBSERVABILITY_SOURCE_CASE_MISSING_%s',case_id); end
    roots = src.cases(idx).roots;
    if numel(roots) ~= 1, error('BIO_CHI_OBSERVABILITY_ROOT_COUNT_%s_%d',case_id,numel(roots)); end
    xstar = roots(1).root(:);

    step_records = struct([]);
    all_rank6 = true;
    all_finite = true;

    for mi = 1:numel(multipliers)
        J = biochi_jacobian(xstar,multipliers(mi));
        scale = norm(J,2);
        if ~(isfinite(scale) && scale > 0), scale = 1; end
        Js = J / scale;

        O = zeros(6,6);
        row = C;
        for k = 1:6
            O(k,:) = row;
            row = row * Js;
        end

        s = svd(O);
        tol = max(size(O)) * eps(max(s));
        rnk = sum(s > tol);

        [V,D] = eig(J);
        ev = diag(D);
        vis = zeros(6,1);
        for j = 1:6
            denom = norm(V(:,j),2);
            if denom == 0 || ~isfinite(denom)
                vis(j) = NaN;
            else
                vis(j) = abs(C * V(:,j)) / denom;
            end
        end

        rec = struct();
        rec.multiplier = multipliers(mi);
        rec.generator_norm2 = scale;
        rec.observability_rank = rnk;
        rec.observability_singular_values = s(:)';
        rec.observability_rank_tolerance = tol;
        rec.eigenvalues_real = real(ev(:))';
        rec.eigenvalues_imag = imag(ev(:))';
        rec.mode_output_visibility = vis(:)';
        rec.all_finite = all(isfinite([J(:); O(:); s(:); ev(:); vis(:)]));

        step_records = [step_records rec]; %#ok<AGROW>
        all_rank6 = all_rank6 && (rnk == 6);
        all_finite = all_finite && rec.all_finite;
    end

    cr = struct();
    cr.case_id = case_id;
    cr.primary_observable = 'free nuclear NF-kappaB';
    cr.primary_observable_state_index_one_based = 3;
    cr.steps = step_records;
    cr.full_rank_all_steps = all_rank6;
    cr.all_finite = all_finite;

    if ~all_finite
        cr.adjudication = 'INDETERMINATE_NUMERICAL';
    elseif all_rank6
        cr.adjudication = 'PASS_LOCAL_OBSERVABILITY';
    else
        cr.adjudication = 'REFUSE_LOCAL_OBSERVABILITY';
    end

    case_results = [case_results cr]; %#ok<AGROW>
    rmpath(case_src);
end

overall = 'PASS_LOCAL_OBSERVABILITY';
if any(strcmp({case_results.adjudication},'INDETERMINATE_NUMERICAL'))
    overall = 'INDETERMINATE_NUMERICAL';
elseif any(strcmp({case_results.adjudication},'REFUSE_LOCAL_OBSERVABILITY'))
    overall = 'REFUSE_LOCAL_OBSERVABILITY';
end

result = struct();
result.schema_version = '0.1';
result.project = 'Bio Chi Investigation';
result.gate = 'Jaruszewicz-Blonska local biological observability';
result.freeze = 'BIO_CHI/config/JARUS_OBSERVABILITY_IDENTIFIABILITY_FREEZE_v0_1.json';
result.source_local_stability_artifact_id = 10748186325;
result.primary_observable = 'free nuclear NF-kappaB';
result.complete_six_state_generator_preserved = true;
result.cases = case_results;
result.status = overall;
result.chi_bio_constructed = false;
result.chi_bio_admitted = false;
result.Chi_bio_admitted = false;
result.Bio_Chi_constructed = false;
result.interpretation = 'Local linear observability through the publication-native nuclear NF-kB output only. This gate does not establish scalar adequacy, prospective biological prediction, or a chi=1 boundary.';

fid = fopen(fullfile(outdir,'observability_v0_1.json'),'w');
fwrite(fid,jsonencode(result,'PrettyPrint',true),'char');
fclose(fid);

disp(result);
disp(['BIO_CHI_JARUS_OBSERVABILITY_STATUS ' overall]);

function f = biochi_rhs(x)
    f = reduced(0,x(:),1);
    f = f(:);
end

function J = biochi_jacobian(x,multiplier)
    n = numel(x);
    J = zeros(n,n);
    base = eps^(1/3);
    for j = 1:n
        h = multiplier * base * max(1,abs(x(j)));
        xp=x; xm=x; xp(j)=xp(j)+h; xm(j)=xm(j)-h;
        fp=biochi_rhs(xp); fm=biochi_rhs(xm);
        J(:,j)=(fp(:)-fm(:))/(2*h);
    end
end
