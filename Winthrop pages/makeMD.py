import os
import re

png_dir = "../Images/"
md_dir = "../Pranab/Output/"

png_files = [f for f in os.listdir(png_dir) if f.endswith(".png")]
md_files = [f for f in os.listdir(md_dir) if f.endswith(".md")]

for png in png_files:
    chapter, verse = re.findall(r"\d+", png)
    matching_md = None
    for md in md_files:
        numbers_in_md = [str(int(num)) for num in re.findall(r"\d+", md)]
        if numbers_in_md[0] == chapter and verse in numbers_in_md:
            matching_md = md
            break
    if matching_md is None:
        print("No commentary file found for {}".format(png))
        continue
    new_filename = "./output/CH{}-{}.md".format(chapter, verse)
    with open(new_filename, "w") as file:
        file.write("![[{}]]\n\n##### Commentaries\n[[{}]]".format(png, matching_md))
