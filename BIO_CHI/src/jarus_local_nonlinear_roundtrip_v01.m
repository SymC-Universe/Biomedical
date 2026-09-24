% Bio Chi P0-Q local nonlinear round-trip v0.1
% Implements BIO_CHI/config/JARUS_LOCAL_NONLINEAR_ROUNDTRIP_FREEZE_v0_1.json.

biochi_this = mfilename('fullpath');
biochi_src = fileparts(biochi_this);
biochi_bio = fileparts(biochi_src);
cases_root = fullfile(biochi_bio,'artifacts','generated','jarus_fig8_cases');
source_json = fullfile(biochi_bio,'artifacts','generated','jarus_roundtrip_source','local_stability_v0_3.json');
outdir = fullfile(biochi_bio,'artifacts','generated','jarus_local_nonlinear_roundtrip_v01');
if exist(outdir,'dir'), rmdir(outdir,'s'); end
mkdir(outdir);

raw = jsondecode(fileread(source_json));
case_ids = {'FIG8A_NOMINAL_DAMPED','FIG8B_LIMIT_CYCLE','FIG8C_RELAXATION_OSCILLATION'};
fractions = [1e-3 1e-4 1e-5];
C = [0 0 1 0 0 0];
opts = odeset('RelTol',1e-10,'AbsTol',1e-12);

case_results = struct([]);
overall_pair_pass = true;
overall_full_pass = true;
overall_selfcheck_pass = true;

