% Bio Chi P0-Q same-system scalar/modal/system joint response test.
% Frozen in JARUS_JOINT_SCALAR_MODAL_SYSTEM_P0Q_FREEZE_v0_1.json.
% No trajectory fitting, post-result mode selection, or threshold tuning is allowed.

biochi_this=mfilename('fullpath');
biochi_src=fileparts(biochi_this);
biochi_bio=fileparts(biochi_src);
source_dir=fullfile(biochi_bio,'artifacts','generated','jarus_matlab_compat','source','S1_Codes','MATLAB files','Reduced2023');
outdir=fullfile(biochi_bio,'artifacts','generated','jarus_joint_scalar_modal_system_p0q_v01');
if exist(outdir,'dir'), rmdir(outdir,'s'); end
mkdir(outdir);
addpath(source_dir,'-begin');
clear reduced;

xstar=[1;0;0;0;0;0];
C=[0 0 1 0 0 0];
k1=0.00195;
B_expected=[-k1;k1;0;0;0;0];

% Frozen centered local Jacobian.
n=6; J=zeros(n,n); base=eps^(1/3);
for j=1:n
    h=base*max(1,abs(xstar(j)));
    xp=xstar; xm=xstar; xp(j)=xp(j)+h; xm(j)=xm(j)-h;
    fp=reduced(0,xp,0); fm=reduced(0,xm,0);
    J(:,j)=(fp(:)-fm(:))/(2*h);
end

% Verify the source input derivative numerically at the exact source equilibrium.
hu=base;
Bp=reduced(0,xstar,hu); Bm=reduced(0,xstar,-hu);
B=(Bp(:)-Bm(:))/(2*hu);
B_error=max(abs(B-B_expected));
if B_error>1e-10
    error('BIO_CHI_JARUS_JOINT_B_MISMATCH %.17g',B_error);
end

% Frozen pair identity from the complete local generator.
[V,D]=eig(J);
ev=diag(D);
pos=find(imag(ev)>1e-10);
neg=find(imag(ev)<-1e-10);
if numel(pos)~=1 || numel(neg)~=1
    error('BIO_CHI_JARUS_JOINT_COMPLEX_PAIR_COUNT_%d_%d',numel(pos),numel(neg));
end
ip=pos(1);
[~,nn]=min(abs(ev(neg)-conj(ev(ip))));
in=neg(nn);
pair=[ip in];
chi_calc=-real(ev(ip))/abs(ev(ip));
chi_pin=0.21311451897468006;
chi_rel=abs(chi_calc-chi_pin)/abs(chi_pin);
if chi_rel>1e-6
    error('BIO_CHI_JARUS_JOINT_CHI_IDENTITY_MISMATCH %.17g',chi_rel);
end

W=inv(V);
Vp=V(:,pair);
Wp=W(pair,:);
Lam=diag(ev(pair));
Bp_pair=Wp*B;
Cp_pair=C*Vp;
eigvec_condition=cond(V);

protocols = {
 'continuous_9h', 9*3600, 0, 1;
 'pulses_5_60', 5*60, 60*60, 3;
 'pulses_5_100', 5*60, 100*60, 3;
 'pulses_5_200', 5*60, 200*60, 3;
 'pulses_22p5_45', 22.5*60, 45*60, 3;
 'pulses_45_90', 45*60, 90*60, 3;
 'on_off_2h', 2*3600, 10*3600, 1
};

t0=0; t1=10*3600; tnf_begin=3600; grid=(t0:60:t1)';
records=struct([]);
all_pair=[]; all_full=[];

