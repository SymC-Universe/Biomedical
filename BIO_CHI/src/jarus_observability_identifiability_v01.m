% Bio Chi P0-Q Jaruszewicz NF-kB observability/identifiability gate v0.1
% Frozen by BIO_CHI/config/JARUS_OBSERVABILITY_IDENTIFIABILITY_FREEZE_v0_1.json.
% Full six-state local generator retained. No scalar admission or trajectory fitting here.

biochi_this = mfilename('fullpath');
biochi_src = fileparts(biochi_this);
biochi_bio = fileparts(biochi_src);
cases_root = fullfile(biochi_bio,'artifacts','generated','jarus_fig8_cases');
source_json = fullfile(biochi_bio,'artifacts','generated','jarus_observability_source','local_stability_v0_3.json');
outdir = fullfile(biochi_bio,'artifacts','generated','jarus_observability_identifiability_v01');
if exist(outdir,'dir'), rmdir(outdir,'s'); end
mkdir(outdir);

raw = jsondecode(fileread(source_json));
case_ids = {'FIG8A_NOMINAL_DAMPED','FIG8B_LIMIT_CYCLE','FIG8C_RELAXATION_OSCILLATION'};
multipliers = [1.0 0.5 0.25];
C = [0 0 1 0 0 0];
case_results = struct([]);

for ci = 1:numel(case_ids)
    case_id = case_ids{ci};
    src_case = find(strcmp({raw.cases.case_id},case_id),1);
    if isempty(src_case), error('BIO_CHI_OBS_MISSING_CASE:%s',case_id); end
    roots = raw.cases(src_case).roots;
    if numel(roots) ~= 1, error('BIO_CHI_OBS_ROOT_COUNT:%s:%d',case_id,numel(roots)); end
    xstar = roots(1).root(:);
    if numel(xstar) ~= 6 || any(~isfinite(xstar)) || any(xstar <= 0)
        error('BIO_CHI_OBS_BAD_ROOT:%s',case_id);
    end

    case_src = fullfile(cases_root,case_id,'source');
    clear reduced;
    addpath(case_src,'-begin');

    step_records = struct([]);
    all_full_rank = true;
    all_unique_nonreal_pair = true;

    for mi = 1:numel(multipliers)
        mult = multipliers(mi);
        J = biochi_jacobian(xstar,mult);
        if any(~isfinite(J(:))), error('BIO_CHI_OBS_NONFINITE_J:%s',case_id); end

        scale = norm(J,2);
        if ~(isfinite(scale) && scale > 0), error('BIO_CHI_OBS_BAD_SCALE:%s',case_id); end
        Js = J / scale;

        O = zeros(6,6);
        row = C;
        for k = 1:6
            O(k,:) = row;
            row = row * Js;
        end
        s = svd(O);
        if isempty(s) || any(~isfinite(s))
            obs_rank = -1; tol = NaN; full_rank = false; ratio = NaN;
        else
            tol = max(size(O)) * eps(s(1)) * s(1);
            obs_rank = sum(s > tol);
            full_rank = (obs_rank == 6);
            if s(1) > 0, ratio = s(end)/s(1); else, ratio = NaN; end
        end
        all_full_rank = all_full_rank && full_rank;

        [V,D] = eig(J);
        ev = diag(D);
        mode_records = struct([]);
        nonreal_idx = find(imag(ev) ~= 0);
        unique_pair = (numel(nonreal_idx) == 2) && ...
                      (abs(ev(nonreal_idx(1)) - conj(ev(nonreal_idx(2)))) <= ...
                       1e-8 * max([1; abs(ev(nonreal_idx(:)))]));
        all_unique_nonreal_pair = all_unique_nonreal_pair && unique_pair;

        for j = 1:numel(ev)
            v = V(:,j);
            vis = abs(C*v) / norm(v,2);
            mr = struct();
            mr.mode_index = j;
            mr.eigenvalue_real = real(ev(j));
            mr.eigenvalue_imag = imag(ev(j));
            mr.output_visibility = vis;
            mr.is_nonreal = logical(imag(ev(j)) ~= 0);
            mode_records = [mode_records mr]; %#ok<AGROW>
        end

        sr = struct();
        sr.multiplier = mult;
        sr.jacobian_scale_norm2 = scale;
        sr.observability_rank = obs_rank;
        sr.observability_tolerance = tol;
        sr.observability_singular_values = s(:)';
        sr.smallest_to_largest_singular_ratio = ratio;
        sr.full_rank = logical(full_rank);
        sr.unique_nonreal_conjugate_pair = logical(unique_pair);
        sr.modes = mode_records;
        step_records = [step_records sr]; %#ok<AGROW>
    end

    cr = struct();
    cr.case_id = case_id;
    cr.root = xstar(:)';
    cr.primary_observable = 'free nuclear NF-kappaB';
    cr.primary_observable_state_index_one_based = 3;
    cr.all_steps_full_rank = logical(all_full_rank);
    cr.all_steps_unique_nonreal_conjugate_pair = logical(all_unique_nonreal_pair);
    cr.steps = step_records;
    if all_full_rank && all_unique_nonreal_pair
        cr.case_status = 'PASS_LOCAL_OBSERVABILITY';
    elseif ~all_full_rank
        cr.case_status = 'REFUSE_LOCAL_OBSERVABILITY';
    else
        cr.case_status = 'INDETERMINATE_NUMERICAL';
    end
    case_results = [case_results cr]; %#ok<AGROW>
    rmpath(case_src);
