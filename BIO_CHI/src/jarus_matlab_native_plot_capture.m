% Bio Chi P0-D native-output capture for the Jaruszewicz-Blońska reduced model.
% This script runs the already documented one-line MATLAB compatibility copy
% and captures every numeric line series plus the authors' figure/axis metadata.
% It does not select a biological endpoint, classify damping, or construct chi_bio.

set(groot,'defaultFigureVisible','off');
close all force;

biochi_this_file = mfilename('fullpath');
biochi_src_dir = fileparts(biochi_this_file);
biochi_bio_dir = fileparts(biochi_src_dir);
biochi_out_dir = fullfile(biochi_bio_dir,'artifacts','generated','jarus_native_plot_capture');
biochi_compat_root = fullfile(biochi_bio_dir,'artifacts','generated','jarus_matlab_compat');
biochi_base_dir = fullfile(biochi_compat_root,'source','S1_Codes','MATLAB files','Reduced2023');

if ~exist(biochi_out_dir,'dir')
    mkdir(biochi_out_dir);
end
assert(isfile(fullfile(biochi_base_dir,'reduced.m')));
assert(isfile(fullfile(biochi_base_dir,'run_simulate_reduced.m')));
assert(isfile(fullfile(biochi_base_dir,'simulate_reduced.m')));
assert(isfile(fullfile(biochi_compat_root,'compatibility_patch.json')));

cd(biochi_base_dir);
addpath(biochi_base_dir);
diary(fullfile(biochi_out_dir,'matlab_stdout.txt'));
disp('BIO_CHI_JARUS_NATIVE_PLOT_CAPTURE_BEGIN');
disp(version);

% Execute the authors' driver unchanged against the mechanically repaired
% simulate_reduced.m copy. All model equations, parameters, inputs, solver
% family, initial conditions, and plotting logic remain those of the source.
run('run_simulate_reduced.m');
drawnow;

biochi_figs = findall(groot,'Type','figure');
if ~isempty(biochi_figs)
    try
        [~,biochi_ord] = sort([biochi_figs.Number]);
        biochi_figs = biochi_figs(biochi_ord);
    catch
        % Figure handles remain exhaustively captured even if numbering differs.
    end
end

biochi_capture = struct('figure_number',{},'figure_name',{},'axis_index',{}, ...
    'axis_title',{},'x_label',{},'y_label',{},'x_scale',{},'y_scale',{}, ...
    'x_lim',{},'y_lim',{},'line_index',{},'display_name',{}, ...
    'x',{},'y',{},'csv_file',{});
biochi_semantics = struct('figure_number',{},'figure_name',{},'axis_index',{}, ...
    'axis_title',{},'x_label',{},'y_label',{},'x_scale',{},'y_scale',{}, ...
    'x_lim',{},'y_lim',{},'line_count',{},'line_display_names',{},'csv_files',{});
biochi_k = 0;
biochi_s = 0;

