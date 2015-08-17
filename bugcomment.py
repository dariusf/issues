import xml.etree.ElementTree as ET
from github import Github

from mapdiff import *
from findbugsbugsdescriptions import *

K = "f0cb04f911da0a3211f16a451c0fc47acc1bd52a"


def comment_bugs_on_github(sha=None):

    g = Github(K[::-1])
    repo = g.get_repo("dariusf/issues")

    if not sha:
        sha = repo.get_commits()[0].sha

    commit = repo.get_commit(sha)

    comment_data = get_comments_from_XML()

    print "Repo:", repo.name
    print "Repo URL:", repo.html_url
    print "Commit message:", commit.commit.message

    # Add prefix to source file names
    prefix = 'src/main/java/'
    for e in comment_data:
        e[0] = prefix + e[0]

    # -----
    files = git_diff_files(sha + '^', sha)
    comments_to_make = [c for c in comment_data if c[0] in files]

    for c in comments_to_make:
        src = c[0]
        diff_line = int(c[1])
        category = c[2]
        _type = c[3]

        title, description = get_description(_type)

        comment = "["+category + "] : " + title + "\n" + description

        pos = get_unified_diff_line(git_diff(sha + '^', sha, src), diff_line)
        print "Comment '%s' on diff line %d of %s" % (comment, pos, src)

        commit.create_comment(body=comment, path=src, position=pos)


def test_github_comment():
    g = Github(K[::-1])
    repo = g.get_repo("dariusf/issues")

    print "Repo:", repo.name
    print "Repo URL:", repo.html_url

    all_commits = repo.get_commits()

    # HEAD commit i think
    commit = all_commits[0]
    print "Commit message:", all_commits[0].commit.message


    # Test comment
    body = "HELLO WORLD comment on pos 0"
    position = 0
    path = "mapdiff.py"

    commit.create_comment(body=body, path=path, position=position)


def get_comments_from_XML():

    # Parse this xml file
    tree = ET.parse('build/reports/findbugs/main.xml')
    root = tree.getroot()

    comments_on_line = []
    general_comments = []

    for bug_instance in root:
        if bug_instance.tag == "BugInstance":
            #print "---"
            #print bug_instance.tag, bug_instance.attrib
            #print bug_instance.attrib['category']
            #print bug_instance.attrib['type']

            category = bug_instance.attrib['category']
            bugType = bug_instance.attrib['type']
            srcFile = ""
            srcLine = -1
            
            for attr in bug_instance:
                #print attr.tag, attr.attrib
                if attr.tag == "SourceLine":
                    srcFile = attr.attrib['sourcepath']
                    srcLine = attr.attrib['start']
                    break

            if srcFile != "" and srcLine != -1:
                comment = [srcFile, srcLine, category, bugType]
                comments_on_line.append(comment)
            else:
                comment = [category, bugType]
                general_comments.append(comment)

    #print comments_on_line
    #print general_comments

    return comments_on_line

if __name__ == "__main__":
    # Uncomment to comment
    #test_github_comment()

    # Parses XML
    #print get_comments_from_XML()

    comment_bugs_on_github()
