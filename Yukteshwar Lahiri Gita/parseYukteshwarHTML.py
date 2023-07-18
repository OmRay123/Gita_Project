import os
import re
from bs4 import BeautifulSoup
import unicodecsv as csv
from word2number import w2n


def get_html_content(file_name):
    with open(file_name, "r") as html_file:
        content = html_file.read()
    return content


def extract_chapter_number(html_file):
    with open(html_file, "r") as file:
        contents = file.read()

    soup = BeautifulSoup(contents, "html.parser")
    chapter_tag = soup.find("h1")
    if chapter_tag:
        chapter_number_match = " ".join(
            re.findall(r"CHAPTER\s(\w+)", chapter_tag.get_text())
        )
        if chapter_number_match:
            return w2n.word_to_num(str(chapter_number_match))

    return None


def extract_data(content):
    soup = BeautifulSoup(content, "html.parser")
    verses = soup.findAll("p")

    verses_data = []

    for verse in verses:
        verse_span = verse.find("span", {"class": "calibre16"})
        if verse_span:
            verse_data = []
            text = verse_span.text.strip()
            verse_numbers = re.findall(r"\s-\s*(\d+)\s*-?", text)
            verse_data.append(", ".join(verse_numbers))
            verse_data.append(text)

            next_sib = verse.find_next_sibling("p")
            if next_sib and next_sib.text.strip() == "Poetically:":
                translations = []
                while True:
                    next_sib = next_sib.find_next_sibling("p")
                    if (
                        next_sib
                        and next_sib.text.strip() != "Commentary:"
                        and not next_sib.find("span", {"class": "calibre16"})
                    ):
                        translations.append(next_sib.text.strip())
                    else:
                        break
                verse_data.append(" ".join(translations))
            else:
                verse_data.append("")

            commentaries = []
            while next_sib and not next_sib.find("span", {"class": "calibre16"}):
                commentaries.append(next_sib.text.strip())
                next_sib = next_sib.find_next_sibling("p")
            verse_data.append(" ".join(commentaries))

            # Add to verses_data only if there's either translation or commentary
            if verse_data[0] or verse_data[2] or verse_data[3]:
                verses_data.append(verse_data)

    return verses_data


def write_to_csv(verses_data, chapter_number):
    with open(
        "./output/Yukteshwar/Chapter{}Yukteshwar.csv".format(chapter_number), "wb"
    ) as file:
        writer = csv.writer(file, encoding="utf-8")
        writer.writerow(["Verse Number", "Verse", "Translation", "Commentary"])
        for verse_data in verses_data:
            writer.writerow(verse_data)


author = "Yukteshwar"
directory = "./HTML files/{}/".format(author)

for fileName in os.listdir(directory):
    if fileName.endswith(".html"):
        html_file = os.path.join(directory, fileName)
        html_content = get_html_content(html_file)
        chapter_number = extract_chapter_number(html_file)
        if chapter_number is not None:
            data = extract_data(html_content)
            write_to_csv(data, chapter_number)
