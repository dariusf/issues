
import re
import os
from subprocess import Popen, PIPE

# http://stackoverflow.com/a/24456418

def git_diff(commit_start, commit_end, for_file=None):
    if for_file:
        args = ['git', 'diff', commit_start, commit_end, for_file]
    else:
        args = ['git', 'diff', commit_start, commit_end]
    process = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if not stderr:
        return stdout
    else:
        raise RuntimeError('Cannot get `git diff` output')

def git_diff_files(commit_start, commit_end):
    process = Popen(['git', 'diff', '--name-only', commit_start, commit_end], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    if not stderr:
        return [l for l in stdout.split('\n') if l.strip()]
    else:
        raise RuntimeError('Cannot get `git diff --name-only` output')

def get_unified_diff_line(file_diff, file_line):
    """
    Should only be used on single file diffs
    """
    lines = file_diff.split('\n')

    diff_start = 0
    for line in lines:
        if line.startswith('@@'):
            break
        diff_start += 1

    diff_lines = lines[diff_start:]
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

# -----

# This is the commit 'Added a few violations', which introduces problems in Main.java
sha_from = 'f1e3a2f'
sha_to = 'b91cc3c'

prefix = 'src/main/java/'

example_data = [
    ['Main.java', '14', 'MALICIOUS_CODE', 'EI_EXPOSE_REP2'],
    ['Main.java', '14', 'PERFORMANCE', 'URF_UNREAD_FIELD'],
    ['expr/Or.java', '17', 'BAD_PRACTICE', 'EQ_CHECK_FOR_OPERAND_NOT_COMPATIBLE_WITH_THIS']
]

for e in example_data:
    e[0] = prefix + e[0]

# -----

files = git_diff_files(sha_from, sha_to)

comments_to_make = [c for c in example_data if c[0] in files]

for c in comments_to_make:
    result = get_unified_diff_line(git_diff(sha_from, sha_to, c[0]), int(c[1]))
    print "Comment '%s' on diff line %d of %s" % (c[2] + ': ' + c[3], result, c[0])

# -----

# 'Tests'

# print get_unified_diff_line(git_diff('05cc3fc', 'cf088b8'), 43) # 6
# print get_unified_diff_line(git_diff('b91cc3c', 'c7df16a'), 6) # 8
# print get_unified_diff_line(git_diff('cf088b8', 'e3e123f'), 6) # 6