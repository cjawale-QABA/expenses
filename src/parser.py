import re
from datetime import date
import extracter


date_regex = r'(0?[1-9]|[12][0-9]|3[01])[/|-](0?[1-9]|[1][0-2])[/|-]([0-9]{4}|[0-9]{2})'
total_amount_regex = r'(\d{1,3}(?:\.\d{3})*,\d{2})'
total_keywords = ["Totaal", "Total", "Total Amount", "Te betalen", "Som", "Bedrag", "A payé", "Montant", "A payer", "Cash", "Invoice Total", "Factuurbedrag"]

company_abbreviations = [
    # Current forms
    "BV", "SRL",      # Besloten vennootschap / Société à responsabilité limitée
    "NV", "SA",       # Naamloze vennootschap / Société anonyme
    "CV", "SC",       # Coöperatieve vennootschap / Société coopérative
    "VOF", "SNC",     # Vennootschap onder firma / Société en nom collectif
    "CommV", "SComm", # Commanditaire vennootschap / Société en commandite
    "SE",             # Societas Europaea (European company)
    "SCE",            # European Cooperative Company
    # Former / replaced forms
    "BVBA", "SPRL",   # Besloten vennootschap met beperkte aansprakelijkheid / Société privée à responsabilité limitée
    "EBVBA", "EPRL",  # Eenpersoons-BVBA / SPRL unipersonnelle
    "CVBA", "SCRL",   # Coöperatieve vennootschap met beperkte aansprakelijkheid / Société coopérative à responsabilité limitée
    "CVOA", "SCRI",   # Coöperatieve vennootschap met onbeperkte aansprakelijkheid / Société coopérative à responsabilité illimitée
    "CommVA", "SCA",  # Commanditaire vennootschap op aandelen / Société en commandite par actions
    "THV",            # Tijdelijke handelsvennootschap / Société momentanée
    "Stille Vennootschap", "Société interne" # Silent partnership forms (legacy)
]


def split_lines(text):
    # text = text.replace('\r\n', '\n').replace('\r', '\n')
    extracted_lines = []
    for line in text.splitlines():
        stripped_line = line.strip()
        if stripped_line:
            extracted_lines.append(stripped_line)
    return extracted_lines

def extract_dates(lines):
    for line in lines:
        match = re.search(date_regex, line)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            # Normalize year to 4 digits
            if len(year) == 2:
                year = "20" + year
            return date(int(year), int(month), int(day))
            
            
def extract_total_amounts(lines):
    for line in lines:
        if any(keyword.lower() in line.lower() for keyword in total_keywords):
            match = re.search(total_amount_regex, line)
            if match:
                amount_str = match.group(0)
                # Remove currency symbols and commas
                amount_str = re.sub(r'[\$€₹.]', '', amount_str)
                return amount_str


def extract_vendor_info(lines, vendors):
    for line in lines:
        for vendor in vendors:
            if vendor.lower() in line.lower():
                return vendor
            else:
                for abbr in company_abbreviations:
                    if abbr in line:
                        return line


def read_vendors_from_file(file_path):
    vendors = []
    with open(file_path, 'r') as file:
        for line in file:
            vendor = line.strip()
            if vendor:
                vendors.append(vendor)
    return vendors


def write_vendors_to_file(vendors, file_path):
    with open(file_path, 'w') as file:
        for vendor in vendors:
            file.write(vendor + '\n')


def vendors_update(vendors, new_vendor):
    if new_vendor and new_vendor not in vendors:
        vendors.append(new_vendor)
        write_vendors_to_file(vendors, "Vendors - Vendors.csv")
        print(f"New vendor '{new_vendor}' added to the file.")
    else:
        print("Vendor already exists or not found.")

def main():
    pdf_text = extracter.extract_text_from_pdf("BEINV24000000797074.pdf")
    lines = split_lines(pdf_text)
    extracted_dates = extract_dates(lines)
    extracted_amounts = extract_total_amounts(lines)
    print("Extracted Dates:", extracted_dates)
    print("Extracted Amounts:", extracted_amounts)
    # image_text = extracter.extract_text_from_image("12070.jpg")
    # lines = split_lines(image_text)
    # extracted_dates = extract_dates(lines)
    # extracted_amounts = extract_total_amounts(lines)
    # print("Extracted Dates:", extracted_dates)
    # print("Extracted Amounts:", extracted_amounts)
    vendors = read_vendors_from_file("Vendors - Vendors.csv")
    vendor_info = extract_vendor_info(lines, vendors)
    vendors_update(vendors, vendor_info)
    print("Vendor Info:", vendor_info)
        

if __name__ == "__main__":
    main()
    