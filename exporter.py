import csv
import os
import normalizer
"""Module for exporting transaction records to CSV files."""


def read_csv(file_path):
    """Read and print the contents of a CSV file."""
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def append_to_csv(file_path: str, data: dict):
    """Append a transaction record to an existing CSV file. Create the file if it doesn't exist."""
    fieldnames = data.keys()
    # print(fieldnames)
    try:
        with open(file_path, mode='a', newline='') as file:
            # print("File opened in append mode.")
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(data)
    except FileNotFoundError:
        create_csv(file_path, data)

def create_csv(file_path: str, data: dict):
    """Create a new CSV file and write the transaction record to it."""
    fieldnames = data.keys()
    # print(fieldnames)
    with open(file_path, mode='w', newline='') as file:
        print("File created.")
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)

if __name__ == "__main__":
    transaction_record = normalizer.normalizer()
    output_file = 'expenses.csv'
    if os.path.isfile(output_file):
        append_to_csv(output_file, transaction_record)
    else:
        create_csv(output_file, transaction_record)