for pi=1:size(protocols,1)
    pid=protocols{pi,1};
    dur_on=protocols{pi,2};
    interval=protocols{pi,3};
    npulse=protocols{pi,4};

    pulses=zeros(npulse,2);
    for q=1:npulse
        pb=tnf_begin+(q-1)*interval;
        pe=pb+dur_on;
        pulses(q,:)=[pb pe];
    end

    events=unique([t0;t1;grid;pulses(:)]);
    events=events(events>=t0 & events<=t1);
    events=sort(events);

    x_nl=xstar;
    dx_full=zeros(6,1);
    z_pair=zeros(2,1);
    yg_nl=zeros(numel(grid),1);
    yg_full=zeros(numel(grid),1);
    yg_pair=zeros(numel(grid),1);
    gidx=1;
    if grid(1)==t0
        yg_nl(1)=C*x_nl;
        yg_full(1)=C*(xstar+dx_full);
        yg_pair(1)=real(C*xstar+Cp_pair*z_pair);
        gidx=2;
    end

    for si=1:numel(events)-1
        ta=events(si); tb=events(si+1);
        if tb<=ta, continue; end
        tm=(ta+tb)/2;
        u=0;
        for q=1:npulse
            if tm>=pulses(q,1) && tm<pulses(q,2), u=1; break; end
        end
        dt=tb-ta;

        % Native nonlinear source model.
        [~,yn]=ode23s(@(t,y) reduced(t,y,u),[ta tb],x_nl,[]);
        x_nl=yn(end,:)';

        % Complete local six-mode response. Augmented exponential avoids J^-1.
        M=[J B*u; zeros(1,7)];
        E=expm(M*dt);
        aug=E*[dx_full;1];
        dx_full=aug(1:6);

        % Frozen chi-bearing complex-pair carrier.
        Mp=[Lam Bp_pair*u; zeros(1,3)];
        Ep=expm(Mp*dt);
        augp=Ep*[z_pair;1];
        z_pair=augp(1:2);

        while gidx<=numel(grid) && abs(grid(gidx)-tb)<1e-7
            yg_nl(gidx)=C*x_nl;
            yg_full(gidx)=C*(xstar+dx_full);
            yg_pair(gidx)=real(C*xstar+Cp_pair*z_pair);
            gidx=gidx+1;
        end
    end

    if gidx<=numel(grid)
        error('BIO_CHI_JARUS_JOINT_GRID_INCOMPLETE_%s_%d',pid,gidx);
    end

    rng_nl=max(yg_nl)-min(yg_nl);
    if ~(isfinite(rng_nl) && rng_nl>0)
        nrmse_pair=NaN; nrmse_full=NaN; max_pair=NaN; max_full=NaN;
        ptn=NaN; ptp=NaN; ptf=NaN; par=NaN; far=NaN;
        status='INDETERMINATE_PROTOCOL';
    else
        nrmse_pair=sqrt(mean((yg_pair-yg_nl).^2))/rng_nl;
        nrmse_full=sqrt(mean((yg_full-yg_nl).^2))/rng_nl;
        max_pair=max(abs(yg_pair-yg_nl))/rng_nl;
        max_full=max(abs(yg_full-yg_nl))/rng_nl;
        [ptn,pan]=first_peak(grid,yg_nl,tnf_begin);
        [ptp,pap]=first_peak(grid,yg_pair,tnf_begin);
        [ptf,paf]=first_peak(grid,yg_full,tnf_begin);
        if isfinite(pan) && pan~=0 && isfinite(pap), par=pap/pan; else, par=NaN; end
        if isfinite(pan) && pan~=0 && isfinite(paf), far=paf/pan; else, far=NaN; end
        status='EVALUABLE';
    end

    rec=struct();
    rec.protocol=pid;
    rec.nonlinear_range=rng_nl;
    rec.pair_nrmse=nrmse_pair;
    rec.full_modal_nrmse=nrmse_full;
    rec.pair_minus_full_modal_nrmse=nrmse_pair-nrmse_full;
    rec.pair_normalized_max_abs_error=max_pair;
    rec.full_modal_normalized_max_abs_error=max_full;
    rec.first_peak_time_nonlinear_s=ptn;
    rec.first_peak_time_pair_s=ptp;
    rec.first_peak_time_full_modal_s=ptf;
    rec.first_peak_amplitude_ratio_pair_to_nonlinear=par;
    rec.first_peak_amplitude_ratio_full_modal_to_nonlinear=far;
    rec.status=status;
    records=[records rec]; %#ok<AGROW>
    all_pair(end+1)=nrmse_pair; %#ok<AGROW>
    all_full(end+1)=nrmse_full; %#ok<AGROW>

    T=table(grid/3600,yg_nl,yg_full,yg_pair,'VariableNames',{'time_h','nonlinear_nfkb','full_modal_nfkb','pair_carrier_nfkb'});
    writetable(T,fullfile(outdir,[pid '_trajectory.csv']));