end

statuses = {case_results.case_status};
if all(strcmp(statuses,'PASS_LOCAL_OBSERVABILITY'))
    overall = 'PASS_LOCAL_OBSERVABILITY';
elseif any(strcmp(statuses,'REFUSE_LOCAL_OBSERVABILITY'))
    overall = 'REFUSE_LOCAL_OBSERVABILITY';
else
    overall = 'INDETERMINATE_NUMERICAL';
end

result = struct();
result.schema_version = '0.1';
result.project = 'Bio Chi Investigation';
result.gate = 'Jaruszewicz NF-kB six-state local observability/identifiability P0-Q';
result.freeze = 'BIO_CHI/config/JARUS_OBSERVABILITY_IDENTIFIABILITY_FREEZE_v0_1.json';
result.status = overall;
result.root_solver_rerun = false;
result.jacobian_recomputed_from_pinned_native_equations = true;
result.all_six_modes_preserved = true;
result.primary_observable = 'free nuclear NF-kappaB';
result.observable_selected_pre_result = true;
result.mode_selected_by_result = false;
result.chi_bio_admitted = false;
result.Chi_bio_admitted = false;
result.Bio_Chi_constructed = false;
result.cases = case_results;
result.interpretation_limit = ['P0-Q local linear observability qualification only. Full-rank observability through the publication-native output does not by itself establish biological scalar adequacy, ' ...
  'prospective confirmation, a chi=1 boundary, or whole-system Bio Chi.'];

fid = fopen(fullfile(outdir,'observability_identifiability_v0_1.json'),'w');
fwrite(fid,jsonencode(result,'PrettyPrint',true),'char');
fclose(fid);
disp(result);
disp(['BIO_CHI_JARUS_OBSERVABILITY_GATE_' overall]);

function J = biochi_jacobian(x,multiplier)
    n = numel(x); J = zeros(n,n); base = eps^(1/3);
    for j = 1:n
        h = multiplier*base*max(1,abs(x(j)));
        xp=x; xm=x; xp(j)=xp(j)+h; xm(j)=xm(j)-h;
        fp=reduced(0,xp,1); fm=reduced(0,xm,1);
        J(:,j)=(fp(:)-fm(:))/(2*h);
    end
end
