import unicodecsv as csv

def write_dict_list(data, filepath):
    with open(filepath, 'wb') as output:
        writer = csv.writer(output)
        
        columns = data[0].keys()

        writer.writerow(columns)

        for row in data:
            temp = []

            for column in columns:
                temp.append(row[column])

            writer.writerow(temp)