end

finite_mask=isfinite(all_pair)&isfinite(all_full);
if sum(finite_mask)~=7
    overall='MIXED_PROTOCOL_DEPENDENT';
else
    pp=all_pair(finite_mask); ff=all_full(finite_mask);
    pair_adequate=(median(pp)<=0.25)&&(max(pp)<=0.50);
    modal_adequate=(median(ff)<=0.25)&&(max(ff)<=0.50);
    modal_added=(sum(ff<pp)>=5)&&(median(pp-ff)>=0.05);
    if pair_adequate
        overall='PAIR_CARRIER_SUFFICIENT';
    elseif modal_adequate && modal_added
        overall='FULL_MODAL_SUFFICIENT_PAIR_INSUFFICIENT';
    elseif ~modal_adequate
        overall='NONLINEAR_SYSTEM_REQUIRED';
    else
        overall='MIXED_PROTOCOL_DEPENDENT';
    end
end

% Frozen zero-input integrity.
zero_rhs=max(abs(reduced(0,xstar,0)));
zero_full=max(abs(expm(J*3600)*zeros(6,1)));
zero_pair=max(abs(expm(Lam*3600)*zeros(2,1)));
known_bad_pass=(zero_rhs<1e-12)&&(zero_full<1e-12)&&(zero_pair<1e-12);

result=struct();
result.schema_version='0.1';
result.project='Bio Chi Investigation';
result.gate='Jaruszewicz same-system scalar-modal-system joint response';
result.freeze='BIO_CHI/config/JARUS_JOINT_SCALAR_MODAL_SYSTEM_P0Q_FREEZE_v0_1.json';
result.chi_bio_candidate=chi_calc;
result.chi_relative_difference_from_inherited_pin=chi_rel;
result.eigenvector_condition_number=eigvec_condition;
result.B_numeric=B';
result.B_expected=B_expected';
result.B_max_abs_error=B_error;
result.protocols=records;
result.pair_median_nrmse=median(all_pair,'omitnan');
result.full_modal_median_nrmse=median(all_full,'omitnan');
result.pair_max_nrmse=max(all_pair);
result.full_modal_max_nrmse=max(all_full);
result.protocols_full_modal_better=sum(all_full<all_pair);
result.median_pair_minus_full_modal_nrmse=median(all_pair-all_full,'omitnan');
result.known_bad_zero_input_pass=known_bad_pass;
result.status=overall;
result.chi_bio_broadly_admitted=false;
result.Chi_bio_broadly_admitted=false;
result.Bio_Chi_predictive_tool_admitted=false;
result.interpretation_limit='Same-model P0-Q Function/Limit mapping only. Nonlinear model is a native system reference, not experimental ground truth.';

fid=fopen(fullfile(outdir,'jarus_joint_scalar_modal_system_p0q_v0_1.json'),'w');
fwrite(fid,jsonencode(result,'PrettyPrint',true),'char');
fclose(fid);

disp(result);
disp(['BIO_CHI_JARUS_JOINT_STATUS ' overall]);

if ~known_bad_pass
    error('BIO_CHI_JARUS_JOINT_ZERO_INPUT_INTEGRITY_FAIL');
end
rmpath(source_dir);

function [tp,amp]=first_peak(t,y,tmin)
tp=NaN; amp=NaN;
for k=2:numel(y)-1
    if t(k)>=tmin && y(k)>y(k-1) && y(k)>y(k+1)
        tp=t(k); amp=y(k); return;
    end
end
end
