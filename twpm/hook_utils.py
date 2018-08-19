import glob
import imp
import os


def find_hooks(file_prefix):
    # Find all files in subdirectories whose names start with <file_prefix>
    file_pattern = '/Users/kevin.fong/build/taskpirate/taskpirate' + '/*/' + \
                   file_prefix + "*.py"
    module_paths = [f for f in glob.glob(file_pattern) if os.path.isfile(f)]
    module_paths.sort()

    # Gather all hooks in these files
    hooks = []

    for module_path in module_paths:
        # Load the module
        module_dir = os.path.dirname(module_path)
        module_filename = os.path.basename(module_path)
        module_name = 'pirate_{0}_{1}'.format(module_dir, module_filename)
        module_name = module_name.replace('.', '_')
        module = imp.load_source(module_name, module_path)

        # Find all hook methods available
        module_hooks = [
            getattr(module, hook_name)
            for hook_name in dir(module)
            if hook_name.startswith('hook_')
        ]

        hooks += module_hooks

    return hooks
