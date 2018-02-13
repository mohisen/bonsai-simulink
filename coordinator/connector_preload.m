pythonpath = getenv('PYTHONPATH');
if not(size(regexp(pythonpath, ':../../coordinator$'), 1))
    disp('Adding ../../coordinator to PYTHONPATH');
    setenv('PYTHONPATH', [pythonpath ':../../coordinator'])
end
