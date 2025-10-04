import parser_1
import extracter
from datetime import date

def normalize_amount(amount_str: str) -> float:
    try:
        return float(amount_str)
    except ValueError:
        return 0.0

def convert_to_date(date_str: str) -> date:
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return date.today()

def create_transaction_record(file_name: str, date_str: str, amount_str: str, vendor: str) -> dict:
    return {
        "file_name": file_name,
        "date": convert_to_date(date_str),
        "amount": normalize_amount(amount_str),
        "vendor": vendor
    }


def main():
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


if __name__ == "__main__":
    main()
    