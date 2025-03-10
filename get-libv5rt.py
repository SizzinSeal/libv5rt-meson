import urllib.request
import urllib.error
import sys
import os
import zipfile
import hashlib

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
    extract_dir = os.path.join(script_dir, dir_name)

    try:
        # Create extraction directory if it doesn't exist
        os.makedirs(extract_dir, exist_ok=True)
        
        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        
        print(f"Successfully extracted to: {extract_dir}")
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


def main():
    # Check minimum arguments (version + hash)
    if len(sys.argv) < 3:
        print("Error: Invalid number of arguments")
        print(f"Usage: {sys.argv[0]} version_str hash_str [filename1 filename2 ...]")
        sys.exit(1)

    # Parse arguments
    version_str = sys.argv[1]
    hash_str = sys.argv[2]
    filenames = sys.argv[3:]

    listA = []
    listB = []
    listC = []
    
    for filename in filenames:
        if filename.endswith('.c.obj'):
            listC.append(filename)
        elif filename.endswith('.a'):
            listA.append(filename)
        elif filename.endswith('.h'):
            listB.append(filename)
    
    print("listA =", listA)
    print("listB =", listB)
    print("listC =", listC)

    # Display results (replace this with your actual logic)
    print(f"Version: {version_str}")
    print(f"Hash: {hash_str}")
    print(f"Number of files: {len(filenames)}")
    for i, filename in enumerate(filenames, 1):
        print(f"File {i}: {filename}")


if __name__ == "__main__":
    main()