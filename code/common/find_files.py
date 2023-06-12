import os


def find_files(root_dir, target_filename):
    result = {}

    # iterate over all directories and subdirectories in root_dir
    for dirpath, _, filenames in os.walk(root_dir):

        # iterate over all filenames in the current directory
        for filename in filenames:

            # if the current filename is the target filename
            if filename == target_filename:
                # split the directory path into parts
                parts = dirpath.split(os.sep)

                # take the last part as the experiment date
                exp_date = parts[-1]

                # build the result entry
                result[exp_date] = os.path.join(dirpath, filename)

    result = dict(sorted(result.items(), key=lambda x: x[1]))

    return result
