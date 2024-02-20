# For pdf-handling:
import fitz
# for OS operations:
import os
# Use defaultdic to default keys when assigned
from collections import defaultdict
# and use hashes when comparing the files
import hashlib


class DuplicateRemover():
    """docstring for DuplicateRemover.
    """

    def __init__(self, dir_path=".", filetype=".pdf"):
        """_summary_

        Args:
            dir_path (str, optional): Path to the directory where duplicates get removed. Defaults to ".".
            filetype (str, optional): Filetype of the files which you want to clean from duplicates. Currently only allows the usage of pdf and plain textfiles . Defaults to ".pdf".
        """
        self.dir_path = dir_path
        self.filetype = filetype
        # needs to be initialized as object is created, a little dict of hashes where we assign the hashed text with the filepath
        self.text_to_path = defaultdict(list)

    def extract_text_from_pdf(self, file_path):
        """ Extract text content from a PDF file.
        
        Args:
            file_path (str): The file path to a PDF file from which you want to extract text.

        Returns:
            str: The text extracted from all the pages of the PDF located at the file_path.
        """
        doc = fitz.open(file_path)
        text = ""
        for page_num in range(doc.page_count):
            text += doc[page_num].get_text()
        return text

    def extract_text_from_text_file(self, file_path):
        """
        Read the text content from a text file.

        Args:
            file_path (str): The path to the text file from which you want to extract the text.

        Returns:
            str: The text content of the file located at the file_path if the file is successfully read.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def hasher(self, extraction_methode):
        """
        Read text from files in a directory, hash the text using MD5, and save the hash along with the file path in a dictionary.

        Args:
            extraction_method (function): A function that is expected to extract text from a file given the file path as input.
        """

        for filename in os.listdir(self.dir_path):
            if filename.endswith(self.filetype):
                file_path = os.path.join(self.dir_path, filename)
                # read the text
                text = extraction_methode(file_path)
                # and hash it:
                text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
                # and save the filepaths to each hash:
                self.text_to_path[text_hash].append(file_path)

    def remover(self):
        """
        The function removes duplicate files while keeping one copy.
        """
        for hash, files in self.text_to_path.items():
            if len(files) > 1:
                # remove all duplicates, but keep one copy:
                for dupes in files[1:]:
                    os.remove(dupes)

    def run(self):
        """
        Check the filetype of a file and then call different functions based on whether it is a PDF or plain text file.
        """
        # in case of pdfs
        if self.filetype == ".pdf":
            self.hasher(self.extract_text_from_pdf)
            self.remover()
        # in case of plain text:
        elif self.filetype == "":
            self.hasher(self.extract_text_from_text_file)
            self.remover()
        elif self.filetype == ".txt":
            self.hasher(self.extract_text_from_text_file)
            self.remover()
            
        else:
            raise Exception("Unknown filetype, write some, add a parser and an if clause to run")