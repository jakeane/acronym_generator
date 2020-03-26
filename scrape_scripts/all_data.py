# Author: Jack Keane
# Date: 3/25/20
# Description: Combines all data in separate file

files = ["quotes", "shakespeare", "state_union", "inaugural", "bible"]

all_files = open("../acronym_data/all_data.csv", "w")

for file in files:
    f = open("acronym_data/" + file + "_data.csv", "r")
    for line in f:
        all_files.write(line)
    f.close()
all_files.close()
