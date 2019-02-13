import csv
import os

token_map = {}

for file in os.listdir("output\searches"):
    with open("output/searches/{0}".format(file), 'rb') as in_csv:
        data = csv.reader(in_csv)

        for row in data:
            tokens = row[2].split(' ')

            for token in tokens:
                if token in token_map:
                    token_map[token] = token_map[token] + 1
                else:
                    token_map[token] = 1

output = []

for key in token_map:
    output.append([key, token_map[key]])

with open("word_counts.csv", 'wb') as out_csv:
    writer = csv.writer(out_csv)

    for row in output:
        writer.writerow(row)