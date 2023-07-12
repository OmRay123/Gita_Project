import csv
import re

chapters = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
]

for chNum in chapters:
    originalGita = open("../CSVs/Chapter" + chNum + ".csv")
    pranabGita = open("./Pranab Gita Csvs/Chapter" + chNum + "PranabGita.csv")

    def csvToArr(file):
        with file as f:
            reader = csv.reader(f)
            arr = list(reader)
        del arr[0]
        return arr

    GitaArr = csvToArr(originalGita)
    PranabArr = csvToArr(pranabGita)

    for i in PranabArr:
        fileName = "P-CH0" + chNum + "-" + re.sub(r"[^0-9,]", "", i[0]) + ".md"
        print(fileName)
        f = open("./Output/" + fileName, "a")
        f.write("#### Prose \n\n")
        i[0] = ",".join(re.findall(r"\d+", i[0]))
        if len(i[0].split(",")) > 1:
            verseNums = i[0].split(",")
            for j in verseNums:
                j = int(j)
                f.write(GitaArr[j - 1][0] + "\n")
                f.write(GitaArr[j - 1][1] + "\n\n")
        else:
            f.write(GitaArr[int(i[0]) - 1][0] + "\n")
            f.write(GitaArr[int(i[0]) - 1][1] + "\n\n")
        f.write(" #### Bengali Translation \n\n")
        f.write(i[1])
        f.write("\n\n #### Commentary \n\n")
        f.write(i[2])
