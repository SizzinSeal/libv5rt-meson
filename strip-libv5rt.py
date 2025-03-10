import argparse
import os
import shutil
import subprocess
import sys
import tempfile

def main():
    parser = argparse.ArgumentParser(description='Strip symbols and sections from a static library.')
    parser.add_argument('-N', action='append', default=[], dest='symbols', help='Symbol to strip')
    parser.add_argument('-R', action='append', default=[], dest='sections', help='Section to remove')
    
    # Parse known arguments first
    args, remaining = parser.parse_known_args()
    
    # Verify remaining arguments contain input and output directory
    if len(remaining) != 2:
        print("Error: Expected format: [OPTIONS] INPUT_FILE OUTPUT_DIR", file=sys.stderr)
        print("       OUTPUT_DIR must be the last argument", file=sys.stderr)
        sys.exit(1)
    
    input_file, output_dir = remaining
    symbols = args.symbols
    sections = args.sections

    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Generate output filename
    input_basename = os.path.basename(input_file)
    stem, ext = os.path.splitext(input_basename)
    output_filename = f"{stem}-stripped{ext}"
    output_path = os.path.join(output_dir, output_filename)

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_archive = os.path.join(temp_dir, os.path.basename(input_file))
        shutil.copy2(input_file, temp_archive)

        try:
            subprocess.run(['ar', 'x', os.path.basename(temp_archive)], 
                          cwd=temp_dir, check=True)
        except subprocess.CalledProcessError:
            print(f"Error: Failed to extract archive '{input_file}'", file=sys.stderr)
            sys.exit(1)

        members = [f for f in os.listdir(temp_dir) if f != os.path.basename(temp_archive)]
        processed_files = []

        for member in members:
            member_path = os.path.join(temp_dir, member)
            if not os.path.isfile(member_path):
                continue

            # ELF file check
            try:
                with open(member_path, 'rb') as f:
                    if f.read(4) == b'\x7fELF':
                        cmd = ['objcopy']
                        cmd += [arg for symbol in symbols for arg in ('--strip-symbol', symbol)]
                        cmd += [arg for section in sections for arg in ('--remove-section', section)]
                        cmd.append(member_path)
                        subprocess.run(cmd, check=True)
            except (IOError, subprocess.CalledProcessError) as e:
                print(f"Error processing {member}: {e}", file=sys.stderr)
                sys.exit(1)

            processed_files.append(member)

        try:
            if members:
                subprocess.run(['ar', 'd', os.path.basename(temp_archive)] + members,
                             cwd=temp_dir, check=True)
            if processed_files:
                subprocess.run(['ar', 'r', os.path.basename(temp_archive)] + processed_files,
                             cwd=temp_dir, check=True)
            shutil.copy2(temp_archive, output_path)
        except (subprocess.CalledProcessError, OSError) as e:
            print(f"Error rebuilding archive: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()