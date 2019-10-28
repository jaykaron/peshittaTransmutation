import bs4
import os
import requests
"""
A script for downloading the peshitta old testament files from http://cal.huc.edu/.
Files were downloaded with permission.
Files are written to the 'raw' directory.
"""

url = "http://cal.huc.edu/get_a_chapter.php"
p_ids = range(62001, 62039 + 1)

for id in p_ids:
    parameters = {"cset":"U", "file": id}
    response = requests.get(url, params=parameters)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    title = soup.find("a", target="info").text
    text = soup.find("div",align="right").find("table").text

    bookname = title.strip().split()[-1]
    file_path = os.path.join("raw", bookname + ".txt")
    with open(file_path, "w") as f:
        f.write(text)
