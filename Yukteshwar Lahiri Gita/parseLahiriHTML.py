import os
import csv
import re
from bs4 import BeautifulSoup


def extract_chapter_number(html_file):
    with open(html_file, "r") as file:
        contents = file.read()

    soup = BeautifulSoup(contents, "html.parser")
    chapter_tag = soup.find("h1")
    if chapter_tag:
        chapter_number_match = re.search(r"CHAPTER\s(\d+)", chapter_tag.get_text())
        if chapter_number_match:
            return chapter_number_match.group(1)

    return None


def split_html_to_csv(html_file, csv_file):
    with open(html_file, "r") as file:
        contents = file.read()

    soup = BeautifulSoup(contents, "html.parser")
    rows = []

    pattern = re.compile(r"-\s\d+-$")

    for tag in soup.find_all("p"):
        text = tag.get_text().strip()
        is_verse = bool(re.search(pattern, text))

        if is_verse:
            rows.append([text, ""])
        else:
            if rows:
                rows[-1][1] += text

    with open(csv_file, "wb") as file:
        writer = csv.writer(file)
        writer.writerow([s.encode("utf-8") for s in ["Verse", "Commentary"]])
        for row in rows:
            writer.writerow(
                [s.encode("utf-8") if isinstance(s, unicode) else s for s in row]
            )


def create_chapter_csv(csv_file, chapter_number):
    with open(csv_file, "r") as file:
        reader = csv.reader(file)
        verse_commentary_lines = list(reader)

    with open(
        "./output/{}/Chapter{}{}.csv".format(author, chapter_number, author), "wb"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(
            [s.encode("utf-8") for s in ["Verse Number", "Translation", "Commentary"]]
        )

        verse_line = ""
        verse_number = ""
        for line in verse_commentary_lines:
            verse_number_match = re.search(r"-\s\d+-$", line[0])
            if verse_number_match:
                if verse_line:
                    writer.writerow(
                        [
                            verse_number.encode("utf-8"),
                            verse_line
                            if isinstance(verse_line, str)
                            else verse_line.encode("utf-8"),
                            line[1],
                        ]
                    )

                verse_number = verse_number_match.group().strip(" -")
                verse_line = line[0].rstrip("- {}-".format(verse_number)).strip()


author = "Lahiri"
directory = "./HTML files/{}/".format(author)

for fileName in os.listdir(directory):
    if fileName.endswith(".html"):
        html_file = os.path.join(directory, fileName)
        csv_file = "verse_sections_{}.csv".format(os.path.splitext(fileName)[0])
        chapter_number = extract_chapter_number(html_file)
        print(chapter_number)
        if chapter_number is not None:
            split_html_to_csv(html_file, csv_file)
            create_chapter_csv(csv_file, chapter_number)
