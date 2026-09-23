% Bio Chi P0-D native-output capture for the Jaruszewicz-Blońska reduced model.
% This script runs the already documented one-line MATLAB compatibility copy
% and captures every numeric line series produced by the authors' own driver.
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
        % Figure handles remain deterministic enough for exhaustive capture.
    end
end

biochi_capture = struct('figure_number',{},'axis_index',{},'line_index',{}, ...
    'display_name',{},'x',{},'y',{},'csv_file',{});
biochi_k = 0;

for biochi_fi = 1:numel(biochi_figs)
    biochi_fig = biochi_figs(biochi_fi);
    biochi_axes = findall(biochi_fig,'Type','axes');
    biochi_axes = flipud(biochi_axes(:));
    for biochi_ai = 1:numel(biochi_axes)
        biochi_lines = findall(biochi_axes(biochi_ai),'Type','line');
        biochi_lines = flipud(biochi_lines(:));
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
            biochi_k = biochi_k + 1;
            biochi_name = get(biochi_lines(biochi_li),'DisplayName');
            if isstring(biochi_name)
                biochi_name = char(biochi_name);
            elseif ~ischar(biochi_name)
                biochi_name = '';
            end
            biochi_csv = sprintf('figure_%02d_axis_%02d_line_%02d.csv',biochi_fi,biochi_ai,biochi_li);
            writematrix([biochi_x biochi_y],fullfile(biochi_out_dir,biochi_csv));
            biochi_capture(biochi_k).figure_number = double(biochi_fi);
            biochi_capture(biochi_k).axis_index = double(biochi_ai);
            biochi_capture(biochi_k).line_index = double(biochi_li);
            biochi_capture(biochi_k).display_name = biochi_name;
            biochi_capture(biochi_k).x = biochi_x;
            biochi_capture(biochi_k).y = biochi_y;
            biochi_capture(biochi_k).csv_file = biochi_csv;
        end
    end
end

biochi_summary = struct();
biochi_summary.schema_version = '0.1';
biochi_summary.audit_type = 'authors_native_plot_output_capture';
biochi_summary.figure_count = double(numel(biochi_figs));
biochi_summary.numeric_line_count = double(numel(biochi_capture));
biochi_summary.chi_bio_constructed = false;
biochi_summary.scientific_endpoint_opened = false;
biochi_summary.capture_basis = 'all numeric line objects produced by the authors published driver after the frozen one-line MATLAB API repair';
biochi_summary.interpretation_limit = 'Capture only. No line is promoted, no damping class is assigned, and no scalar or modal Bio Chi quantity is computed.';

biochi_fid = fopen(fullfile(biochi_out_dir,'capture_summary.json'),'w');
fwrite(biochi_fid,jsonencode(biochi_summary,'PrettyPrint',true),'char');
fclose(biochi_fid);
save(fullfile(biochi_out_dir,'native_plot_capture.mat'),'biochi_capture','biochi_summary','-v7');

disp(biochi_summary);
disp('BIO_CHI_JARUS_NATIVE_PLOT_CAPTURE_END');
diary off;

if isempty(biochi_capture)
    error('BIO_CHI_JARUS_NATIVE_PLOT_CAPTURE_NO_NUMERIC_LINES');
end
