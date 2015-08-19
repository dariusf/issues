from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open("FindBugsBugDescriptions.html"), 'html.parser')

def clean_html(html):
    encoded_str = html.encode("utf8")
    return re.sub(r'[\s]+', ' ', encoded_str).strip()

def format_title(title):
    print title
    match = re.match(r'[\w\d]+: ([^()]+) \(([^()]+)\)', title)
    header = match.group(1).strip()
    footer = match.group(2).strip()
    return header, footer

def get_description(code):
    a_tag = soup.find_all(attrs={"name": code})[0]

    desc = a_tag.parent.findNext('p').contents[0]
    title = a_tag.contents[0]
    header, footer = format_title(clean_html(title))

    return "### %s\n\n%s\n\n**%s**" % (header, clean_html(desc), footer)


if __name__ == "__main__":
    print get_description('ST_WRITE_TO_STATIC_FROM_INSTANCE_METHOD')
