# import required libraries
import subprocess
from os.path import isfile, join, isdir
from os import listdir, walk, remove, getenv, mkdir


def grid_file_to_12km_rcm(file):
    """
    Take a file and re-grid to the 12Km RCM grid
    """

    # get just the name of the file (remove the extension)
    file_name = file.split('/')[-1]
    file_name = file_name.split('.')[0]

    # re-grid to the 12km RCM grid, save as virtual raster in the temp directory
    subprocess.run(["gdalwarp", "-te", "0", "12000", "660000", "1212000", "-tr", "12000", "12000", "-r", "sum",
                    file,
                    join(data_path, temp_directory, '%s-%s.vrt' % (file_name, 'temp'))])

    # save the virtual raster as an .asc in the output directory
    subprocess.run(
        ["gdal_translate", "-of", "AAIGrid", join(data_path, temp_directory, "%s-%s.vrt" % (file_name, 'temp')),
         join(data_path, outputs_directory, "%s-12km-sum.asc" % file_name)])

    return


def search_for_files(base_search_path):
    """
    Search for files in directory and subdirectories.

    Return None is no file found.
    """
    files = []  # set in case no file is passed
    extensions = ['asc','']
    for extension in extensions:

        for dirpath, dirnames, filenames in walk(base_search_path):
            for filename in [f for f in filenames if f.endswith(".%s" %extension)]:
                files.append(join(dirpath, filename))

    return files


## set paths
# set data path and directory names
data_path = '/data'
inputs_directory = 'inputs'
input_data_directory = 'layers'
temp_directory = 'temp'
outputs_directory = 'outputs'

# check if required folder structure in place
# if so and folders have files in, empty
## temp
if isdir(join(data_path, temp_directory)) is False:
    mkdir(join(data_path, temp_directory))
else:
    files = [f for f in listdir(join(data_path, temp_directory)) if isfile(join(data_path, temp_directory,f))]
    for file in files:
        remove(join(data_path, temp_directory,file))

## outputs
if isdir(join(data_path, outputs_directory)) is False:
    mkdir(join(data_path, outputs_directory))

# empty output dir
files = [f for f in listdir(join(data_path, outputs_directory)) if isfile(join(data_path, outputs_directory,f))]
for file in files:
    remove(join(data_path, outputs_directory,file))


## start the processing
# get list of input files to loop through
files = search_for_files(join(data_path, inputs_directory))
print('Files to loop through: %s' %files)

# loop through the files and re-grid
for file in files:
    print('Processing file:', file)
    grid_file_to_12km_rcm(file)

