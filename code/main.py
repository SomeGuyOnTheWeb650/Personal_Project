from pypdf import PdfReader
import os
import re
import sys
import pathlib
import sensitive
from organize import establish_lines, keep_only_entries_with_transaction, create_list_of_transactions, initialize_dictionary
# TODO: make a sensitive.py checker, make file if not found, ask in the GUI whether you want to define bank or town
# to reduce sensitive info

def generate_data_text():
    
    dir = pathlib.Path("data/")
    os.makedirs(dir, exist_ok=True)
        
    # will need to change this and establish dummy data to demonstrate functionality
    # blegh, lotta work
    dst = pathlib.Path("data_text/")
    os.makedirs(dst, exist_ok=True)
    docs = []
    for file in dir.iterdir():
        
        if file.is_file():
            reader = PdfReader(file)
    # reader object not a string
            page = reader.pages[0:]
    # page object, in this case a list of page objects
            text = ""
            for item in page:
        # need extract text method to translate page objects into strings, or plain text
                text = text + '\n' + item.extract_text()
            shrunk = text.replace(" ", "")
            lower = shrunk.lower()
            m = re.search(r"[0-9]{2}([a-z]){3,5}[0-9]{2}", lower)
            
            if m:
                month = m.group()[2:5]
                months = {"jan": '01', "feb": '02', "mar": '03', "apr": '04', "may": '05', "jun": '06',
                        "jul": '07', "aug": '08', "sep": '09', "oct": '10', "nov": '11', "dec": '12'}
                if month in months:
                    date = m.group()[5:] + months[month]

                    f = sensitive.BANK + "_" + date + ".txt"
                    new = dst / f
                        
                with pathlib.Path.open(new, "w") as f:
                    f.write(text)
                    #Path.open() needs the "w" to change mode to write mode, allows for the creation
                    #of files instead of just the reference of existing ones
                doc = establish_lines(new)
                docs.append(doc)
    return docs


def main():
    rejoined = generate_data_text()
    # Takes an initial pdf and creates a new file in data_text
    data = []
    for item in rejoined:

        chequeing = keep_only_entries_with_transaction(item)
        data.append(chequeing)
    # should be the transaction log of chequeing account
    chunks = []
    for dat in data:

        blocks = create_list_of_transactions(dat)
        chunks.extend(blocks)
    initialize_dictionary(chunks)
    # woo! got both deposits and withdrawals working, reworked the framework I was using to sort them
    # I definitely know there are better ways, but I got my way working and it feels semi-clean XD


    



main()