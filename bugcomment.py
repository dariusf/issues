import os
import xml.etree.ElementTree as ET
from github import Github
from mapdiff import *
from findbugsbugsdescriptions import *

K = "f0cb04f911da0a3211f16a451c0fc47acc1bd52a"

SOURCE_FILE_PREFIX = 'src/main/java/'
FINDBUGS_XML = 'build/reports/findbugs/main.xml'
REPO_NAME = "dariusf/issues"
env_commit = None
env_pull_request_id = None
env_commit = os.environ.get('TRAVIS_COMMIT')
env_pull_request_id = os.environ.get('TRAVIS_PULL_REQUEST')

print env_commit, env_pull_request_id


def main():
    global env_pull_request_id

    # Login and get repo
    g = Github(K[::-1])
    repo = g.get_repo(REPO_NAME)    

    head_sha = current_head()
    base_sha = head_sha + '^'

    pull = None
    head_commit = None
    base_commit = None

    # Check if pull request or just a commit
    if env_pull_request_id is not None and env_pull_request_id != 'false':
        env_pull_request_id = int(env_pull_request_id)
        pull = repo.get_pull(env_pull_request_id)
        head_sha = pull.head.sha
        base_sha = pull.base.sha

    head_commit = repo.get_commit(head_sha)
    base_commit = repo.get_commit(base_sha)
    base_sha = base_commit.sha

    print 'head: ', head_sha
    print 'base: ', base_sha

    # We have the correct head and base now

    # Get comments
    comment_data = get_comments_from_XML()

    # Files to comment on
    files = git_diff_files(base_sha, head_sha)
    comments_to_make = [c for c in comment_data if c[0] in files]

    for c in comments_to_make:
        src = c[0]
        diff_line = int(c[1])
        category = c[2]
        _type = c[3]

        comment = get_description(_type)

        pos = get_unified_diff_line(git_diff(base_sha, head_sha, src), diff_line)
        if pos is not None:
            print "Comment '%s' on diff line %d of %s" % (comment, pos, src)
            commit.create_comment(body=comment, path=src, position=pos)



def test_pull_request_apis():

    # assert not isinstance(env_pull_request_id, basestring)

    # env_pull_request_id = int(env_pull_request_id)
    env_pull_request_id = 62

    g = Github(K[::-1])
    repo = g.get_repo(REPO_NAME)

    pull = repo.get_pull(env_pull_request_id)

    print pull.title
    print pull.body
    # Base commit
    print pull.base.sha

    head_sha = pull.head.sha

    print 'pr head:', pull.head.sha
    print 'current head: ', current_head()

    head_commit = repo.get_commit(head_sha)

    # pull.create_issue_comment("Test create_issue_comment")
    pull.create_review_comment(body='test comment on pr by travis',
                               commit_id=head_commit,
                               path='bugcomment.py',
                               position=4)


def comment_bugs_on_github(sha=None):

    g = Github(K[::-1])
    repo = g.get_repo(REPO_NAME)

    if not sha:
        sha = current_head()

    commit = repo.get_commit(sha)

    comment_data = get_comments_from_XML()

    print "Repo:", repo.name
    print "Repo URL:", repo.html_url
    print "Commit message:", commit.commit.message

    # -----
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
    repo = g.get_repo(REPO_NAME)

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
    tree = ET.parse(FINDBUGS_XML)
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
                comment = [SOURCE_FILE_PREFIX + srcFile, srcLine, category, bugType]
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

    # Test pull request APIs
    #test_pull_request_apis()

    #comment_bugs_on_github()

    main()

