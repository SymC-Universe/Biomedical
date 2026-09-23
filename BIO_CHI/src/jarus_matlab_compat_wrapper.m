% Bio Chi P0-D compatibility-source execution wrapper.
% The immutable published source remains preserved separately. This wrapper
% executes only the fail-closed one-line solver-call repair documented in
% compatibility_patch.json. No chi_bio quantity is constructed here.

set(groot,'defaultFigureVisible','off');
this_file = mfilename('fullpath');
src_dir = fileparts(this_file);
bio_dir = fileparts(src_dir);
out_dir = fullfile(bio_dir,'artifacts','generated','jarus_matlab_compat');
base_dir = fullfile(out_dir,'source','S1_Codes','MATLAB files','Reduced2023');

assert(isfile(fullfile(base_dir,'reduced.m')));
assert(isfile(fullfile(base_dir,'run_simulate_reduced.m')));
assert(isfile(fullfile(base_dir,'simulate_reduced.m')));
assert(isfile(fullfile(out_dir,'compatibility_patch.json')));

cd(base_dir);
addpath(base_dir);
diary(fullfile(out_dir,'matlab_stdout.txt'));
disp('BIO_CHI_JARUS_MATLAB_COMPAT_BEGIN');
disp(version);
run('run_simulate_reduced.m');
disp('BIO_CHI_JARUS_MATLAB_COMPAT_END');
whos;
save(fullfile(out_dir,'compat_workspace.mat'),'-v7');
diary off;
