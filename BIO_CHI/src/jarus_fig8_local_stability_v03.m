% Final prospectively frozen numerical cross-check for Figure 8 local stability.
% Uses exactly the same 70 frozen seeds and unchanged root/Jacobian criteria.
% No prior root candidate or trajectory state is used as a seed.

biochi_this=mfilename('fullpath'); biochi_src=fileparts(biochi_this); biochi_bio=fileparts(biochi_src);
cases_root=fullfile(biochi_bio,'artifacts','generated','jarus_fig8_cases');
outdir=fullfile(biochi_bio,'artifacts','generated','jarus_fig8_local_stability_v03');
if exist(outdir,'dir'), rmdir(outdir,'s'); end; mkdir(outdir);
case_ids={'FIG8A_NOMINAL_DAMPED','FIG8B_LIMIT_CYCLE','FIG8C_RELAXATION_OSCILLATION'};
expected={'STABLE','UNSTABLE','UNSTABLE'};
fixed_scalars=[1e-4 1e-3 1e-2 1e-1 5e-1 1.0];
rng(20260923,'twister'); lo=log(1e-6); hi=log(10.0);
random_seeds=exp(lo+(hi-lo).*rand(6,64));
fixed_seeds=zeros(6,numel(fixed_scalars));
for k=1:numel(fixed_scalars), fixed_seeds(:,k)=fixed_scalars(k).*ones(6,1); end
all_seeds=[fixed_seeds random_seeds];
lb=zeros(6,1); ub=inf(6,1);
opts=optimoptions('lsqnonlin','Display','off','FunctionTolerance',1e-20, ...
  'StepTolerance',1e-14,'OptimalityTolerance',1e-14,'MaxIterations',5000, ...
  'MaxFunctionEvaluations',100000);
case_results=struct([]);
for ci=1:numel(case_ids)
  case_id=case_ids{ci}; case_src=fullfile(cases_root,case_id,'source'); clear reduced; addpath(case_src,'-begin');
  accepted={}; root_records=struct([]); attempt_records=struct([]);
  fprintf('BIO_CHI_LOCAL_STABILITY_V03_CASE_BEGIN %s\n',case_id);
  for si=1:size(all_seeds,2)
    seed=all_seeds(:,si); err='';
    try
      [x,resnorm,residual,exitflag,output]=lsqnonlin(@(x) biochi_rhs(x),seed,lb,ub,opts);
      x=x(:); residual=residual(:); residual_inf=norm(residual,inf);
      finite_ok=all(isfinite(x))&&all(isfinite(residual));
      accepted_this=finite_ok&&all(x>0)&&residual_inf<=1e-9&&exitflag>0;
    catch ME
      x=nan(6,1); resnorm=Inf; residual=nan(6,1); residual_inf=Inf; exitflag=-999;
      output=struct('iterations',0); accepted_this=false; err=ME.message;
    end
    ar=struct('seed_index',si,'seed',seed(:)','candidate',x(:)','exitflag',exitflag, ...
      'residual_inf',residual_inf,'resnorm',resnorm,'accepted',logical(accepted_this),'error',err);
    if isfield(output,'iterations'), ar.iterations=output.iterations; else, ar.iterations=NaN; end
    attempt_records=[attempt_records ar]; %#ok<AGROW>
    if ~accepted_this, continue; end
    is_new=true;
    for ri=1:numel(accepted)
      ref=accepted{ri}; rel=max(abs(x-ref)./max(1,abs(ref)));
      if rel<=1e-6, is_new=false; break; end
    end
    if ~is_new, continue; end
    accepted{end+1}=x; %#ok<AGROW>
    rr=struct(); rr.root=x(:)'; rr.residual_inf=residual_inf; rr.resnorm=resnorm; rr.source_seed_index=si; rr.jacobian_steps=struct([]);
    multipliers=[1.0 0.5 0.25]; maxre=zeros(1,3);
    for mi=1:3
      J=biochi_jacobian(x,multipliers(mi)); ev=eig(J); js=struct(); js.multiplier=multipliers(mi);
      js.max_real_eigenvalue=max(real(ev)); js.eigenvalues_real=real(ev(:))'; js.eigenvalues_imag=imag(ev(:))';
      rr.jacobian_steps=[rr.jacobian_steps js]; %#ok<AGROW>; maxre(mi)=js.max_real_eigenvalue;
    end
    rr.max_real_eigenvalues=maxre;
    if all(maxre<0), rr.local_stability='STABLE'; elseif all(maxre>0), rr.local_stability='UNSTABLE'; else, rr.local_stability='INDETERMINATE_NUMERICAL_SIGN'; end
    root_records=[root_records rr]; %#ok<AGROW>
  end
  cr=struct(); cr.case_id=case_id; cr.expected_paper_local_stability=expected{ci}; cr.seed_count=size(all_seeds,2);
  cr.accepted_distinct_root_count=numel(root_records); cr.roots=root_records; cr.attempts=attempt_records;
  if numel(root_records)~=1, cr.paper_local_stability_status='INDETERMINATE_ROOT_MULTIPLICITY';
  elseif strcmp(root_records(1).local_stability,expected{ci}), cr.paper_local_stability_status='PASS';
  elseif strcmp(root_records(1).local_stability,'INDETERMINATE_NUMERICAL_SIGN'), cr.paper_local_stability_status='INDETERMINATE_NUMERICAL_SIGN';
  else, cr.paper_local_stability_status='FAIL_NATIVE_LOCAL_STABILITY'; end
  case_results=[case_results cr]; %#ok<AGROW>; rmpath(case_src);
  fprintf('BIO_CHI_LOCAL_STABILITY_V03_CASE_END %s ROOTS=%d STATUS=%s\n',case_id,numel(root_records),cr.paper_local_stability_status);
end
result=struct('schema_version','0.3','audit_type','bounded_residual_TR1_local_stability_crosscheck', ...
 'freeze','BIO_CHI/config/JARUS_FIG8_LOCAL_STABILITY_FREEZE_v0_3.json', ...
 'preserved_v01','BIO_CHI/config/JARUS_LOCAL_STABILITY_V01_RESULT_PIN.json', ...
 'preserved_v02','BIO_CHI/config/JARUS_LOCAL_STABILITY_V02_RESULT_PIN.json', ...
 'cases',case_results,'finite_window_results_preserved',true,'limit_cycle_proved',false, ...
 'chi_bio_constructed',false,'Chi_bio_constructed',false,'Bio_Chi_constructed',false);
fid=fopen(fullfile(outdir,'local_stability_v0_3.json'),'w'); fwrite(fid,jsonencode(result,'PrettyPrint',true),'char'); fclose(fid);
disp(result); disp('BIO_CHI_JARUS_LOCAL_STABILITY_V03_GATE_COMPLETE');

function f=biochi_rhs(x), f=reduced(0,x(:),1); f=f(:); end
function J=biochi_jacobian(x,multiplier)
 n=numel(x); J=zeros(n,n); base=eps^(1/3);
 for j=1:n
  h=multiplier*base*max(1,abs(x(j))); xp=x; xm=x; xp(j)=xp(j)+h; xm(j)=xm(j)-h;
  fp=reduced(0,xp,1); fm=reduced(0,xm,1); J(:,j)=(fp(:)-fm(:))/(2*h);
 end
end
