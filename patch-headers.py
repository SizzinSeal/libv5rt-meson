import re
import sys
import os

def patch_header(input_file, output_file):
    # Read the input file
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Modify #include directives to include _patched before the extension
    # Only modify if the file name starts with "v5_"
    include_pattern = re.compile(r'(#include\s+")([^"]+)(")')
    def include_replacer(match):
        filename = match.group(2)
        if not filename.startswith("v5_"):
            return match.group(0)
        base, ext = os.path.splitext(filename)
        return f'{match.group(1)}{base}_patched{ext}{match.group(3)}'
    
    content = include_pattern.sub(include_replacer, content)
    
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
    
    # Substitute all occurrences for function declarations/definitions
    modified_content = pattern.sub(replacer, content)
    
    # Write the output file
    dir_name = os.path.dirname(output_file)
    if dir_name != '':
        os.makedirs(dir_name, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(modified_content)

def append_patched_to_filename(file_path: str) -> str:
    base, ext = os.path.splitext(file_path)
    return f"{base}_patched{ext}"

def main():
    # get headers to patch
    files = sys.argv[3:-1]
    # get output directory
    out_dir = sys.argv[-1]

    # patch headers
    print("patching headers")
    for file in files:
        name = os.path.join(out_dir, os.path.basename(file))
        new_name = os.path.basename(append_patched_to_filename(name))
        patch_header(name, new_name)
    
    # we're done
    sys.exit(0)

if __name__ == "__main__":
    main()
