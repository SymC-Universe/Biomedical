% Bio Chi P0-Q six-mode conditioning gate v0.1
% Implements BIO_CHI/config/JARUS_MODAL_CONDITIONING_FREEZE_v0_1.json.

biochi_this = mfilename('fullpath');
biochi_src = fileparts(biochi_this);
biochi_bio = fileparts(biochi_src);
cases_root = fullfile(biochi_bio,'artifacts','generated','jarus_fig8_cases');
source_json = fullfile(biochi_bio,'artifacts','generated','jarus_modal_conditioning_source','local_stability_v0_3.json');
outdir = fullfile(biochi_bio,'artifacts','generated','jarus_modal_conditioning_v01');
if exist(outdir,'dir'), rmdir(outdir,'s'); end
mkdir(outdir);

raw = jsondecode(fileread(source_json));
case_ids = {'FIG8A_NOMINAL_DAMPED','FIG8B_LIMIT_CYCLE','FIG8C_RELAXATION_OSCILLATION'};
multipliers = [1.0 0.5 0.25];
sep_floor = sqrt(eps);
cond_ceiling = 1/sqrt(eps);
case_results = struct([]);
overall_pass = true;
any_indeterminate = false;

for ci = 1:numel(case_ids)
    case_id = case_ids{ci};
    src_case = find(strcmp({raw.cases.case_id},case_id),1);
    if isempty(src_case), error('BIO_CHI_COND_MISSING_CASE:%s',case_id); end
    roots = raw.cases(src_case).roots;
    if numel(roots) ~= 1, error('BIO_CHI_COND_ROOT_COUNT:%s:%d',case_id,numel(roots)); end
    xstar = roots(1).root(:);
    if numel(xstar) ~= 6 || any(~isfinite(xstar)) || any(xstar <= 0)
        error('BIO_CHI_COND_BAD_ROOT:%s',case_id);
    end

    case_src = fullfile(cases_root,case_id,'source');
    clear reduced;
    addpath(case_src,'-begin');

    step_records = struct([]);
    case_pass = true;
    case_indeterminate = false;

    for mi = 1:numel(multipliers)
        mult = multipliers(mi);
        J = biochi_jacobian(xstar,mult);
        [V,D] = eig(J);
        ev = diag(D);

        finite_ok = all(isfinite(J(:))) && all(isfinite(V(:))) && all(isfinite(ev(:)));
        if finite_ok
            condV = cond(V,2);
            recip = 1/condV;
            scale = max(abs(ev));
            if ~(isfinite(scale) && scale > 0)
                min_sep = NaN; norm_sep = NaN;
            else
                min_sep = Inf;
                for a = 1:numel(ev)
                    for b = a+1:numel(ev)
                        min_sep = min(min_sep,abs(ev(a)-ev(b)));
                    end
                end
                norm_sep = min_sep/max(scale,realmin);
            end
            nonreal = ev(imag(ev) ~= 0);
            unique_pair = numel(nonreal) == 2 && ...
                abs(nonreal(1)-conj(nonreal(2))) <= 1e-8*max([1;abs(nonreal(:))]);
            metrics_finite = all(isfinite([condV recip min_sep norm_sep]));
        else
            condV = NaN; recip = NaN; min_sep = NaN; norm_sep = NaN;
            unique_pair = false; metrics_finite = false;
        end

        step_pass = finite_ok && metrics_finite && unique_pair && ...
            norm_sep > sep_floor && condV < cond_ceiling;

        if ~finite_ok || ~metrics_finite
            case_indeterminate = true;
        end
        case_pass = case_pass && step_pass;

        sr = struct();
        sr.multiplier = mult;
        sr.eigenvalues_real = real(ev(:))';
        sr.eigenvalues_imag = imag(ev(:))';
        sr.condition_number_V_2 = condV;
        sr.reciprocal_condition_V_2 = recip;
        sr.minimum_pairwise_complex_separation = min_sep;
        sr.minimum_normalized_eigenvalue_separation = norm_sep;
        sr.unique_nonreal_conjugate_pair = logical(unique_pair);
        sr.separation_floor_sqrt_eps = sep_floor;
        sr.condition_ceiling_inv_sqrt_eps = cond_ceiling;
        sr.step_pass = logical(step_pass);
        sr.finite = logical(finite_ok && metrics_finite);
        step_records = [step_records sr]; %#ok<AGROW>
    end

    cr = struct();
    cr.case_id = case_id;
    cr.steps = step_records;
    if case_indeterminate
        cr.case_status = 'INDETERMINATE_NUMERICAL';
    elseif case_pass
        cr.case_status = 'PASS_MODAL_NUMERICAL_CONDITIONING';
    else
        cr.case_status = 'REFUSE_MODAL_NUMERICAL_CONDITIONING';
    end
    overall_pass = overall_pass && case_pass && ~case_indeterminate;
    any_indeterminate = any_indeterminate || case_indeterminate;
    case_results = [case_results cr]; %#ok<AGROW>
    rmpath(case_src);
end

if any_indeterminate
    status = 'INDETERMINATE_NUMERICAL';
elseif overall_pass
    status = 'PASS_MODAL_NUMERICAL_CONDITIONING';
else
    status = 'REFUSE_MODAL_NUMERICAL_CONDITIONING';
end

result = struct();
result.schema_version = '0.1';
result.project = 'Bio Chi Investigation';
result.gate = 'Jaruszewicz complete six-mode numerical conditioning';
result.freeze = 'BIO_CHI/config/JARUS_MODAL_CONDITIONING_FREEZE_v0_1.json';
result.epistemic_mode = 'P0-Q';
result.status = status;
result.representation_scope = 'native physical six-state coordinates';
result.separation_floor_sqrt_eps = sep_floor;
result.condition_ceiling_inv_sqrt_eps = cond_ceiling;
result.cases = case_results;
result.chi_bio_model_specific_status = 'INHERITED_P0Q_SUPPORTED';
result.Chi_bio_admitted = false;
result.Bio_Chi_constructed = false;
result.interpretation = ['Numerical conditioning and degeneracy qualification only. A pass supports numerical identifiability of the complete local modal record in the declared native-coordinate scope; ' ...
    'it does not establish cross-system transport, P1 confirmation, or whole-system Bio Chi.'];

fid = fopen(fullfile(outdir,'jarus_modal_conditioning_v0_1.json'),'w');
fwrite(fid,jsonencode(result,'PrettyPrint',true),'char');
fclose(fid);
disp(result);
disp(['BIO_CHI_MODAL_CONDITIONING_' status]);

function J = biochi_jacobian(x,multiplier)
    n = numel(x); J = zeros(n,n); base = eps^(1/3);
    for j = 1:n
        h = multiplier*base*max(1,abs(x(j)));
        xp=x; xm=x; xp(j)=xp(j)+h; xm(j)=xm(j)-h;
        fp=reduced(0,xp,1); fm=reduced(0,xm,1);
        J(:,j)=(fp(:)-fm(:))/(2*h);
    end
end
