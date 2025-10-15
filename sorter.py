import os  # import os module
"""
This script organizes files in a specified directory into subdirectories based on file types.
It creates folders for images, PDFs, and emails, and moves files into these folders accordingly.
"""

# Define directory paths and file extensions
input_folder = 'input'  # Input folder name
directory = os.path.abspath(input_folder)  # set directory path
images = os.path.join(directory, 'images')  # set images subdirectory path
pdfs = os.path.join(directory, 'pdfs')  # set pdfs subdirectory path
emails = os.path.join(directory, 'emails')  # set emails subdirectory path
images_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')  # image file extensions
pdf_extensions = ('.pdf',)  # pdf file extensions
email_extensions = ('.eml', '.msg')  # email file extensions    


def create_folders(folder_name):
    """Create a folder if it doesn't exist.

    Args:
        folder_name (str): The name of the folder to create.
    """    
    if os.path.exists(folder_name):
        print(f"Directory {folder_name} exists")
    else:
        try:
            os.mkdir(folder_name)  # create directory if it doesn't exist
            print(f"Directory {folder_name} created")
        except FileNotFoundError:
            print("Check the path, some parent directory is missing")
        except Exception as e:
            print(f"Error creating directory {folder_name}: {e}")


def check_files(file_name, extensions):
    """
    Check if the file has one of the specified extensions.
    Args:
        file_name (str): The name of the file to check.
        extensions (tuple): A tuple of file extensions to check against.
    Returns:
        bool: True if the file has one of the specified extensions, False otherwise.
    """
    return file_name.lower().endswith(extensions)  # check if file ends with given extensions


def move_files(src, dest):
    """
    Move files from source to destination.

    Args:
        src (str): The source file path.
        dest (str): The destination file path.

    Returns:
        None
    """
    try:
        os.rename(src, dest)  # move file from src to dest
        print(f"Moved file from {src} to {dest}")
    except FileNotFoundError:
        print(f"Source file {src} not found")
    except Exception as e:
        print(f"Error moving file from {src} to {dest}: {e}")
        print("Check if the destination directory exists")


def main():
    print(directory)  # print the directory path
    # create_folders(images)  # create images folder
    # create_folders(pdfs)  # create pdfs folder
    # create_folders(emails)  # create emails folder
    for file in os.listdir(directory):  # iterate over files in the directory
        file_path = os.path.join(directory, file)  # get full file path
        if os.path.isfile(file_path):  # check if it's a file
            if check_files(file, images_extensions): # check if it's an image
                move_files(file_path, os.path.join(images, file))  # move to images folder
            elif check_files(file, pdf_extensions):  # check if it's a pdf
                move_files(file_path, os.path.join(pdfs, file))  # move to pdfs folder
            elif check_files(file, email_extensions):  # check if it's an email
                move_files(file_path, os.path.join(emails, file))  # move to emails folder
            else:
                print(f"File {file} does not match any category")
        print("All files processed")
        print("File organization complete.")

if __name__ == "__main__":
    main()  # run the main function
# This script organizes files in the specified directory into subdirectories based on file types.