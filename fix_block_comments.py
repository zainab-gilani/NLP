import re
import os

BLOCK_MARKERS = ['endif', 'endfor', 'endwhile', 'enddef', 'endclass', 'endtry', 'endwith', 'endelse', 'endcase']

def fix_block_comments_in_file(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        fixed = line
        for marker in BLOCK_MARKERS:
            pattern = r'^(\s*)# ' + marker + r'\b'
            repl = r'\1#' + marker
            fixed = re.sub(pattern, repl, fixed)
        new_lines.append(fixed)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Fixed block comments in {filepath}")

def fix_all_py_files_in_folder(folder: str):
    for filename in os.listdir(folder):
        if filename.endswith('.py'):
            fix_block_comments_in_file(os.path.join(folder, filename))

# USAGE EXAMPLE:
# Change '.' to your folder path if needed
fix_all_py_files_in_folder('.')