import sys
import subprocess
from pathlib import Path
import os

def main():
    # Parse arguments
    strip_exe = sys.argv[1]
    input_lib = Path(sys.argv[2])
    options_file = Path(sys.argv[3])
    base_name = os.path.basename(sys.argv[4])
    output = os.path.join("../", sys.argv[5], base_name)

    # Read strip options from file
    with options_file.open() as f:
        strip_options = f.read().strip()

    # Run strip command
    subprocess.run(
        [strip_exe] + strip_options.split() + [str(input_lib), '-o', str(base_name)],
        check=True
    )

    # copy to second location
    subprocess.run(
        [strip_exe] + strip_options.split() + [str(input_lib), '-o', str(output)],
        check=True
   )

if __name__ == '__main__':
    main()