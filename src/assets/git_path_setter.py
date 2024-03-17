import os
import sys
from git import Repo

def add_src_subdirs_to_path():
    # Find the root directory of the git repository
    repo = Repo('.', search_parent_directories=True)
    repo_root = repo.git.rev_parse("--show-toplevel")

    src_path = os.path.join(repo_root, 'src')
    # Add src directory to the path
    if os.path.isdir(src_path) and src_path not in sys.path:
        sys.path.append(src_path)
        # print(f"Added to path: {src_path}")

    # Add immediate subdirectories of src to the path
    for item in os.listdir(src_path):
        item_path = os.path.join(src_path, item)
        if os.path.isdir(item_path) and item_path not in sys.path:
            sys.path.append(item_path)
            print(f"Added to path: {item_path}")

# Call the function
if __name__ == "__main__":
    add_src_subdirs_to_path()

    # Now you can import your modules located in any subdirectories under src
    # For example, if you have a module at src/subdir/mymodule.py, you can import it using
    # from mymodule import MyClass
