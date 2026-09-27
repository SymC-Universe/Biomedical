function nfkb_d2fc_native_modal_p0q_v01
% Frozen D2FC^2 native-modal biological chi P0-Q execution.
% Contract: BIO_CHI/control/NFKB_D2FC_NATIVE_MODAL_P0Q_FREEZE_v0_1.md

repoRoot = pwd;
sourceRoot = fullfile(repoRoot,"nfkb_d2fc_source");
outdir = fullfile(repoRoot,"BIO_CHI","experiments","nfkb_d2fc_results");
if ~exist(outdir,"dir"), mkdir(outdir); end
cd(sourceRoot);
addpath("Classes","Data","Functions");

try
    sourceCommit = "4414c1556e3068c9bfe2162d5ba9d2cf770713fc";
    fittedIKKProfiles = readtable("Data/MeanIKKTrajectories.csv");
    scenarios = string(fittedIKKProfiles.Scenarios);
    if numel(scenarios) ~= 9
        error("Expected 9 source scenarios, found %d",numel(scenarios));
    end

    expLoaded = load("Data/ExpData.mat");
    ExpData = expLoaded.ExpData;
    expTimes = (0:4:180)'; % source source-data grid: 46 points

    % Source-preferred D2FC^2 model.
    [model, initialCondition] = build_source_model(1);
    speciesKeys = get_species_keys(model);
    idxNuc = [find(speciesKeys=="Nucleus.NFkB",1), ...
              find(speciesKeys=="Nucleus.NFkBDNA",1), ...
              find(speciesKeys=="Nucleus.IkBaNFkB",1)];
    if any(isempty(idxNuc)) || numel(idxNuc) ~= 3
        error("Could not resolve the three source nuclear NF-kB species");
    end

    stageA = repmat(struct(),numel(scenarios),1);
    finalStates = cell(numel(scenarios),1);
    allFinite = true;
    for i = 1:numel(scenarios)
        sc = strtrim(scenarios(i));
        ikkPars = fittedIKKProfiles{i,2:end};
        model = UpdateParameters(model,ikkPars,1);
        [tSec,x] = simulate_source_scenario(model,initialCondition);
        finalStates{i} = x(end,:)';

        totalNuc = sum(x(:,idxNuc),2);
        relNuc = totalNuc ./ totalNuc(1);
        modelGrid = interp1(tSec./60,relNuc,expTimes,"linear","extrap");
        expGrid = GetMeanNuclearRelAExpData(ExpData,sc);
        expGrid = expGrid(:);

        if numel(expGrid) ~= 46 || any(~isfinite(expGrid)) || any(~isfinite(modelGrid))
            allFinite = false;
        end

        diffv = modelGrid-expGrid;
        rmse = sqrt(mean(diffv.^2));
        if std(modelGrid)>0 && std(expGrid)>0
            C = corrcoef(modelGrid,expGrid);
            pearson = C(1,2);
        else
            pearson = NaN;
        end
        [mPeak,mIdx] = max(modelGrid);
        [ePeak,eIdx] = max(expGrid);
        lateMask = expTimes>=120;
        stageA(i).scenario = char(sc);
        stageA(i).source_split = char(ternary(i<=4,"fit","validation"));
        stageA(i).n_points = numel(expGrid);
        stageA(i).rmse = rmse;
        stageA(i).pearson_r = pearson;
        stageA(i).model_peak = mPeak;
        stageA(i).model_time_to_peak_min = expTimes(mIdx);
        stageA(i).model_auc = trapz(expTimes,modelGrid);
        stageA(i).model_late_mean_120_180 = mean(modelGrid(lateMask));
        stageA(i).experimental_peak = ePeak;
        stageA(i).experimental_time_to_peak_min = expTimes(eIdx);
        stageA(i).experimental_auc = trapz(expTimes,expGrid);
        stageA(i).experimental_late_mean_120_180 = mean(expGrid(lateMask));
    end

    stageAPass = allFinite && all([stageA.n_points]==46);
    writetable(struct2table(stageA),fullfile(outdir,"stageA_source_trajectory_fidelity.csv"));

    result = struct();
    result.schema_version = "0.1";
    result.experiment_id = "NFKB_D2FC_NATIVE_MODAL_P0Q_V01";
    result.evidence_class = "P0-Q_LITERATURE_OPEN_SOURCE_MODEL_NATIVE_MODAL_QUALIFICATION";
    result.source_repository = "recleelab/D2FCSquared";
    result.source_commit = sourceCommit;
    result.stageA_pass = stageAPass;
    result.stageA = stageA;
    result.chi_formula = "-trace(J_pair)/(2*sqrt(det(J_pair))) = -real(lambda)/abs(lambda)";

    if ~stageAPass
        result.status = "VALID_REFUSAL_SOURCE_TRAJECTORY_GATE_FAILED";
        result.biological_chi = "NOT_OPENED_STAGE_A_SOURCE_GATE_FAILED";
        result.Chi_bio = "NOT_OPENED_STAGE_A_SOURCE_GATE_FAILED";
        result.chi_bio = "NOT_OPENED_STAGE_A_SOURCE_GATE_FAILED";
        write_json(fullfile(outdir,"NFKB_D2FC_NATIVE_MODAL_P0Q_V01_RESULT.json"),result);
        disp(jsonencode(result,PrettyPrint=true));
        cd(repoRoot);
        return;
    end

    % Baseline local recovery Jacobians for the eight stimulated scenarios.
    modal = repmat(struct(),8,1);
    stimulatedRows = 2:9; % all source scenarios except Control, preserving source order
    familyExactlyOne = true;
    for k = 1:numel(stimulatedRows)
        i = stimulatedRows(k);
        sc = strtrim(scenarios(i));
        x0 = finalStates{i};
        J = numerical_jacobian(model,x0,0.01,1e-5);
        [V,D] = eig(J);
        lam = diag(D);
        [summary,candidates] = modal_summary(lam);

        modal(k).scenario = char(sc);
        modal(k).spectral_abscissa = max(real(lam));
        modal(k).stable_complex_pairs = summary.stable_complex_pairs;
        modal(k).unstable_mode_count = summary.unstable_mode_count;
        modal(k).near_zero_mode_count = summary.near_zero_mode_count;
        modal(k).stable_real_mode_count = summary.stable_real_mode_count;
        modal(k).eigenvalues_real = real(lam)';
        modal(k).eigenvalues_imag = imag(lam)';
        modal(k).chi_candidates = candidates;
        if summary.stable_complex_pairs==0
            modal(k).local_scalar_status = "LOCAL_SCALAR_REFUSED_REAL_ONLY_OR_NONSTABLE";
        elseif summary.stable_complex_pairs==1
            modal(k).local_scalar_status = "LOCAL_SCALAR_CANDIDATE_UNIQUE_COMPLEX_PAIR";
            modal(k).chi_bio_candidate = candidates(1);
        else
            modal(k).local_scalar_status = "LOCAL_SCALAR_REFUSED_NONUNIQUE_COMPLEX_CARRIER";
        end
        if summary.stable_complex_pairs ~= 1
            familyExactlyOne = false;
        end

        writematrix(J,fullfile(outdir,"jacobian_"+sanitize(sc)+".csv"));
    end
    result.primary_modal = modal;

    % Numerical sensitivity is conditional and was frozen prospectively.
    robustness = struct();
    if familyExactlyOne
        baseChi = [modal.chi_bio_candidate];
        dtGrid = [0.005,0.02];
        epsGrid = [5e-6,2e-5];
        robust = true;
        records = repmat(struct(),numel(dtGrid)*numel(epsGrid)*8,1);
        rr = 0;
        for dti = 1:numel(dtGrid)
            for ei = 1:numel(epsGrid)
                for k = 1:8
                    rr = rr+1;
                    i = stimulatedRows(k);
                    sc = strtrim(scenarios(i));
                    J2 = numerical_jacobian(model,finalStates{i},dtGrid(dti),epsGrid(ei));
                    lam2 = eig(J2);
                    [sm2,cand2] = modal_summary(lam2);
                    records(rr).scenario = char(sc);
                    records(rr).dt = dtGrid(dti);
                    records(rr).perturbation_relative_factor = epsGrid(ei);
                    records(rr).stable_complex_pairs = sm2.stable_complex_pairs;
                    if sm2.stable_complex_pairs==1
                        records(rr).chi_bio_candidate = cand2(1);
                        relDiff = abs(cand2(1)-baseChi(k))/max(abs(baseChi(k)),eps);
                        records(rr).relative_chi_difference = relDiff;
                        if relDiff >= 0.05, robust = false; end
                    else
                        records(rr).chi_bio_candidate = NaN;
                        records(rr).relative_chi_difference = NaN;
                        robust = false;
                    end
                end
            end
        end
        robustness.executed = true;
        robustness.pass = robust;
        robustness.records = records;
        writetable(struct2table(records),fullfile(outdir,"scalar_numerical_robustness.csv"));
        if robust
            result.chi_bio = "ADMITTED_MODEL_SPECIFIC_UNIQUE_COMPLEX_FAMILY_P0Q";
        else
            result.chi_bio = "SCALAR_REFUSED_NUMERICAL_CLASS_OR_VALUE_SENSITIVITY";
        end
    else
        robustness.executed = false;
        robustness.pass = false;
        robustness.reason = "Family gate already refused because at least one stimulated scenario did not contain exactly one stable complex pair.";
        result.chi_bio = "REFUSED_NO_UNIQUE_COMPLEX_CARRIER_ACROSS_SOURCE_SCENARIOS";
    end
    result.scalar_numerical_robustness = robustness;

    % Source model-form sensitivity: original source D2FC optimized and original parameterizations.
    modelSensitivity = repmat(struct(),2,1);
    for mt = 2:3
        [m2,ic2] = build_source_model(mt);
        counts = zeros(1,8);
        localStatus = strings(1,8);
        for k = 1:8
            i = stimulatedRows(k);
            ikkPars = fittedIKKProfiles{i,2:end};
            m2 = UpdateParameters(m2,ikkPars,1);
            [~,x2] = simulate_source_scenario(m2,ic2);
            J2 = numerical_jacobian(m2,x2(end,:)',0.01,1e-5);
            [sm2,~] = modal_summary(eig(J2));
            counts(k)=sm2.stable_complex_pairs;
            if counts(k)==1
                localStatus(k)="UNIQUE";
            elseif counts(k)==0
                localStatus(k)="NONE";
            else
                localStatus(k)="MULTIPLE";
            end
        end
        modelSensitivity(mt-1).model_type = mt;
        modelSensitivity(mt-1).model_name = char(ternary(mt==2,"D2FC Optimized","D2FC Original"));
        modelSensitivity(mt-1).stable_complex_pair_counts = counts;
        modelSensitivity(mt-1).local_status = cellstr(localStatus);
    end
    result.source_model_form_sensitivity = modelSensitivity;

    result.status = "EXECUTED_VALID_SOURCE_MODEL_NATIVE_MODAL_P0Q";
    result.Chi_bio = "QUALIFIED_MODEL_SPECIFIC_D2FC2_LOCAL_MODAL_FAMILY_P0Q";
    result.biological_chi = "IKK_PATH_TO_NFKB_RESPONSE_AND_LOCAL_RECOVERY_ORGANIZATION_QUALIFIED_P0Q";
    result.claim_ceiling = "Source/model P0-Q qualification only; no universal NF-kB scalar, no biological chi=1 boundary, no common mechanism across systems, and no cancer causal claim.";

    write_json(fullfile(outdir,"NFKB_D2FC_NATIVE_MODAL_P0Q_V01_RESULT.json"),result);
    disp(jsonencode(result,PrettyPrint=true));
    cd(repoRoot);
catch ME
    failure = struct("schema_version","0.1", ...
        "experiment_id","NFKB_D2FC_NATIVE_MODAL_P0Q_V01", ...
        "status","EXECUTION_FAILURE_PRESERVED", ...
        "error_identifier",ME.identifier, ...
        "error_message",ME.message);
    write_json(fullfile(outdir,"NFKB_D2FC_NATIVE_MODAL_P0Q_V01_FAILURE.json"),failure);
    cd(repoRoot);
    rethrow(ME);
end
end

function [model,initialCondition] = build_source_model(modelType)
parameters = readtable("ModelParameters.xlsx","Sheet","MainTextModels");
model = D2FCSquared();
switch modelType
    case 1
        parameterSet = parameters.D2FCSquared;
    case 2
        parameterSet = parameters.D2FCOptimized;
    case 3
        parameterSet = parameters.D2FC;
    otherwise
        error("Unsupported source model type");
end
model = UpdateParameters(model,parameterSet,16);
initialCondition = [model.Species.Value];
end

function [tStim,xStim] = simulate_source_scenario(model,initialCondition)
cs = getconfigset(model,"active");
set(cs,"SolverType","sundials");
set(cs.SolverOptions,"AbsoluteTolerance",1e-8);
set(cs.SolverOptions,"RelativeTolerance",1e-8);
cs.RuntimeOptions.StatesToLog = model.Species;

for j=1:numel(model.Species)
    model.Species(j).InitialAmount = initialCondition(j);
end
TR = sbioselect(model,"Type","parameter","Name","TR");
TR.Value = 0;
set(cs,"StopTime",10*24*60*60);
[t0,x0] = sbiosimulate(model);
baselineState = x0(end,:);

for j=1:numel(model.Species)
    model.Species(j).InitialAmount = baselineState(j);
end
TR.Value = 1;
set(cs,"StopTime",3*60*60);
set(cs.SolverOptions,"MaxStep",2*60);
[tStim,xStim] = sbiosimulate(model);

for j=1:numel(model.Species)
    model.Species(j).InitialAmount = initialCondition(j);
end
TR.Value = 0;
end

function J = numerical_jacobian(model,x,dt,relfactor)
n = numel(x);
J = zeros(n,n);
f0 = local_flow(model,x,dt);
for j=1:n
    delta = max(1e-10,relfactor*max(abs(x(j)),1e-4));
    xp=x; xp(j)=xp(j)+delta;
    fp=local_flow(model,xp,dt);
    if x(j)-delta >= 0
        xm=x; xm(j)=xm(j)-delta;
        fm=local_flow(model,xm,dt);
        J(:,j)=(fp-fm)/(2*delta);
    else
        J(:,j)=(fp-f0)/delta;
    end
end
end

function f = local_flow(model,x,dt)
cs = getconfigset(model,"active");
set(cs,"SolverType","sundials");
set(cs.SolverOptions,"AbsoluteTolerance",1e-10);
set(cs.SolverOptions,"RelativeTolerance",1e-10);
set(cs.SolverOptions,"MaxStep",dt/5);
set(cs,"StopTime",dt);
cs.RuntimeOptions.StatesToLog = model.Species;
TR = sbioselect(model,"Type","parameter","Name","TR");
TR.Value = 0;
for j=1:numel(model.Species)
    model.Species(j).InitialAmount = max(x(j),0);
end
[~,y] = sbiosimulate(model);
f=(y(end,:)'-x)/dt;
end

function [s,candidates] = modal_summary(lam)
tolComplex = 1e-8;
tolZero = 1e-8;
posComplex = find(imag(lam)>tolComplex & real(lam)<0);
candidates = zeros(1,numel(posComplex));
for q=1:numel(posComplex)
    z=lam(posComplex(q));
    candidates(q)=-real(z)/abs(z);
end
s = struct();
s.stable_complex_pairs = numel(posComplex);
s.unstable_mode_count = sum(real(lam)>tolZero);
s.near_zero_mode_count = sum(abs(lam)<=tolZero);
s.stable_real_mode_count = sum(real(lam)<-tolZero & abs(imag(lam))<=tolComplex);
end

function keys = get_species_keys(model)
keys = strings(1,numel(model.Species));
for j=1:numel(model.Species)
    keys(j)=string(model.Species(j).Parent.Name)+"."+string(model.Species(j).Name);
end
end

function s = sanitize(x)
s = regexprep(string(x),"[^A-Za-z0-9]+","_");
s = strip(s,"_");
end

function out = ternary(cond,a,b)
if cond, out=a; else, out=b; end
end

function write_json(path,s)
fid=fopen(path,"w");
if fid<0, error("Could not open JSON output %s",path); end
cleanup=onCleanup(@() fclose(fid));
fprintf(fid,"%s\n",jsonencode(s,PrettyPrint=true));
end
