import urllib.request
import urllib.error
import sys
import os
import zipfile
import hashlib
import subprocess
import tempfile
import shutil

def download_zip(file_name):
    # Construct the URL using the version passed (in its original format).
    url = f"https://content.vexrobotics.com/vexos/public/V5/vscode/sdk/cpp/{file_name}.zip"
    print(f"Downloading from: {url}")

    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36")
    }
    req = urllib.request.Request(url, headers=headers)

    zip_filename = f"{file_name}.zip"
    try:
        with urllib.request.urlopen(req) as response:
            with open(zip_filename, "wb") as out_file:
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    out_file.write(chunk)
    except urllib.error.URLError:
        print(f"failed downloading libv5rt")
        return None

    return zip_filename


def calculate_sha256(filename):
    try:
        with open(filename, 'rb') as f:
            sha256 = hashlib.sha256()
            while True:
                chunk = f.read(4096)  # Read file in 4KB chunks
                if not chunk:
                    break
                sha256.update(chunk)
            return sha256.hexdigest()

    except FileNotFoundError:
        print(f"Error: The file '{filename}' does not exist.")
        return None
    except PermissionError:
        print(f"Error: Permission denied to read '{filename}'.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None


def copy_all_items(source_dir, target_dir):
    # Check if the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist.")
        sys.exit(1)
    
    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Iterate over each item in the source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)
        
        try:
            # If the item is a directory, use copytree (with dirs_exist_ok to allow merging)
            if os.path.isdir(source_path):
                shutil.copytree(source_path, target_path, dirs_exist_ok=True)
                print(f"Copied directory: {source_path} -> {target_path}")
            # If it's a file, use copy2 to preserve metadata
            elif os.path.isfile(source_path):
                shutil.copy2(source_path, target_path)
                print(f"Copied file: {source_path} -> {target_path}")
            else:
                print(f"Skipped non-file/directory: {source_path}")
        except Exception as e:
            print(f"Error copying {source_path} to {target_path}: {e}")
            sys.exit(1)


def extract_zip(zip_path):
    # Check if the zip file exists
    if not os.path.exists(zip_path):
        print(f"Error: The file '{zip_path}' does not exist.")
        return False

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(path=tmpdir)
            # create a new extraction dir with a consistent name
            new_dir = os.path.relpath('libv5rt')
            os.makedirs(new_dir, exist_ok=True)
            extraction_dir = os.path.splitext(os.path.basename(zip_path))[0]
            copy_all_items(os.path.join(tmpdir, extraction_dir), new_dir)
            print(f"libv5rt successfully extracted")
            return True

    except zipfile.BadZipFile:
        print(f"Error: '{zip_path}' is not a valid zip file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    return False


def main():
    # Check minimum arguments (version + hash)
    if len(sys.argv) < 3:
        print("Error: Invalid number of arguments")
        print(f"Usage: {sys.argv[0]} version_str hash_str [filename1 filename2 ...]")
        sys.exit(1)

    # get version and hash
    version = sys.argv[1]
    hash = sys.argv[2]
    
    # download the zip
    zip = download_zip(version)
    if zip == None:
        sys.exit(1)
    
    # check the hash
    if calculate_sha256(zip) != hash:
        print(f"failed to download libv5rt! hashes don't match! try recompiling? deleting archive...")
        os.remove(zip)
        sys.exit(1)

    # extract the zip
    if extract_zip(zip) == False:
        sys.exit(1)
    
    # we're done
    sys.exit(0)


if __name__ == "__main__":
    main()