for ci = 1:numel(case_ids)
    case_id = case_ids{ci};
    src_case = find(strcmp({raw.cases.case_id},case_id),1);
    if isempty(src_case), error('BIO_CHI_RT_MISSING_CASE:%s',case_id); end
    roots = raw.cases(src_case).roots;
    if numel(roots) ~= 1, error('BIO_CHI_RT_ROOT_COUNT:%s:%d',case_id,numel(roots)); end
    xstar = roots(1).root(:);
    if numel(xstar) ~= 6 || any(~isfinite(xstar)) || any(xstar <= 0)
        error('BIO_CHI_RT_BAD_ROOT:%s',case_id);
    end

    case_src = fullfile(cases_root,case_id,'source');
    clear reduced;
    addpath(case_src,'-begin');

    J = biochi_jacobian(xstar,1.0);
    [V,D] = eig(J);
    ev = diag(D);
    pos_idx = find(imag(ev) > 0);
    if numel(pos_idx) ~= 1
        error('BIO_CHI_RT_NONUNIQUE_POSITIVE_IMAG_PAIR:%s:%d',case_id,numel(pos_idx));
    end
    pair_idx = pos_idx(1);
    lambda = ev(pair_idx);
    v = V(:,pair_idx);

    cv = C*v;
    if ~(isfinite(abs(cv)) && abs(cv) > 0)
        error('BIO_CHI_RT_ZERO_OUTPUT_PROJECTION:%s',case_id);
    end
    phase = exp(-1i*angle(cv));
    w = v*phase;
    u_pair = real(w);
    pair_norm = norm(u_pair,2);
    if ~(isfinite(pair_norm) && pair_norm > 0)
        error('BIO_CHI_RT_BAD_PAIR_DIRECTION:%s',case_id);
    end
    u_pair = u_pair/pair_norm;

    omega_d = abs(imag(lambda));
    if ~(isfinite(omega_d) && omega_d > 0)
        error('BIO_CHI_RT_BAD_OMEGAD:%s',case_id);
    end
    horizon = 4*pi/omega_d;
    tvec = linspace(0,horizon,401)';

    eq_norm = norm(xstar,2);
    if ~(isfinite(eq_norm) && eq_norm > 0)
        error('BIO_CHI_RT_BAD_EQ_NORM:%s',case_id);
    end

    % Implementation self-check: analytic pair response vs full linear expm.
    eps_check = fractions(2)*eq_norm;
    delta0_pair_check = eps_check*u_pair;
    pair_lin_check = zeros(6,numel(tvec));
    full_lin_check = zeros(6,numel(tvec));
    denom_w = norm(real(w),2);
    for ti = 1:numel(tvec)
        tt = tvec(ti);
        pair_lin_check(:,ti) = eps_check*real(w*exp(lambda*tt))/denom_w;
        full_lin_check(:,ti) = expm(J*tt)*delta0_pair_check;
    end
    selfcheck_rel = norm(full_lin_check-pair_lin_check,'fro') / max(norm(pair_lin_check,'fro'),realmin);
    selfcheck_pass = isfinite(selfcheck_rel) && selfcheck_rel <= 1e-8;

    % Refusal control: a single real pole is not a second-order conjugate factor.
    real_idx = find(imag(ev) == 0);
    if isempty(real_idx)
        error('BIO_CHI_RT_NO_REAL_POLE_CONTROL:%s',case_id);
    end
    [~,rr] = max(real(ev(real_idx)));
    real_control_lambda = ev(real_idx(rr));
    refusal_status = biochi_scalar_constructor(real_control_lambda);
    refusal_pass = strcmp(refusal_status,'REFUSE_SINGLE_REAL_POLE');
    selfcheck_pass = selfcheck_pass && refusal_pass;

    pair_records = struct([]);
    full_records = struct([]);

    for ai = 1:numel(fractions)
        frac = fractions(ai);
        eps_abs = frac*eq_norm;

        % Pair-lane nonlinear trajectory.
        x0_pair = xstar + eps_abs*u_pair;
        if any(x0_pair <= 0), error('BIO_CHI_RT_PAIR_NONPOSITIVE_X0:%s:%g',case_id,frac); end
        [tp,yp] = ode23s(@(t,x) reduced(t,x,1),tvec,x0_pair,opts);
        if numel(tp) ~= numel(tvec) || any(~isfinite(yp(:)))
            error('BIO_CHI_RT_PAIR_BAD_SOLVE:%s:%g',case_id,frac);
        end
        pred_pair = zeros(6,numel(tvec));
        for ti = 1:numel(tvec)
            pred_pair(:,ti) = eps_abs*real(w*exp(lambda*tvec(ti)))/denom_w;
        end
        obs_nonlinear = yp(:,3)-xstar(3);
        obs_pair = pred_pair(3,:)';
        pair_rel_err = norm(obs_nonlinear-obs_pair,2) / max(norm(obs_pair,2),realmin);

        pr = struct();
        pr.fraction_of_equilibrium_norm = frac;
        pr.absolute_amplitude = eps_abs;
        pr.relative_L2_error_nuclear_NFkB = pair_rel_err;
        pr.all_finite = all(isfinite([pair_rel_err; obs_nonlinear; obs_pair]));
        pair_records = [pair_records pr]; %#ok<AGROW>

        % Full-modal lane nonlinear trajectory.
        u_full = ones(6,1)/sqrt(6);
        x0_full = xstar + eps_abs*u_full;
        if any(x0_full <= 0), error('BIO_CHI_RT_FULL_NONPOSITIVE_X0:%s:%g',case_id,frac); end
        [tf,yf] = ode23s(@(t,x) reduced(t,x,1),tvec,x0_full,opts);
        if numel(tf) ~= numel(tvec) || any(~isfinite(yf(:)))
            error('BIO_CHI_RT_FULL_BAD_SOLVE:%s:%g',case_id,frac);
        end
        pred_full = zeros(6,numel(tvec));
        for ti = 1:numel(tvec)
            pred_full(:,ti) = expm(J*tvec(ti))*(eps_abs*u_full);
        end
        nonlinear_full = (yf - xstar')';
        full_rel_err = norm(nonlinear_full-pred_full,'fro') / max(norm(pred_full,'fro'),realmin);

        fr = struct();
        fr.fraction_of_equilibrium_norm = frac;
        fr.absolute_amplitude = eps_abs;
        fr.relative_Frobenius_error_all_states = full_rel_err;
        fr.all_finite = all(isfinite([full_rel_err; nonlinear_full(:); pred_full(:)]));
        full_records = [full_records fr]; %#ok<AGROW>
    end

    pair_primary_pass = pair_records(2).all_finite && pair_records(1).all_finite && ...
        pair_records(2).relative_L2_error_nuclear_NFkB < pair_records(1).relative_L2_error_nuclear_NFkB;
    full_primary_pass = full_records(2).all_finite && full_records(1).all_finite && ...
        full_records(2).relative_Frobenius_error_all_states < full_records(1).relative_Frobenius_error_all_states;

    overall_pair_pass = overall_pair_pass && pair_primary_pass;
    overall_full_pass = overall_full_pass && full_primary_pass;
    overall_selfcheck_pass = overall_selfcheck_pass && selfcheck_pass;

    cr = struct();
    cr.case_id = case_id;
    cr.lambda_real = real(lambda);
    cr.lambda_imag = imag(lambda);
    cr.chi_bio = -real(lambda)/abs(lambda);
    cr.horizon_seconds = horizon;
    cr.horizon_hours = horizon/3600;
    cr.pair_vs_full_linear_relative_error = selfcheck_rel;
    cr.pair_vs_full_linear_selfcheck_pass = logical(selfcheck_rel <= 1e-8);
    cr.real_pole_control_lambda = real(real_control_lambda);
    cr.real_pole_refusal_status = refusal_status;
    cr.real_pole_refusal_pass = logical(refusal_pass);
    cr.pair_lane = pair_records;
    cr.full_modal_lane = full_records;
    cr.pair_primary_pass = logical(pair_primary_pass);
    cr.full_modal_primary_pass = logical(full_primary_pass);
    case_results = [case_results cr]; %#ok<AGROW>
    rmpath(case_src);
end

if ~overall_selfcheck_pass
    status = 'FAIL_IMPLEMENTATION_SELF_CHECK';
elseif ~overall_pair_pass
    status = 'FAIL_PAIR_LOCAL_ROUNDTRIP';
elseif ~overall_full_pass
    status = 'FAIL_FULL_MODAL_LOCAL_ROUNDTRIP';
else
    status = 'PASS_LOCAL_NONLINEAR_ROUNDTRIP';
end

result = struct();
result.schema_version = '0.1';
result.project = 'Bio Chi Investigation';
result.gate = 'Jaruszewicz local nonlinear modal round-trip';
result.freeze = 'BIO_CHI/config/JARUS_LOCAL_NONLINEAR_ROUNDTRIP_FREEZE_v0_1.json';
result.epistemic_mode = 'P0-Q';
result.status = status;
result.cases = case_results;
result.chi_bio_model_specific_status = 'INHERITED_P0Q_SUPPORTED';
result.Chi_bio_admitted = false;
result.Bio_Chi_constructed = false;
result.p1_confirmation_claimed = false;
result.interpretation = ['This gate tests only local convergence of the native nonlinear model to the frozen linear/modal representation. ' ...
    'It does not establish independent biological transport, a chi=1 boundary, or whole-system Bio Chi.'];

fid = fopen(fullfile(outdir,'jarus_local_nonlinear_roundtrip_v0_1.json'),'w');
fwrite(fid,jsonencode(result,'PrettyPrint',true),'char');
fclose(fid);
disp(result);
disp(['BIO_CHI_LOCAL_NONLINEAR_ROUNDTRIP_' status]);

function J = biochi_jacobian(x,multiplier)
    n = numel(x); J = zeros(n,n); base = eps^(1/3);
    for j = 1:n
        h = multiplier*base*max(1,abs(x(j)));
        xp=x; xm=x; xp(j)=xp(j)+h; xm(j)=xm(j)-h;
        fp=reduced(0,xp,1); fm=reduced(0,xm,1);
        J(:,j)=(fp(:)-fm(:))/(2*h);
    end
end

function status = biochi_scalar_constructor(input_lambda)
    if numel(input_lambda) ~= 2
        status = 'REFUSE_SINGLE_REAL_POLE';
        return;
    end
    status = 'PAIR_INPUT_NOT_USED_IN_CONTROL';
end
