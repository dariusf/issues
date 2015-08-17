import xml.etree.ElementTree as ET
from github import Github

K = "f0cb04f911da0a3211f16a451c0fc47acc1bd52a"

def testGithubComment():
	g = Github(K[::-1])
	repo = g.get_repo("dariusf/issues")

	print "Repo:", repo.name
	print "Repo URL:", repo.html_url

	allCommits = repo.get_commits()

	# HEAD commit i think
	commit = allCommits[0]
	print "Commit message:", allCommits[0].commit.message


	# Test comment
	body = "HELLO WORLD"
	position = 1
	path = "mapdiff.py"

	commit.create_comment(body=body, path=path, position=position)


def getCommentsFromXML():

	# Parse this xml file
	tree = ET.parse('build/reports/findbugs/main.xml')
	root = tree.getroot()

	commentsOnLine = []
	generalComments = []

	for bugInstance in root:
		if bugInstance.tag == "BugInstance":
			#print "---"
			#print bugInstance.tag, bugInstance.attrib
			#print bugInstance.attrib['category']
			#print bugInstance.attrib['type']

			category = bugInstance.attrib['category']
			bugType = bugInstance.attrib['type']
			srcFile = ""
			srcLine = -1
			
			for attr in bugInstance:
				#print attr.tag, attr.attrib
				if attr.tag == "SourceLine":
					srcFile = attr.attrib['sourcepath']
					srcLine = attr.attrib['start']
					break

			if srcFile != "" and srcLine != -1:
				comment = [srcFile, srcLine, category, bugType]
				commentsOnLine.append(comment)
			else:
				comment = [category, bugType]
				generalComments.append(comment)

	#print commentsOnLine
	#print generalComments

	return commentsOnLine


# Uncomment to comment
#testGithubComment()

# Parses XML
print getCommentsFromXML()