for biochi_fi = 1:numel(biochi_figs)
    biochi_fig = biochi_figs(biochi_fi);
    biochi_fig_name = biochi_get_text(biochi_fig,'Name');
    biochi_axes = findall(biochi_fig,'Type','axes');
    biochi_axes = flipud(biochi_axes(:));
    for biochi_ai = 1:numel(biochi_axes)
        biochi_ax = biochi_axes(biochi_ai);
        biochi_axis_title = biochi_graphics_text(get(biochi_ax,'Title'));
        biochi_x_label = biochi_graphics_text(get(biochi_ax,'XLabel'));
        biochi_y_label = biochi_graphics_text(get(biochi_ax,'YLabel'));
        biochi_x_scale = biochi_get_text(biochi_ax,'XScale');
        biochi_y_scale = biochi_get_text(biochi_ax,'YScale');
        biochi_x_lim = double(get(biochi_ax,'XLim'));
        biochi_y_lim = double(get(biochi_ax,'YLim'));
        biochi_lines = findall(biochi_ax,'Type','line');
        biochi_lines = flipud(biochi_lines(:));
        biochi_names = cell(0,1);
        biochi_csvs = cell(0,1);
        biochi_numeric_lines = 0;
        for biochi_li = 1:numel(biochi_lines)
            biochi_x = get(biochi_lines(biochi_li),'XData');
            biochi_y = get(biochi_lines(biochi_li),'YData');
            if ~(isnumeric(biochi_x) && isnumeric(biochi_y))
                continue;
            end
            biochi_x = biochi_x(:);
            biochi_y = biochi_y(:);
            if numel(biochi_x) ~= numel(biochi_y) || isempty(biochi_x)
                continue;
            end
            biochi_numeric_lines = biochi_numeric_lines + 1;
            biochi_k = biochi_k + 1;
            biochi_name = biochi_get_text(biochi_lines(biochi_li),'DisplayName');
            biochi_csv = sprintf('figure_%02d_axis_%02d_line_%02d.csv',biochi_fi,biochi_ai,biochi_numeric_lines);
            writematrix([biochi_x biochi_y],fullfile(biochi_out_dir,biochi_csv));
            biochi_names{end+1,1} = biochi_name;
            biochi_csvs{end+1,1} = biochi_csv;
            biochi_capture(biochi_k).figure_number = double(biochi_fi);
            biochi_capture(biochi_k).figure_name = biochi_fig_name;
            biochi_capture(biochi_k).axis_index = double(biochi_ai);
            biochi_capture(biochi_k).axis_title = biochi_axis_title;
            biochi_capture(biochi_k).x_label = biochi_x_label;
            biochi_capture(biochi_k).y_label = biochi_y_label;
            biochi_capture(biochi_k).x_scale = biochi_x_scale;
            biochi_capture(biochi_k).y_scale = biochi_y_scale;
            biochi_capture(biochi_k).x_lim = biochi_x_lim;
            biochi_capture(biochi_k).y_lim = biochi_y_lim;
            biochi_capture(biochi_k).line_index = double(biochi_numeric_lines);
            biochi_capture(biochi_k).display_name = biochi_name;
            biochi_capture(biochi_k).x = biochi_x;
            biochi_capture(biochi_k).y = biochi_y;
            biochi_capture(biochi_k).csv_file = biochi_csv;
        end
        biochi_s = biochi_s + 1;
        biochi_semantics(biochi_s).figure_number = double(biochi_fi);
        biochi_semantics(biochi_s).figure_name = biochi_fig_name;
        biochi_semantics(biochi_s).axis_index = double(biochi_ai);
        biochi_semantics(biochi_s).axis_title = biochi_axis_title;
        biochi_semantics(biochi_s).x_label = biochi_x_label;
        biochi_semantics(biochi_s).y_label = biochi_y_label;
        biochi_semantics(biochi_s).x_scale = biochi_x_scale;
        biochi_semantics(biochi_s).y_scale = biochi_y_scale;
        biochi_semantics(biochi_s).x_lim = biochi_x_lim;
        biochi_semantics(biochi_s).y_lim = biochi_y_lim;
        biochi_semantics(biochi_s).line_count = double(biochi_numeric_lines);
        biochi_semantics(biochi_s).line_display_names = biochi_names;
        biochi_semantics(biochi_s).csv_files = biochi_csvs;
    end
end

biochi_summary = struct();
biochi_summary.schema_version = '0.2';
biochi_summary.audit_type = 'authors_native_plot_output_and_semantic_capture';
biochi_summary.figure_count = double(numel(biochi_figs));
biochi_summary.axis_count = double(numel(biochi_semantics));
biochi_summary.numeric_line_count = double(numel(biochi_capture));
biochi_summary.chi_bio_constructed = false;
biochi_summary.scientific_endpoint_opened = false;
biochi_summary.capture_basis = 'all numeric line objects and author-authored figure/axis metadata produced by the published driver after the frozen one-line MATLAB API repair';
biochi_summary.interpretation_limit = 'Capture only. Metadata are preserved for mapping; no line is promoted, no damping class is assigned, and no scalar or modal Bio Chi quantity is computed.';

biochi_fid = fopen(fullfile(biochi_out_dir,'capture_summary.json'),'w');
fwrite(biochi_fid,jsonencode(biochi_summary,'PrettyPrint',true),'char');
fclose(biochi_fid);
biochi_fid = fopen(fullfile(biochi_out_dir,'semantic_map.json'),'w');
fwrite(biochi_fid,jsonencode(biochi_semantics,'PrettyPrint',true),'char');
fclose(biochi_fid);
save(fullfile(biochi_out_dir,'native_plot_capture.mat'),'biochi_capture','biochi_semantics','biochi_summary','-v7');

disp(biochi_summary);
disp('BIO_CHI_JARUS_NATIVE_PLOT_CAPTURE_END');
diary off;

if isempty(biochi_capture)
    error('BIO_CHI_JARUS_NATIVE_PLOT_CAPTURE_NO_NUMERIC_LINES');
end

function txt = biochi_get_text(obj,prop)
    try
        value = get(obj,prop);
        txt = biochi_value_text(value);
    catch
        txt = '';
    end
end

function txt = biochi_graphics_text(obj)
    try
        txt = biochi_value_text(get(obj,'String'));
    catch
        txt = '';
    end
end

function txt = biochi_value_text(value)
    if isstring(value)
        txt = strjoin(cellstr(value(:)),' | ');
    elseif ischar(value)
        if size(value,1) > 1
            txt = strjoin(cellstr(value),' | ');
        else
            txt = value;
        end
    elseif iscell(value)
        parts = cellfun(@biochi_value_text,value,'UniformOutput',false);
        txt = strjoin(parts,' | ');
    elseif isempty(value)
        txt = '';
    else
        try
            txt = char(string(value));
        catch
            txt = '';
        end
    end
end
