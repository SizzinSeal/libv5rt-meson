import urllib.request
import urllib.error
import sys
import os
import zipfile
import hashlib
import re

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


def extract_zip(zip_path):
    # Check if the zip file exists
    if not os.path.exists(zip_path):
        print(f"Error: The file '{zip_path}' does not exist.")
        return False

    # Get script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create extraction directory name based on zip filename
    zip_basename = os.path.basename(zip_path)
    dir_name = os.path.splitext(zip_basename)[0]

    try:
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall()
        print(f"{zip_path} successfully extracted")
        return True

    except zipfile.BadZipFile:
        print(f"Error: '{zip_path}' is not a valid zip file.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    return False

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

def patch_header(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Regular expression to find function declarations/definitions
    # This regex looks for closing parenthesis of function parameters followed by attributes and termination
    pattern = re.compile(
        r'\)(\s*)((?:__attribute__\s*\(\([^)]*\)\)\s*)*)(\s*)(;|\{)',
        re.DOTALL
    )
    
    def replacer(match):
        whitespace_after_paren = match.group(1)
        existing_attrs = match.group(2)
        whitespace_after_attrs = match.group(3)
        ending = match.group(4)
        
        # Check if 'pcs("aapcs")' is already present
        if 'pcs("aapcs")' in existing_attrs:
            return match.group(0)
        
        new_attr = ' __attribute__((pcs("aapcs")))'
        new_part = f'){whitespace_after_paren}{new_attr}'
        
        # Add existing attributes if present
        if existing_attrs:
            new_part += f' {existing_attrs}'
        
        # Add remaining whitespace and ending
        new_part += f'{whitespace_after_attrs}{ending}'
        
        return new_part
    
    # Substitute all occurrences
    modified_content = pattern.sub(replacer, content)
    
    # Write the output file
    with open(output_file, 'w') as f:
        f.write(modified_content)


def main():
    # Check minimum arguments (version + hash)
    if len(sys.argv) < 3:
        print("Error: Invalid number of arguments")
        print(f"Usage: {sys.argv[0]} version_str hash_str [filename1 filename2 ...]")
        sys.exit(1)

    # get version and hash
    version = sys.argv[1]
    hash = sys.argv[2]
    filenames = sys.argv[3:]
    path_prefix = os.path.join(version, "vexv5")

    # get files
    headers = [] # list of headers to keep
    object_files = [] # list of object files to keep
    for filename in filenames:
        if filename.endswith('.c.obj'):
            object_files.append(filename)
        elif filename.endswith('.h'):
            headers.append(os.path.join(path_prefix, 'include', filename))
    
    # download the zip
    zip = download_zip(version)
    if zip == None:
        sys.exit(1)
    
    # check the hash
    if calculate_sha256(zip) != hash:
        os.remove(zip)
        print(f"hashes don't match! try again!")
        sys.exit(1)

    # extract the zip
    if extract_zip(zip) == False:
        sys.exit(1)
    
    # patch headers
    try:
        os.makedirs(name="include", exist_ok=True)
    except:
        print("failed to path header files: could not create include directory")
        sys.exit(1)
    for header in headers:
        patch_header(header, os.path.join("include", os.path.basename(header)))


if __name__ == "__main__":
    main()