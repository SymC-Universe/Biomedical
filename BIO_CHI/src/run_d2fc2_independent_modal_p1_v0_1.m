% Independent D2FC2 NF-kB modal/observability test.
% Executes only after BIO_CHI/config/D2FC2_NFKB_INDEPENDENT_MODAL_P1_FREEZE_v0_1.json.
% External source is pinned at recleelab/D2FCSquared commit
% 4414c1556e3068c9bfe2162d5ba9d2cf770713fc.

set(groot,'defaultFigureVisible','off');
close all force;

thisfile = mfilename('fullpath');
srcdir = fileparts(thisfile);
biodir = fileparts(srcdir);
root = fileparts(biodir);
ext = fullfile(root,'external_d2fc2');
outdir = fullfile(biodir,'artifacts','generated','d2fc2_independent_modal_p1');
if exist(outdir,'dir'), rmdir(outdir,'s'); end
mkdir(outdir);

addpath(ext);
addpath(fullfile(ext,'Classes'));
addpath(fullfile(ext,'Functions'));
addpath(fullfile(ext,'Data'));

% Load source-native modelType 1 parameterization.
parameters = readtable(fullfile(ext,'ModelParameters.xlsx'),"Sheet","MainTextModels");
model = D2FCSquared();
parameterSet = parameters.D2FCSquared;
model = UpdateParameters(model,parameterSet,16);
initialCondition = [model.Species.Value]';

% Log species only for local-generator construction.
cs = getconfigset(model,'active');
cs.RuntimeOptions.StatesToLog = model.Species;
set(cs,'SolverType','sundials');
set(cs.SolverOptions,'AbsoluteTolerance',1e-9);
set(cs.SolverOptions,'RelativeTolerance',1e-9);
set(cs.SolverOptions,'MaxStep',60);

TR = sbioselect(model,"Type","parameter","Name","TR");
TR.Value = 0;

% Source-native 10-day pre-equilibration.
for i=1:numel(model.Species), model.Species(i).InitialAmount = initialCondition(i); end
set(cs,'StopTime',10*24*60*60);
[t0,s0,n0] = sbiosimulate(model);
xstar = s0(end,1:numel(model.Species))';

% Local RHS by a very short autonomous TR=0 simulation.
dt = 0.05; % seconds
multipliers = [1.0 0.5 0.25];
baseStep = 1e-6;
steps = struct([]);
for mi=1:numel(multipliers)
    mult = multipliers(mi);
    J = zeros(numel(xstar));
    f0 = local_rhs(model,cs,TR,xstar,dt);
    for j=1:numel(xstar)
        h = mult*baseStep*max(1,abs(xstar(j)));
        xp = xstar; xp(j)=xp(j)+h;
        fp = local_rhs(model,cs,TR,xp,dt);
        if xstar(j) > h
            xm = xstar; xm(j)=xm(j)-h;
            fm = local_rhs(model,cs,TR,xm,dt);
            J(:,j) = (fp-fm)/(2*h);
        else
            J(:,j) = (fp-f0)/h;
        end
    end
    ev = eig(J);
    steps(mi).multiplier = mult;
    steps(mi).eigenvalues_real = real(ev(:))';
    steps(mi).eigenvalues_imag = imag(ev(:))';
    steps(mi).max_real_eigenvalue = max(real(ev));
    if mi==1
        Jbase=J; evbase=ev;
    end
end

% Match eigenvalues to base step and assess numerical spread.
maxSpread = 0;
for mi=2:numel(steps)
    z = complex(steps(mi).eigenvalues_real,steps(mi).eigenvalues_imag);
    used=false(size(z));
    for bi=1:numel(evbase)
        [~,order] = sort(abs(z-evbase(bi)));
        pick = order(find(~used(order),1,'first'));
        used(pick)=true;
        rel = abs(z(pick)-evbase(bi))/max(abs(evbase(bi)),1e-12);
        maxSpread=max(maxSpread,rel);
    end
end

% Enumerate stable conjugate pairs in base spectrum without choosing among
% multiple pairs. Only positive-imaginary representatives are retained.
pairRecords = struct([]);
pi=0;
for k=1:numel(evbase)
    z=evbase(k);
    if imag(z)<=1e-10, continue; end
    [d,idx]=min(abs(evbase-conj(z)));
    if d > 1e-6*max(abs(z),1e-12), continue; end
    pi=pi+1;
    pairRecords(pi).real_s_inv=real(z);
    pairRecords(pi).imag_s_inv=imag(z);
    pairRecords(pi).stable=real(z)<0;
    pairRecords(pi).chi=(-real(z))/abs(z);
    pairRecords(pi).period_min=(2*pi/abs(imag(z)))/60;
    pairRecords(pi).conjugate_match_error=d;
end
stablePairs = pairRecords([pairRecords.stable]);

% Known-bad generator fixture: real diagonal stable matrix must yield no
% complex pair.
Jbad = diag(-[1 2 3 4 5 6]*1e-3);
evbad=eig(Jbad);
knownBadGeneratorPass = ~any(abs(imag(evbad))>1e-12);

