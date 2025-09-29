import os  # import os module
"""
This script organizes files in a specified directory into subdirectories based on file types.
It creates folders for images, PDFs, and emails, and moves files into these folders accordingly.
"""

# Define directory paths and file extensions
directory = '/Users/chaitalijawale/Downloads'  # set directory path
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


def file_iterator(directory):
    """
    Iterate over files in the specified directory and move them to corresponding folders based on file types.

    Args:
        directory (str): The directory to scan for files.

    Returns:
        None
    """
    try:
        for item in os.listdir(directory):  # iterate over items in the directory
            item_path = os.path.join(directory, item)  # get full path of the item
            if os.path.isfile(item_path):  # check if it's a file
                if check_files(item, images_extensions):
                    move_files(item_path, os.path.join(images, item))  # move image files
                elif check_files(item, pdf_extensions):
                    move_files(item_path, os.path.join(pdfs, item))  # move pdf files
                elif check_files(item, email_extensions):
                    move_files(item_path, os.path.join(emails, item))  # move email files
                else:
                    print(f"File {item} does not match any category")
            else:
                print(f"{item} is not a file")
    except Exception as e:
        print(f"Error iterating over files in {directory}: {e}")


def main():
    create_folders(images)  # create images folder
    create_folders(pdfs)  # create pdfs folder
    create_folders(emails)  # create emails folder
    file_iterator(directory)  # start file iteration and organization


if __name__ == "__main__":
    main()  # run the main function
# This script organizes files in the specified directory into subdirectories based on file types.