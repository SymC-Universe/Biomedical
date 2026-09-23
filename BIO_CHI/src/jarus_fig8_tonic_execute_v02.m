% Corrected Figure 8 trajectory execution under JARUS_FIG8_EXECUTION_FREEZE_v0_2.
% This script repairs only the published helper's fixed-horizon control flow.
% It does not classify behavior, select modes, or construct chi_bio / Chi_bio / Bio Chi.

biochi_this = mfilename('fullpath');
biochi_src = fileparts(biochi_this);
biochi_bio = fileparts(biochi_src);
biochi_cases_root = fullfile(biochi_bio,'artifacts','generated','jarus_fig8_cases');
biochi_out = fullfile(biochi_bio,'artifacts','generated','jarus_fig8_execution_v02');
if exist(biochi_out,'dir'), rmdir(biochi_out,'s'); end
mkdir(biochi_out);

% Published reduced-model state order.
state_names = {'IKKn','IKKa','free nuclear NF-kappaB','A20', ...
               'free cytoplasmic IkappaBalpha','IkappaBalpha_t'};
reference_state = [1 0 0 0 0 0];
t_equil_begin = -20*3600;
t_tnf_begin = 1*3600;

cases = {
    'FIG8A_NOMINAL_DAMPED', 10;
    'FIG8B_LIMIT_CYCLE', 30;
    'FIG8C_RELAXATION_OSCILLATION', 30
};

manifest = struct('case_id',{},'observation_end_hours',{},'row_count',{}, ...
                  'time_monotone',{},'all_states_finite',{},'trajectory_file',{});

for ci = 1:size(cases,1)
    case_id = cases{ci,1};
    end_h = cases{ci,2};
    case_src = fullfile(biochi_cases_root,case_id,'source');
    case_out = fullfile(biochi_out,case_id);
    mkdir(case_out);

    clear reduced;
    addpath(case_src,'-begin');
    diary(fullfile(case_out,'matlab_stdout.txt'));
    fprintf('BIO_CHI_JARUS_FIG8_V02_CASE_BEGIN %s\n',case_id);
    fprintf('MATLAB_VERSION %s\n',version);

    % Reproduce the authors' pre-stimulus equilibration under TR=0, then
    % keep tonic TNF ON monotonically from t=1 h to the frozen endpoint.
    [t0,y0] = ode23s(@(t,y) reduced(t,y,0), ...
                     [t_equil_begin t_tnf_begin], reference_state, []);
    tonic_initial = y0(end,:);
    [t1,y1] = ode23s(@(t,y) reduced(t,y,1), ...
                     [t_tnf_begin end_h*3600], tonic_initial, []);

    t = [t0; t1(2:end)] / 3600;
    y = [y0; y1(2:end,:)];
    trajectory = [t y];

    time_monotone = all(diff(t) > 0);
    all_states_finite = all(isfinite(trajectory),'all');
    if ~time_monotone
        error('BIO_CHI_JARUS_FIG8_V02_NONMONOTONE_TIME_%s',case_id);
    end
    if ~all_states_finite
        error('BIO_CHI_JARUS_FIG8_V02_NONFINITE_STATE_%s',case_id);
    end

    csv_file = fullfile(case_out,'trajectory_raw.csv');
    writematrix(trajectory,csv_file);
    save(fullfile(case_out,'trajectory_raw.mat'),'t','y','state_names','case_id','end_h','-v7');

    semantics = struct();
    semantics.time_units = 'hours';
    semantics.columns = [{'time_h'}, state_names];
    semantics.tnf_onset_h = 1;
    semantics.observation_end_h = end_h;
    semantics.trajectory_is_raw_state = true;
    semantics.plot_normalization_applied = false;
    fid=fopen(fullfile(case_out,'semantic_map.json'),'w');
    fwrite(fid,jsonencode(semantics,'PrettyPrint',true),'char');
    fclose(fid);

    manifest(ci).case_id = case_id;
    manifest(ci).observation_end_hours = end_h;
    manifest(ci).row_count = size(trajectory,1);
    manifest(ci).time_monotone = logical(time_monotone);
    manifest(ci).all_states_finite = logical(all_states_finite);
    manifest(ci).trajectory_file = fullfile(case_id,'trajectory_raw.csv');

    fprintf('BIO_CHI_JARUS_FIG8_V02_CASE_END %s ROWS=%d END_H=%g\n', ...
            case_id,size(trajectory,1),end_h);
    diary off;
    rmpath(case_src);
end

summary = struct();
summary.schema_version = '0.2';
summary.audit_type = 'corrected_monotone_tonic_figure8_execution';
summary.execution_freeze = 'BIO_CHI/config/JARUS_FIG8_EXECUTION_FREEZE_v0_2.json';
summary.preserved_failure_pin = 'BIO_CHI/config/JARUS_FIG8_EXECUTION_VALIDITY_PIN_v0_1.json';
summary.cases = manifest;
summary.behavior_classified = false;
summary.chi_bio_constructed = false;
summary.Chi_bio_constructed = false;
summary.Bio_Chi_constructed = false;
summary.interpretation_limit = 'Trajectory execution and integrity only. Behavior adjudication is a separate frozen gate.';
fid=fopen(fullfile(biochi_out,'execution_summary.json'),'w');
fwrite(fid,jsonencode(summary,'PrettyPrint',true),'char');
fclose(fid);
disp(summary);
disp('BIO_CHI_JARUS_FIG8_V02_EXECUTION_PASS');
