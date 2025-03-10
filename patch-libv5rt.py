import sys
import os
import subprocess
import tempfile

def strip_object_files(keep):
    lib = os.path.join("libv5rt", "vexv5", "libv5rt.a")
    ar = 'arm-none-eabi-ar'

    def list_objects(library):
        """Return a list of object files in the static library using 'ar t'."""
        try:
            output = subprocess.check_output([ar, "t", library], universal_newlines=True)
        except subprocess.CalledProcessError as e:
            print(f"Error listing objects in {library}: {e}")
            sys.exit(1)
        return output.splitlines()

    def extract_objects(library, objects, extract_dir):
        """Extract specified objects from the library into extract_dir."""
        abs_library = os.path.abspath(library)  # Compute the absolute path BEFORE changing directory
        orig_dir = os.getcwd()
        os.chdir(extract_dir)
        try:
            for obj in objects:
                try:
                    subprocess.check_call([ar, "x", abs_library, obj])
                except subprocess.CalledProcessError as e:
                    print(f"Error extracting object {obj} from {library}: {e}")
                    sys.exit(1)
        finally:
            os.chdir(orig_dir)

    def create_new_library(output_library, object_files, working_dir):
        """Create a new static library with the given object files."""
        files = [os.path.join(working_dir, obj) for obj in object_files]
        try:
            subprocess.check_call([ar, "rcs", output_library] + files)
        except subprocess.CalledProcessError as e:
            print(f"Error creating new library {output_library}: {e}")
            sys.exit(1)

    if not os.path.isfile(lib):
        print(f"Library file {lib} does not exist.")
        sys.exit(1)

    all_objects = list_objects(lib)
    if not all_objects:
        print("No object files found in the library.")
        sys.exit(1)

    # Identify objects from the preserve list that are present in the library.
    objects_to_extract = [obj for obj in keep if obj in all_objects]
    if not objects_to_extract:
        print("None of the specified object files were found in the library.")
        sys.exit(1)

    # Use a temporary directory to extract and process objects.
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Extracting objects to temporary directory: {tmpdir}")
        extract_objects(lib, objects_to_extract, tmpdir)
        new_lib_path = os.path.relpath('libv5.a')
        print(f"Creating new library: {new_lib_path}")
        create_new_library(new_lib_path, objects_to_extract, tmpdir)

def main():
    # get compiler tools to use
    files = sys.argv[1:]

    # create library
    strip_object_files(files)
    
    # we're done
    sys.exit(0)

if __name__ == "__main__":
    main()