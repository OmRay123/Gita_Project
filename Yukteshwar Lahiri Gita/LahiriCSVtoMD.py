import csv
import re


def csv_to_arr(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    del data[0]
    return data


def write_to_file(path, content):
    with open(path, "a") as f:
        f.write(content)


def create_file(ch_num, pranab_arr, gita_arr):
    for record in pranab_arr:
        file_name = f"Lahiri-CH0{ch_num}-{re.sub(r'[^0-9,]', '', record[0])}.md"
        print(file_name)
        write_path = f"./CSV Output/Lahiri/{file_name}"

        verse_nums = re.findall(r"\d+", record[0])
        verse_content = "\n".join(
            [
                f"{gita_arr[int(verse)-1][0]}\n{gita_arr[int(verse)-1][1]}\n"
                for verse in verse_nums
            ]
        )

        # Check if translation and commentary exist
        translation = record[1] if record[1] else "No translation"
        commentary = record[2] if record[2] else "No commentary"

        content = (
            "### Prose \n --- \n"
            + f"{verse_content}\n"
            + "### Translation \n --- \n"
            + f"{translation}\n\n"
            + "### Commentary \n --- \n"
            + f"{commentary}"
        )

        write_to_file(write_path, content)


def process_chapters(chapters):
    for ch_num in chapters:
        original_gita_path = f"../CSVs/Chapter{ch_num}.csv"
        lahiri_gita_path = f"./output/Lahiri/Chapter{ch_num}Lahiri.csv"

        gita_arr = csv_to_arr(original_gita_path)
        lahiri_arr = csv_to_arr(lahiri_gita_path)

        create_file(ch_num, lahiri_arr, gita_arr)


chapters = [str(i) for i in range(1, 19)]
process_chapters(chapters)
