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

import os
import shutil
import tempfile
import zipfile

def extract_zip(zip_path, keep_files, out_dir):
    # Check if the zip file exists
    if not os.path.exists(zip_path):
        print(f"Error: The file '{zip_path}' does not exist.")
        return False

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            # Extract the zip file
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(path=tmpdir)
            
            extraction_dir = os.path.splitext(os.path.basename(zip_path))[0]
            vexv5_dir = os.path.join(tmpdir, extraction_dir, "vexv5")
            include_dir = os.path.join(vexv5_dir, "include")
            
            # Ensure the output directory exists
            os.makedirs(out_dir, exist_ok=True)
            
            # Copy each specified file from either vexv5 or include directories
            for file_name in keep_files:
                file_name = os.path.basename(file_name)
                found = False
                # Check in the vexv5 directory
                src_path = os.path.join(vexv5_dir, file_name)
                if os.path.exists(src_path):
                    dst_path = os.path.join(out_dir, file_name)
                    if os.path.isfile(src_path):
                        shutil.copy(src_path, dst_path)
                    else:
                        shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                    found = True
                else:
                    # Check in the include directory
                    src_path = os.path.join(include_dir, file_name)
                    if os.path.exists(src_path):
                        dst_path = os.path.join(out_dir, file_name)
                        if os.path.isfile(src_path):
                            shutil.copy(src_path, dst_path)
                        else:
                            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                        found = True
                if not found:
                    print(f"Error: File '{file_name}' not found in the extracted contents.")
                    return False
            
            print("libv5rt successfully extracted")
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

    # get files that need to be kept
    keep_files = sys.argv[3:-1]
    # get output directory
    out_dir = os.path.join("../", sys.argv[-1])
    
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
    if extract_zip(zip, keep_files, out_dir) == False:
        sys.exit(1)
    
    # we're done
    sys.exit(0)


if __name__ == "__main__":
    main()