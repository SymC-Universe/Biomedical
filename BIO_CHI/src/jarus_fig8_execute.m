% Execute the prospectively frozen Jaruszewicz Figure 8 parameter cases.
% This gate captures trajectories only. It does not classify dynamics, select
% modes, or construct chi_bio / Chi_bio / Bio Chi.

set(groot,'defaultFigureVisible','off');
close all force;

biochi_this = mfilename('fullpath');
biochi_src = fileparts(biochi_this);
biochi_bio = fileparts(biochi_src);
biochi_root = fileparts(biochi_bio);
biochi_cases_root = fullfile(biochi_bio,'artifacts','generated','jarus_fig8_cases');
biochi_out = fullfile(biochi_bio,'artifacts','generated','jarus_fig8_execution');
if exist(biochi_out,'dir'), rmdir(biochi_out,'s'); end
mkdir(biochi_out);

biochi_cases = {
    'FIG8A_NOMINAL_DAMPED', 9;
    'FIG8B_LIMIT_CYCLE', 30;
    'FIG8C_RELAXATION_OSCILLATION', 30
};

biochi_manifest = struct('case_id',{},'duration_hours',{},'axis_count',{},'numeric_line_count',{},'semantic_map_file',{});

for ci = 1:size(biochi_cases,1)
    case_id = biochi_cases{ci,1};
    duration_h = biochi_cases{ci,2};
    case_src = fullfile(biochi_cases_root,case_id,'source');
    case_out = fullfile(biochi_out,case_id);
    mkdir(case_out);

    clear reduced simulate_reduced;
    addpath(case_src,'-begin');
    close all force;
    diary(fullfile(case_out,'matlab_stdout.txt'));
    fprintf('BIO_CHI_JARUS_FIG8_CASE_BEGIN %s\n',case_id);
    fprintf('MATLAB_VERSION %s\n',version);

    simulate_reduced(duration_h*3600, 0, 1, case_id);
    drawnow;

    figs = findall(groot,'Type','figure');
    if isempty(figs)
        error('BIO_CHI_JARUS_FIG8_NO_FIGURE_%s',case_id);
    end
    fig = figs(1);
    axes_handles = flipud(findall(fig,'Type','axes'));
    semantics = struct('axis_index',{},'axis_title',{},'x_label',{},'y_label',{},'x_lim',{},'y_lim',{},'csv_file',{});
    numeric_count = 0;
    for ai = 1:numel(axes_handles)
        ax = axes_handles(ai);
        lines = flipud(findall(ax,'Type','line'));
        for li = 1:numel(lines)
            x = get(lines(li),'XData');
            y = get(lines(li),'YData');
            if ~(isnumeric(x) && isnumeric(y)) || isempty(x) || numel(x) ~= numel(y)
                continue;
            end
            numeric_count = numeric_count + 1;
            csv_name = sprintf('axis_%02d_line_%02d.csv',ai,li);
            writematrix([x(:) y(:)],fullfile(case_out,csv_name));
            semantics(numeric_count).axis_index = double(ai);
            semantics(numeric_count).axis_title = biochi_graphics_text(get(ax,'Title'));
            semantics(numeric_count).x_label = biochi_graphics_text(get(ax,'XLabel'));
            semantics(numeric_count).y_label = biochi_graphics_text(get(ax,'YLabel'));
            semantics(numeric_count).x_lim = double(get(ax,'XLim'));
            semantics(numeric_count).y_lim = double(get(ax,'YLim'));
            semantics(numeric_count).csv_file = csv_name;
        end
    end

    fid=fopen(fullfile(case_out,'semantic_map.json'),'w');
    fwrite(fid,jsonencode(semantics,'PrettyPrint',true),'char');
    fclose(fid);
    save(fullfile(case_out,'trajectory_capture.mat'),'semantics','case_id','duration_h','-v7');

    biochi_manifest(ci).case_id = case_id;
    biochi_manifest(ci).duration_hours = duration_h;
    biochi_manifest(ci).axis_count = double(numel(axes_handles));
    biochi_manifest(ci).numeric_line_count = double(numeric_count);
    biochi_manifest(ci).semantic_map_file = fullfile(case_id,'semantic_map.json');

    fprintf('BIO_CHI_JARUS_FIG8_CASE_END %s AXES=%d LINES=%d\n',case_id,numel(axes_handles),numeric_count);
    diary off;
    rmpath(case_src);
end

summary = struct();
summary.schema_version = '0.1';
summary.audit_type = 'prospectively_frozen_figure8_trajectory_execution';
summary.execution_freeze = 'BIO_CHI/config/JARUS_FIG8_EXECUTION_FREEZE_v0_1.json';
summary.cases = biochi_manifest;
summary.scientific_endpoint_opened = false;
summary.chi_bio_constructed = false;
summary.Chi_bio_constructed = false;
summary.Bio_Chi_constructed = false;
summary.interpretation_limit = 'Trajectory execution only. No behavior classification or scalar/modal inference is made in this gate.';
fid=fopen(fullfile(biochi_out,'execution_summary.json'),'w');
fwrite(fid,jsonencode(summary,'PrettyPrint',true),'char');
fclose(fid);
disp(summary);
disp('BIO_CHI_JARUS_FIG8_EXECUTION_PASS');

function txt = biochi_graphics_text(obj)
    try
        value=get(obj,'String');
        if isstring(value)
            txt=strjoin(cellstr(value(:)),' | ');
        elseif ischar(value)
            if size(value,1)>1, txt=strjoin(cellstr(value),' | '); else, txt=value; end
        elseif iscell(value)
            parts=cellfun(@char,value,'UniformOutput',false);
            txt=strjoin(parts,' | ');
        else
            txt='';
        end
    catch
        txt='';
    end
end
