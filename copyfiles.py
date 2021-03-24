import os
import shutil

SOURCE_DIR_NAME = "Path/to/copy/from"
COPYTO_DIR_NAME = "Path/to/copy/to"

def get_listdir(mypath):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(mypath):
        f.extend(filenames)
        break
    return f

def copyto(from_path, to_path):
    name_lst = sorted(get_listdir(from_path), reverse=False)
    for f in name_lst:
        full_name = os.path.join(from_path, f)
        shutil.copy(full_name, to_path)
        print(full_name)

if __name__ == "__main__":
    copyto(SOURCE_DIR_NAME, COPYTO_DIR_NAME)
