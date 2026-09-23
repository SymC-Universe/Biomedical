% Prospectively frozen necessary-not-sufficient full-state coordinate invariance control.
% No root solving, parameter changes, behavior reclassification, mode selection, or chi construction.

biochi_this = mfilename('fullpath');
biochi_src = fileparts(biochi_this); biochi_bio = fileparts(biochi_src);
cases_root = fullfile(biochi_bio,'artifacts','generated','jarus_fig8_cases');
source_json = fullfile(biochi_bio,'artifacts','generated','jarus_representation_control_source','local_stability_v0_3.json');
outdir = fullfile(biochi_bio,'artifacts','generated','jarus_full_state_representation_control_v01');
if exist(outdir,'dir'), rmdir(outdir,'s'); end; mkdir(outdir);

raw = jsondecode(fileread(source_json));
case_ids = {'FIG8A_NOMINAL_DAMPED','FIG8B_LIMIT_CYCLE','FIG8C_RELAXATION_OSCILLATION'};
multipliers = [1.0 0.5 0.25];
case_results = struct([]);

for ci = 1:numel(case_ids)
  case_id = case_ids{ci};
  src_case = find(strcmp({raw.cases.case_id},case_id),1);
  if isempty(src_case), error('BIO_CHI_REP_CONTROL_MISSING_CASE:%s',case_id); end
  roots = raw.cases(src_case).roots;
  if numel(roots) ~= 1, error('BIO_CHI_REP_CONTROL_ROOT_COUNT:%s:%d',case_id,numel(roots)); end
  xstar = roots(1).root(:);
  if numel(xstar) ~= 6 || any(~isfinite(xstar)) || any(xstar <= 0)
    error('BIO_CHI_REP_CONTROL_BAD_ROOT:%s',case_id);
  end

  case_src = fullfile(cases_root,case_id,'source');
  clear reduced; addpath(case_src,'-begin');
  reps = struct([]);
  for mi = 1:numel(multipliers)
    mult = multipliers(mi);
    Jx = jac_physical(xstar,mult);
    Jz = jac_transformed(ones(6,1),mult,@(z) dyn_normalized(z,xstar));
    Jy = jac_transformed(zeros(6,1),mult,@(y) dyn_log(y,xstar));
    reps = [reps rep_record('physical_x',mult,Jx) rep_record('equilibrium_normalized_z',mult,Jz) rep_record('log_equilibrium_normalized_y',mult,Jy)]; %#ok<AGROW>
  end
  cr = struct(); cr.case_id = case_id; cr.root = xstar(:)'; cr.records = reps;
  case_results = [case_results cr]; %#ok<AGROW>
  rmpath(case_src);
end

result = struct();
result.schema_version = '0.1';
result.audit_type = 'necessary_not_sufficient_full_state_coordinate_invariance_control';
result.freeze = 'BIO_CHI/config/JARUS_FULL_STATE_REPRESENTATION_CONTROL_FREEZE_v0_1.json';
result.root_solver_rerun = false;
result.jacobian_recomputed = true;
result.parameter_change = false;
result.behavior_reclassified = false;
result.mode_selected = false;
result.preferred_complex_pair_selected = false;
result.chi_bio_constructed = false;
result.Chi_bio_admitted = false;
result.Bio_Chi_constructed = false;
result.biological_representation_independence_claimed = false;
result.cases = case_results;
result.interpretation = ['Numerical full-state invertible-coordinate control only. ' ...
  'Local Jacobians under smooth invertible coordinate changes are theoretically similar at an equilibrium, ' ...
  'so agreement is necessary but not sufficient for biological representation independence, observability, identifiability, or scalar adequacy.'];

fid = fopen(fullfile(outdir,'representation_control_raw_v0_1.json'),'w');
fwrite(fid,jsonencode(result,'PrettyPrint',true),'char'); fclose(fid);
disp('BIO_CHI_JARUS_FULL_STATE_REPRESENTATION_CONTROL_RAW_COMPLETE');

function rr = rep_record(rep_id,mult,J)
  ev = eig(J);
  rr = struct(); rr.representation = rep_id; rr.multiplier = mult;
  rr.eigenvalues_real = real(ev(:))'; rr.eigenvalues_imag = imag(ev(:))';
  rr.spectral_abscissa = max(real(ev));
  rr.all_finite = all(isfinite(J(:))) && all(isfinite(ev(:)));
end

function J = jac_physical(x,mult)
  n = numel(x); J = zeros(n,n); base = eps^(1/3);
  for j = 1:n
    h = mult*base*max(1,abs(x(j))); xp=x; xm=x; xp(j)=xp(j)+h; xm(j)=xm(j)-h;
    fp = reduced(0,xp,1); fm = reduced(0,xm,1); J(:,j)=(fp(:)-fm(:))/(2*h);
  end
end

function J = jac_transformed(q,mult,fun)
  n = numel(q); J = zeros(n,n); base = eps^(1/3);
  for j = 1:n
    h = mult*base*max(1,abs(q(j))); qp=q; qm=q; qp(j)=qp(j)+h; qm(j)=qm(j)-h;
    fp = fun(qp); fm = fun(qm); J(:,j)=(fp(:)-fm(:))/(2*h);
  end
end

function dz = dyn_normalized(z,xstar)
  x = xstar(:).*z(:); f = reduced(0,x,1); dz = f(:)./xstar(:);
end

function dy = dyn_log(y,xstar)
  scale = exp(y(:)); x = xstar(:).*scale; f = reduced(0,x,1); dy = f(:)./(xstar(:).*scale);
end
