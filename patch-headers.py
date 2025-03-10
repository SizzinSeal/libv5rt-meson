import re
import sys
import os

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
    # get headers to patch
    files = sys.argv[3:]

    # patch headers
    print("patching headers")
    for file in files:
        try:
            patch_header(os.path.join("libv5rt", "vexv5", "include", os.path.basename(file)))
        except:
            print(f"failed patching {file}!")
            sys.exit(1)
    
    # we're done
    sys.exit(0)

if __name__ == "__main__":
    main()