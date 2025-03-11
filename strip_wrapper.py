import sys
import subprocess
from pathlib import Path

def main():
    # Parse arguments
    strip_exe = sys.argv[1]
    input_lib = Path(sys.argv[2])
    options_file = Path(sys.argv[3])
    output1 = Path(sys.argv[4])
    output2 = Path(sys.argv[5])

    # Read strip options from file
    with options_file.open() as f:
        strip_options = f.read().strip()

    # Create output directories if needed
    output1.parent.mkdir(parents=True, exist_ok=True)
    output2.parent.mkdir(parents=True, exist_ok=True)

    # Run strip command
    subprocess.run(
        [strip_exe] + strip_options.split() + [str(input_lib), '-o', str(output1)],
        check=True
    )

    # Copy to second location
    if output1 != output2:
        output1.rename(output2)

if __name__ == '__main__':
    main()