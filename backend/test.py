import csv
with open("projects.csv", "r") as csv_file:
    projects = list(csv.reader(csv_file))


for row in projects:
    print(row)