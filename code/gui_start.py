from tkinter import *
from tkinter import ttk
from organize import *
from main import *

def build_data(start=None, end=None):

    generate_data_text()
    
    # Takes an initial pdf and creates a new file in data_text
    

    data = []
    src = pathlib.Path("data_text/")


    for file in sorted(src.iterdir()):
        
        if start is not None and file.name[5:] < start:
            continue
        if end is not None and file.name[5:] > end:
            continue
        text = establish_lines(file)
        chequeing = keep_only_entries_with_transaction(text)
        
        data.append(chequeing)
    # should be the transaction log of chequeing account
    
    chunks = []
    
    for dat in data:
        
        blocks = create_list_of_transactions(dat)
        
        chunks.extend(blocks)
    
    dictionary = initialize_dictionary(chunks)
    # woo! got both deposits and withdrawals working, reworked the framework I was using to sort them
    # I definitely know there are better ways, but I got my way working and it feels semi-clean XD

class Window_for_Presentation:
    def __init__(self, root):


        root.title("Finance Manager")

        mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        self.datestart = StringVar()
        self.dateend = StringVar()

        start_entry = ttk.Entry(mainframe, width=7, textvariable=self.datestart)
        end_entry = ttk.Entry(mainframe, width=7, textvariable=self.dateend)

        start_entry.grid(column=1, row=1, sticky=(W, E))
        end_entry.grid(column=2, row=1, sticky=(W, E))

        self.data = StringVar()
        ttk.Label(mainframe, textvariable=self.data).grid(column=2, row=2, sticky=(W, E))


        ttk.Button(mainframe, text="Run", command=self.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(2, weight=1)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)

build_data()




