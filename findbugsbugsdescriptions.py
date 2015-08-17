from bs4 import BeautifulSoup
import re

soup = BeautifulSoup(open("FindBugsBugDescriptions.html"), 'html.parser')

def clean_html(html):
    encoded_str = html.encode("utf8")
    text = re.sub(' +', ' ', encoded_str)
    text = re.sub('\n', '', text).lstrip()
    return text

def get_description(code):
    a_tag = soup.find_all(attrs={"name" : code})[0]

    desc = a_tag.parent.findNext('p').contents[0]

    title = a_tag.contents[0]

    return clean_html(title), clean_html(desc)


if __name__ == "__main__":
    print get_description('EI_EXPOSE_REP2')