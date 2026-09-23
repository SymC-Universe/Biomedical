% Bio Chi P0-D native-source execution wrapper.
% This wrapper does not modify the published Jaruszewicz-Blońska source.

set(groot,'defaultFigureVisible','off');
this_file = mfilename('fullpath');
src_dir = fileparts(this_file);
bio_dir = fileparts(src_dir);
out_dir = fullfile(bio_dir,'artifacts','generated','jarus_matlab_native');
base_dir = fullfile(out_dir,'source','S1_Codes','MATLAB files','Reduced2023');

assert(isfile(fullfile(base_dir,'reduced.m')));
assert(isfile(fullfile(base_dir,'run_simulate_reduced.m')));
assert(isfile(fullfile(base_dir,'simulate_reduced.m')));

cd(base_dir);
addpath(base_dir);
diary(fullfile(out_dir,'matlab_stdout.txt'));
disp('BIO_CHI_JARUS_MATLAB_NATIVE_BEGIN');
disp(version);
run('run_simulate_reduced.m');
disp('BIO_CHI_JARUS_MATLAB_NATIVE_END');
whos;
save(fullfile(out_dir,'native_workspace.mat'),'-v7');
diary off;
