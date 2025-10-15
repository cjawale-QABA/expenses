import parser
import extractor
from datetime import date

def normalize_amount(amount_str: str) -> float:
    try:
        # print(f"Normalizing amount: {amount_str}")
        amount_str = amount_str.replace(",", ".")
        return float(amount_str)
    except ValueError:
        return 0.0

def convert_to_date(date_str: str) -> date:
    day, month, year = date_str.split('-')
    try:
        return date(int(year), int(month), int(day)).strftime("%d-%m-%Y")
    except ValueError:
        # print(f"Invalid date format: {date_str}")
        return date.today()

def create_transaction_record(file_name: str, date_str: str, amount_str: str, vendor: str) -> dict:
    return {
        "file_name": file_name,
        "date": convert_to_date(date_str),
        "amount": normalize_amount(amount_str),
        "vendor": vendor
    }

def Normalizer():
    file_name = "BEINV24000000797074.pdf"
    pdf_text = extractor.extract_text_from_pdf(file_name)
    lines = parser.split_lines(pdf_text)
    extracted_dates = parser.extract_dates(lines)
    print("Extracted Dates:", extracted_dates)
    extracted_amounts = parser.extract_total_amounts(lines)
    vendor_info = parser.extract_vendors_info(lines)
    print("Vendor Info:", vendor_info)
    if extracted_dates and extracted_amounts:
        transaction_record = create_transaction_record(
            file_name,
            extracted_dates,
            extracted_amounts,
            vendor_info
        )
        return transaction_record
    else:
        print("Could not extract necessary information.")

def main():
    print(Normalizer())


if __name__ == "__main__":
    main()
    