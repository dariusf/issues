
import re
from subprocess import Popen, PIPE

def git_diff(commit_start, commit_end):
    process = Popen(['git', 'diff', commit_start, commit_end], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if not stderr:
        return stdout
    else:
        raise RuntimeError('Cannot get `git diff` output')

def get_unified_diff_line(diff, file_line):
    lines = diff.split('\n')
    diff_lines = lines[4:]
    diff_lines_without_header = diff_lines[1:]

    new_file_info = re.search(r'\+(\d+),(\d+)', diff_lines[0])
    start = int(new_file_info.group(1))
    count = int(new_file_info.group(2))
    # new_file_content = [l for l in lines[5:] if re.match(r'^[^-]', l)]

    new_file_diff_line = file_line - start + 1

    remaining = new_file_diff_line
    minuses = 0

    # Count minuses until we run out of diff lines, then offset by that
    for line in diff_lines_without_header:
        if line.startswith('-'):
            minuses += 1
        else:
            remaining -= 1

        if remaining < 0:
            break
    return new_file_diff_line + minuses

print get_unified_diff_line(git_diff('HEAD^', 'HEAD'), 43)
print get_unified_diff_line(git_diff('HEAD^^^', 'HEAD^^'), 6)