% Open source-native experimental validation data only after freeze.
load(fullfile(ext,'Data','ExpData.mat'));
fittedIKKProfiles = readtable(fullfile(ext,'Data','MeanIKKTrajectories.csv'));
scenarios = string(fittedIKKProfiles.Scenarios);
expected = ["Control","1X30 sec","1X2 min","1X6 min","1X15 min","1X30 min","2X3 min","3X2 min","4X1.5 min"];
sourcePartitionPass = isequal(scenarios(:)',expected);

validation = struct([]);
for ith=5:9
    scenario=scenarios(ith);
    y=GetMeanNuclearRelAExpData(ExpData,scenario);
    y=y(:);
    tmin=(0:4:181)';
    n=min(numel(y),numel(tmin)); y=y(1:n); tt=tmin(1:n);
    yrange=max(y)-min(y);
    if n>=5
        ys=smoothdata(y,'sgolay',5);
    else
        ys=y;
    end
    if yrange>0
        prom=0.10*yrange;
        [pks,locs]=findpeaks(ys,'MinPeakProminence',prom);
    else
        pks=[]; locs=[];
    end
    identifiable=numel(locs)>=2;
    if identifiable
        periods=diff(tt(locs));
        periodMed=median(periods);
        omegaEmp=2*pi/periodMed; % rad/min
    else
        periods=[];
        periodMed=NaN;
        omegaEmp=NaN;
    end
    validation(ith-4).scenario=char(scenario);
    validation(ith-4).n_points=n;
    validation(ith-4).range=yrange;
    validation(ith-4).peak_count=numel(locs);
    validation(ith-4).peak_times_min=tt(locs)';
    validation(ith-4).interpeak_min=periods';
    validation(ith-4).median_period_min=periodMed;
    validation(ith-4).omega_rad_per_min=omegaEmp;
    validation(ith-4).identifiable=logical(identifiable);
end

% Known-bad empirical fixture: monotone trace must be non-identifiable.
tb=(0:4:181)';
yb=1+exp(-tb/45);
ybs=smoothdata(yb,'sgolay',5);
[~,lb]=findpeaks(ybs,'MinPeakProminence',0.1*(max(yb)-min(yb)));
knownBadEmpiricalPass=numel(lb)<2;

result=struct();
result.schema_version='0.1';
result.project='Bio Chi Investigation';
result.gate='D2FC2 independent NF-kB generator/modal and validation-observability test';
result.freeze='BIO_CHI/config/D2FC2_NFKB_INDEPENDENT_MODAL_P1_FREEZE_v0_1.json';
result.external_commit='4414c1556e3068c9bfe2162d5ba9d2cf770713fc';
result.source_partition_pass=logical(sourcePartitionPass);
result.equilibrium=xstar';
result.local_generator_steps=steps;
result.maximum_matched_eigenvalue_relative_spread=maxSpread;
result.complex_pairs=pairRecords;
result.stable_complex_pair_count=numel(stablePairs);
result.validation=validation;
result.known_bad_generator_pass=logical(knownBadGeneratorPass);
result.known_bad_empirical_pass=logical(knownBadEmpiricalPass);
result.chi_bio_admitted=false;
result.Chi_bio_admitted=false;
result.Bio_Chi_constructed=false;

% Frozen adjudication.
if ~sourcePartitionPass
    result.status='INVALID_TEST_SOURCE_PARTITION';
elseif ~knownBadGeneratorPass || ~knownBadEmpiricalPass
    result.status='INVALID_TEST_KNOWN_BAD_FAILURE';
elseif maxSpread>1e-5
    result.status='NON_IDENTIFIABLE_NUMERICAL_GENERATOR';
elseif numel(stablePairs)==0
    result.status='NO_LICENSED_COMPLEX_PAIR';
elseif numel(stablePairs)>1
    result.status='NON_IDENTIFIABLE_MULTIPLE_STABLE_COMPLEX_PAIRS';
else
    omegaGen=abs(stablePairs(1).imag_s_inv)*60; % rad/min
    identifiable=[validation.identifiable];
    idx=find(identifiable);
    errs=[];
    for q=idx
        errs(end+1)=abs(validation(q).omega_rad_per_min-omegaGen)/omegaGen; %#ok<AGROW>
        validation(q).relative_frequency_error=errs(end);
    end
    for q=find(~identifiable)
        validation(q).relative_frequency_error=NaN;
    end
    result.validation=validation;
    result.selected_pair=stablePairs(1);
    result.selected_pair.omega_rad_per_min=omegaGen;
    result.identifiable_validation_count=sum(identifiable);
    if isempty(errs), mederr=NaN; else, mederr=median(errs); end
    result.median_relative_frequency_error=mederr;
    if sum(identifiable)>=3 && mederr<=0.25
        result.status='INDEPENDENT_MODEL_MODAL_AND_OBSERVABILITY_SUPPORT';
    else
        result.status='GENERATOR_PAIR_EXISTS_BUT_EMPIRICAL_OBSERVABILITY_FAILS';
    end
end

fid=fopen(fullfile(outdir,'d2fc2_independent_modal_p1_v0_1.json'),'w');
fwrite(fid,jsonencode(result,'PrettyPrint',true),'char'); fclose(fid);

disp(result.status);
disp(result);
disp('BIO_CHI_D2FC2_INDEPENDENT_GATE_COMPLETE');

function f=local_rhs(model,cs,TR,x,dt)
    TR.Value=0;
    for ii=1:numel(model.Species), model.Species(ii).InitialAmount=max(x(ii),0); end
    set(cs,'StopTime',dt);
    [~,s,~]=sbiosimulate(model);
    x1=s(end,1:numel(model.Species))';
    f=(x1-x)/dt;
end
