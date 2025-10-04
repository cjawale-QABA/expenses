import csv
from Normalizer import create_transaction_record
import extracter
import parser_1


def read_csv(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

def append_to_csv(file_path: str, data: dict):
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writerow(data)



if __name__ == "__main__":
    read_csv('expenses.csv')
    file_name = "BEINV24000000797074.pdf"
    pdf_text = extracter.extract_text_from_pdf(file_name)
    lines = parser_1.split_lines(pdf_text)
    extracted_dates = parser_1.extract_dates(lines)
    extracted_amounts = parser_1.extract_total_amounts(lines)
    vendors = parser_1.read_vendors_from_file("Vendors - Vendors.csv")
    vendor_info = parser_1.extract_vendor_info(lines, vendors)
    parser_1.vendors_update(vendors, vendor_info)
    print("Vendor Info:", vendor_info)
    
    if extracted_dates and extracted_amounts:
        transaction_record = create_transaction_record(
            file_name,
            extracted_dates[0],
            extracted_amounts[0],
            vendor_info
        )
        print("Transaction Record:", transaction_record)
    else:
        print("Could not extract necessary information.")
    append_to_csv('expenses.csv', transaction_record.values())
