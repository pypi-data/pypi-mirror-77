import os

from simses.constants_simses import ROOT_PATH


def count_loc(lines):
    nb_lines = 0
    docstring = False
    for line in lines:
        line = line.strip()

        if line == "" \
           or line.startswith("#") \
           or docstring and not (line.startswith('"""') or line.startswith("'''"))\
           or (line.startswith("'''") and line.endswith("'''") and len(line) > 3)  \
           or (line.startswith('"""') and line.endswith('"""') and len(line) > 3):
            continue

        # this is either a starting or ending docstring
        elif line.startswith('"""') or line.startswith("'''"):
            docstring = not docstring
            continue

        else:
            nb_lines += 1

    return nb_lines


def count_loc_in_directory(directory: str, ext: str, start: str = ''):
    loc = 0
    #print(directory)
    for item in os.listdir(directory):
        filename = os.path.join(directory, item)
        if os.path.isfile(filename) and filename.endswith(ext) and os.path.basename(filename).startswith(start):
            #print(filename)
            with open(filename, 'r') as file:
                try:
                    lines = file.readlines()
                    # count all lines
                    # loc += len(lines)
                    # count all lines except comments
                    loc += count_loc(lines)
                except UnicodeDecodeError:
                    print('Error in ' + filename)
        if os.path.isdir(filename):
            loc += count_loc_in_directory(filename, ext, start)
    return loc

loc_with_tests = count_loc_in_directory(ROOT_PATH, '.py', '')
loc_tests = count_loc_in_directory(ROOT_PATH, '.py', 'test_')
print('LOC: ' + str(loc_with_tests - loc_tests), 'LOC Tests: ' + str(loc_tests))
