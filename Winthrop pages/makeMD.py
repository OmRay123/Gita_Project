import os
import re

png_dir = "../Images/"

# Directories containing the .md files
md_dirs = {
    "Pranab": "../Pranab/Output/",
    "Yukteshwar": "../Yukteshwar Lahiri Gita/CSV Output/Yukteshwar/",
    "Lahiri": "../Yukteshwar Lahiri Gita/CSV Output/Lahiri/",
}

png_files = [f for f in os.listdir(png_dir) if f.endswith(".png")]

# Loop through the .png files
for png in png_files:
    chapter, verse = re.findall(r"\d+", png)
    new_filename = "CH{}-{}.md".format(chapter, verse)

    # Open the new file and write content
    with open(new_filename, "w") as file:
        file.write(f"![[{png}]]\n\n### Commentaries\n\n---\n")

        for author, md_dir in md_dirs.items():
            md_files = [f for f in os.listdir(md_dir) if f.endswith(".md")]
            matching_md = None

            for md in md_files:
                numbers_in_md = [str(int(num)) for num in re.findall(r"\d+", md)]
                if numbers_in_md[0] == chapter and verse in numbers_in_md[1:]:
                    matching_md = md
                    break

            if matching_md is not None:
                file.write(f"\n#### {author}: [[{matching_md}]]\n")
            else:
                file.write(f"\n#### {author}: No commentary found for this verse.\n")
