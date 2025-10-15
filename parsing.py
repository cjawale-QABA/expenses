import re
from datetime import date
import extractor
from typing import List
import csv
"""Module for parsing text to extract dates, amounts, and vendor information."""

"""Regex patterns and keywords for identifying dates and total amounts in text."""

date_regex = r'(0?[1-9]|[12][0-9]|3[01])[/|-](0?[1-9]|[1][0-2])[/|-]([0-9]{4}|[0-9]{2})'
total_amount_regex = r'(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})'
total_keywords = ["Totaal", "Total", "Total Amount", "Te betalen", "Som", "Bedrag", "A payé", "Montant", "A payer", "Cash", "Invoice Total", "Factuurbedrag"]

"""List of common company abbreviations in Belgium to help identify vendor names."""

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
    """Split text into non-empty, stripped lines."""
    # text = text.replace('\r\n', '\n').replace('\r', '\n')
    extracted_lines = []
    for line in text.splitlines():
        stripped_line = line.strip()
        if stripped_line:
            # print(f"Line: {stripped_line}")
            extracted_lines.append(stripped_line)
    return extracted_lines

def extract_dates(lines):
    """Extract the first date found in the text lines."""
    for line in lines:
        match = re.search(date_regex, line)
        if match:
            day = match.group(1)
            month = match.group(2)
            year = match.group(3)
            # Normalize year to 4 digits
            if len(year) == 2:
                year = "20" + year
            date_str = f"{day}-{month}-{year}"
            # return date(int(year), int(month), int(day))
            return date_str
            
            
def extract_total_amounts(lines):
    """Extract the total amount from the text lines based on keywords."""
    for line in lines:
        if any(keyword.lower() in line.lower() for keyword in total_keywords):
            match = re.search(total_amount_regex, line)
            if match:
                amount_str = match.group(0)
                # Remove currency symbols and commas
                amount_str = re.sub(r'[\$€₹]', '', amount_str)
                return amount_str


def vendor_in_vendor_list(lines: List[str], vendors: List[str]):
    """Check if any vendor from the list is mentioned in the text lines."""
    for line in lines:
        # print(f"Checking line: {line}")
        for vendor in vendors:
            # print(f"Is vendor: {vendor} in line: {line}?")
            if line.lower().__contains__(vendor.lower()):
                # print(f"Matched vendor: {vendor} in line: {line}")
                return vendor
            # else:
            #     for abbr in company_abbreviations:
            #         if abbr in line:
            #             print(f"Matched abbreviation: {abbr} in line: {line}")
            #             return line
    return None


def check_abbreviations_in_lines(lines: List[str]):
    """Check for company abbreviations in the text lines to identify vendor names."""
    for line in lines:
        for abbr in company_abbreviations:
            if abbr in line:
                return line
    return None


def read_vendors_from_file(file_path):
    """Read vendor names from a CSV file into a list."""
    vendors = []
    with open(file_path, 'r') as file:
        for line in file:
            vendor = line.strip()
            if vendor:
                vendors.append(vendor)
    return vendors


def write_vendors_to_file(vendors, file_path):
    """Write the list of vendor names to a CSV file."""
    with open(file_path, 'w') as file:
        for vendor in vendors:
            file.write(vendor + '\n')


def vendors_update(vendors, new_vendor):
    """Add a new vendor to the list and update the CSV file if it's not already present."""
    if new_vendor and new_vendor not in vendors:
        vendors.append(new_vendor)
        write_vendors_to_file(vendors, "Vendors - Vendors.csv")
        print(f"New vendor '{new_vendor}' added to the file.")
    else:
        print("Vendor already exists or not found.")
        
        
def extract_vendors_info(lines):
    """Extract vendor information from text lines using a predefined vendor list and abbreviations."""
    vendors = read_vendors_from_file("input/Vendors - Vendors.csv")
    vendor_info = vendor_in_vendor_list(lines, vendors)
    if not vendor_info:
        vendor_info = check_abbreviations_in_lines(lines)
        vendors_update(vendors, vendor_info)
    return vendor_info

def main():
    pdf_text = extractor.extract_text_from_pdf("input/Ticket20250401004820590073.pdf")
    lines = split_lines(pdf_text)
    extracted_dates = extract_dates(lines)
    extracted_amounts = extract_total_amounts(lines)
    print("Extracted Dates:", extracted_dates)
    print("Extracted Amounts:", extracted_amounts)
    # image_text = extracter.extract_text_from_image("input/1759751396753.jpg")
    # lines = split_lines(image_text)
    # extracted_dates = extract_dates(lines)
    # extracted_amounts = extract_total_amounts(lines)
    # print("Extracted Dates:", extracted_dates)
    # print("Extracted Amounts:", extracted_amounts)
    vendor_info = extract_vendors_info(lines)
    print("Vendor Info:", vendor_info)
        

if __name__ == "__main__":
    main()
    