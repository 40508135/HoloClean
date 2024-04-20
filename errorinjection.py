import csv
import random

error_rate = 0.1

def add_errors(input_file_path, output_file_path):
    with open(input_file_path, 'r', newline='') as infile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            print(row)
            for i in range(len(row)):
                if len(row[i]) == 0:
                    continue
                if random.random() < error_rate:
                    idx = random.randrange(0, len(row[i]))
                    row[i] = row[i][:idx] + "x" + row[i][idx + 1:]
            writer.writerow(row)


# change the input and output file path here.
input_file_path = 'flights.csv'
output_file_path = 'flights_dirty0.1.csv'
add_errors(input_file_path, output_file_path)
