import sorter
import normalizer
import parsing as parser
import extractor
import exporter
import os
from datetime import date
from typing import List
from dataclasses import dataclass

"""Main module to orchestrate file processing, including extraction, parsing, normalization, exporting, and sorting."""
""" Define file type categories based on extensions."""
# Define directory paths and file extensions
images_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')  # image file extensions
pdf_extensions = ('.pdf',)  # pdf file extensions
email_extensions = ('.eml', '.msg')  # email file extensions    

def extract_file_text(file_path: str) -> str:
    """Extract text from a file based on its type (image, PDF, email)."""
    file_name = os.path.basename(file_path)
    extension_file_name = file_name.lower().split('.')[-1]
    # print(extension_file_name)
    if images_extensions.__contains__(f'.{extension_file_name}'):
        print(f"Processing image file: {file_path}")
        return extractor.extract_text_from_image(file_path)
    elif pdf_extensions.__contains__(f'.{extension_file_name}'):  
        print(f"Processing PDF file: {file_path}")
        return extractor.extract_text_from_pdf(file_path)
    elif email_extensions.__contains__(f'.{extension_file_name}'): 
        print(f"Processing email file: {file_path}")
        return extractor.extract_text_from_email(file_path)
    else:
        print(f"extract_file_text File {file_name} does not match any category")
        return ""


def parsing_text(filetext: str) -> dict:
    """Parse extracted text to retrieve dates, amounts, and vendor information."""
    # Further processing of the extracted text
    lines = parser.split_lines(filetext)
    extracted_dates = parser.extract_dates(lines)
    # print("Extracted Dates:", extracted_dates)
    extracted_amounts = parser.extract_total_amounts(lines)
    vendor_info = parser.extract_vendors_info(lines)
    # print("Vendor Info:", vendor_info)
    return {
        "dates": extracted_dates,
        "amounts": extracted_amounts,
        "vendor": vendor_info
    }


def normalizing_info(extracted_info: dict, file_name: str) -> dict:
    """Normalize parsed information into a structured transaction record."""
    extracted_dates = extracted_info.get("dates")
    # print("Extracted Dates:", extracted_dates)
    extracted_amounts = extracted_info.get("amounts")
    # print("Extracted Amounts:", extracted_amounts)
    vendor_info = extracted_info.get("vendor")
    # print("Vendor Info:", vendor_info)
    
    if extracted_dates and extracted_amounts:
        transaction_record = normalizer.create_transaction_record(
            file_name,
            extracted_dates,
            extracted_amounts,
            vendor_info
        )
        return transaction_record
    else:
        print("Could not extract necessary information.")
        return {}
    
    
def file_processing(file_path: str):
    """Process a single file: extract text, parse, normalize, export, and move the file."""
    file_name = os.path.basename(file_path)
    filetext = extract_file_text(file_path)
    # Further processing of the extracted text
    extracted_info = parsing_text(filetext)
    transaction_record = normalizing_info(extracted_info, file_name)
    if transaction_record:
        output_file = 'expenses.csv'
        if os.path.isfile(output_file):
            exporter.append_to_csv(output_file, transaction_record)
        else:
            exporter.create_csv(output_file, transaction_record)
        # Move the original file to the 'processed' folder
        sorter.create_folders('processed')
        move_dest = os.path.join('processed', file_name)
        print(f"Moving file {file_path} to {move_dest}")
        sorter.move_files(file_path, move_dest)
    else:
        print(f"Skipping file {file_name} due to incomplete information.")



def main():
    """Main function to process all files in the input directory."""
    allowed_extensions = images_extensions + pdf_extensions + email_extensions # allowed file extensions
    directory = 'input' # directory to organize
    for file in os.listdir(directory):  # iterate over files in the directory
        file_path = os.path.join(directory, file)  # get full file path
        if os.path.isfile(file_path):  # check if it's a file
            # print(sorter.check_files(file, allowed_extensions))
            if sorter.check_files(file, allowed_extensions): # check if it's an image
                file_processing(file_path) # process the file
            else:
                print(f"File {file} does not match any category")
    print("All files processed")
    print("File processing complete.")
        
        
if __name__ == "__main__":
    main()  # run the main function
# This script organizes files in the specified directory into subdirectories based on file types.