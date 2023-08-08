import re

text = "/pressa/photoreports/photoreport/8649019.htm"

match = re.search(r"\d+", text)
print(match[0])