import os
import xml.etree.ElementTree as ET
from github import Github
from mapdiff import *
from findbugsbugsdescriptions import *

K = "f0cb04f911da0a3211f16a451c0fc47acc1bd52a"

env_commit = os.environ.get('TRAVIS_COMMIT')
env_pull = os.environ.get('TRAVIS_PULL_REQUEST')

print env_commit, env_pull


def test_pull_apis():
    env_pull = 62

    g = Github(K[::-1])
    repo = g.get_repo("dariusf/issues")

    pull = repo.get_pull(env_pull)

    print pull.title
    print pull.body
    # Base commit
    print pull.base.sha

    pull.create_issue_comment("Test create_issue_comment")


def comment_bugs_on_github(sha=None):

    g = Github(K[::-1])
    repo = g.get_repo("dariusf/issues")

    if not sha:
        sha = current_head()

    commit = repo.get_commit(sha)

    comment_data = get_comments_from_XML()

    print "Repo:", repo.name
    print "Repo URL:", repo.html_url
    print "Commit message:", commit.commit.message

    # Add prefix to source file names
    prefix = 'src/main/java/'
    for e in comment_data:
        e[0] = prefix + e[0]

    files = git_diff_files(sha + '^', sha)
    comments_to_make = [c for c in comment_data if c[0] in files]

    for c in comments_to_make:
        src = c[0]
        diff_line = int(c[1])
        category = c[2]
        _type = c[3]

        comment = get_description(_type)

        pos = get_unified_diff_line(git_diff(sha + '^', sha, src), diff_line)
        if pos is not None:
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
            category = bug_instance.attrib['category']
            bugType = bug_instance.attrib['type']
            srcFile = ""
            srcLine = -1
            
            for attr in bug_instance:

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


    return comments_on_line

if __name__ == "__main__":
    # Test pull request APIs
    test_pull_apis()

