import sorter
import normalizer
import parser
import extractor
import exporter
import os
from datetime import date
from typing import List
from dataclasses import dataclass



images_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')  # image file extensions
pdf_extensions = ('.pdf',)  # pdf file extensions
email_extensions = ('.eml', '.msg')  # email file extensions    

def file_processing(file_path: str):
    file_name = os.path.basename(file_path)
    extension_file_name = file_name.lower().split('.')[-1]
    # print(extension_file_name)
    if images_extensions.__contains__(f'.{extension_file_name}'):
        print(f"Processing image file: {file_path}")
        filetext = extractor.extract_text_from_image(file_path)
    elif pdf_extensions.__contains__(f'.{extension_file_name}'):  
        print(f"Processing PDF file: {file_path}")
        filetext = extractor.extract_text_from_pdf(file_path)
    elif email_extensions.__contains__(f'.{extension_file_name}'): 
        print(f"Processing email file: {file_path}")
        filetext = extractor.extract_text_from_email(file_path)
    else:
        print(f"file_processing File {file_name} does not match any category")
    # Further processing of the extracted text
    lines = parser.split_lines(filetext)
    extracted_dates = parser.extract_dates(lines)
    # print("Extracted Dates:", extracted_dates)
    extracted_amounts = parser.extract_total_amounts(lines)
    vendor_info = parser.extract_vendors_info(lines)
    # print("Vendor Info:", vendor_info)
    
    if extracted_dates and extracted_amounts:
        transaction_record = normalizer.create_transaction_record(
            file_name,
            extracted_dates,
            extracted_amounts,
            vendor_info
        )
        # print(transaction_record)
        output_file = 'expenses.csv'
        if os.path.isfile(output_file):
            exporter.append_to_csv(output_file, transaction_record)
        else:
            exporter.create_csv(output_file, transaction_record)
        sorter.create_folders('Processed')
        move_dest = os.path.join('Processed', file_name)
        print(f"Moving file {file_path} to {move_dest}")
        sorter.move_files(file_path, move_dest)
    else:
        print("Could not extract necessary information.")


def main():
    allowed_extensions = images_extensions + pdf_extensions + email_extensions
    directory = 'Input'
    # print(directory)  # print the directory path
    # print(allowed_extensions)  # print allowed extensions
    for file in os.listdir(directory):  # iterate over files in the directory
        file_path = os.path.join(directory, file)  # get full file path
        if os.path.isfile(file_path):  # check if it's a file
            # print(sorter.check_files(file, allowed_extensions))
            if sorter.check_files(file, allowed_extensions): # check if it's an image
                file_processing(file_path)
            else:
                print(f"File {file} does not match any category")
    # print("All files processed")
    # print("File organization complete.")
        
        
if __name__ == "__main__":
    main()  # run the main function
# This script organizes files in the specified directory into subdirectories based on file types.