import os
import re
from enum import Enum
import sensitive
# important split keywords
# OWNER, SPLITS into blocks seperated by account type
# UNLIMITED checks that the transaction block following is chequeing
# EVERYDAY checks that the transaction block following is savings
# SHARES checks that "" is Shares
# REWARDS checks that "" is Rewards


def establish_lines(path):
    
    clean = []
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        shrunk_lines = line.replace(" ", "")
        stripped_lines = shrunk_lines.strip()
        
        if stripped_lines.lower():
            
            clean.append(stripped_lines.lower())
    rejoined = "\n".join(clean)
    return rejoined
    
# returning a cleaned and rejoined block of text
# should have newlines at the original places where line return was

def keep_only_entries_with_transaction(rejoined):
    blocks = rejoined.split("owner")
    for index, value in enumerate(blocks):
        if "unlimited" in value:
            chequeing = blocks[index + 1]
            return chequeing
        
    


def create_list_of_transactions(chequeing: str):
    lines = chequeing.split("\n")
    blocks = []
    block = []
    # block is going to be a string seperated by newlines
    # that contains ALL of a SINGLE transactions data
    for line in lines:
        spot = line + "\n"
        # spot is shorthand for each line with a newline added, for ease of typing
        if re.match(r"[0-9]{2}[a-z]{3,5}[0-9]{2}", line):
            # essentially a catch to end a transaction out, and start the next
            if block:
                
                a = ""
                for index, item in enumerate(block):
                    if re.match(r"[0-9]{2}[a-z]{3,5}[0-9]{2}", item):

                        a = "\n".join(block[index:])
                        break
                # a makes the block not a list but a string joined with newlines
                 
                blocks.append(a)
                # append a to blocks for the full transaction
                block = []
                # reset block to empty for next transaction

        if len(block) >= 2:
            continue
        # if block is above a certain length, it will contain fluff, like page endings and beginnings
        # restrict block size to clear fluff
        block.append(spot)
        # append spot to block
    
    
    blocks.append("\n".join(block))
    # flush leftover block into blocks
    no_empty = []
    for chunk in blocks:
        if not chunk:
            continue
        no_empty.append(chunk)
        # clean blocks out, don't leave empty index's
    return no_empty
        
def initialize_dictionary(blocks: list[str]) -> dict[str, int]:
    data = {
        "count": 0,
        "withdrawals": {},
        "deposits" : {}
    }
    
    for block in blocks:
        
        if "balance" in block:
            funds = int(block.split("\xa0")[1].strip().replace(",", "").replace(".", ""))
            if "start" not in data:

                data["start"] = funds
            
            if "current" not in data:
                data["current"] = funds
            
        elif "withdrawal" in block or "bill" in block:
            decrease = data["withdrawals"]
            if "paypal" in block:
                funds = int(block.split("\xa0")[1].strip().replace(",", "").replace(".", ""))
                if "paypal" not in decrease:
                    decrease["paypal"] = 0
                delta = data["current"] - funds
                decrease["paypal"] += delta
                data["current"] -= delta
                data["count"] += 1
                # paypal and collabria might be wrong for a bit, until I get deposits set up
            elif "collabria" in block:
                funds = int(block.split("\xa0")[1].strip().replace(",", "").replace(".", ""))
                if "collabria" not in decrease:
                    decrease["collabria"] = 0
                delta = data["current"] - funds
                decrease["collabria"] += delta
                data["current"] -= delta
                data["count"] += 1
            elif "bill" in block:
                a = block.split("-")[1]
                location = ""
                
                for index, char in enumerate(a):
                    
                    if char.isalpha():
                        
                        location += char
                    else:
                        
                        break
                b = a[index:]
                clean = clean_num(b)
                if location not in decrease:
                    decrease[location] = 0
                decrease[location] += clean
                data["current"] -= clean
                data["count"] += 1
            
            elif "atm" in block:
                if "atm" not in decrease:
                    decrease["atm"] = 0
                a = clean_num(block)
                decrease["atm"] += a
                data["current"] -= a
                data["count"] += 1
            
            elif "#" in block:
                a = block.split("withdrawal")[1]
                b = a.split("#")[0]
                location = b.replace("\n", "")
                funds = clean_num(block)
                if location not in decrease:
                    decrease[location] = 0
                decrease[location] += funds
                data["current"] -= funds
                data["count"] += 1


            else:
                a = block.split("withdrawal")[1]
                b = a.split("oliver")[0]
                c = b.strip("1234567890")
                location = c.replace("\n", "")
                funds = clean_num(block)
                if location not in decrease:
                    decrease[location] = 0
                decrease[location] += funds
                data["current"] -= funds
                data["count"] += 1

        elif "deposit" in block:        
            funds = int(block.split("\xa0")[1].strip().replace(",", "").replace(".", ""))
            increase = data["deposits"]
            if "payroll" in block:
                if "pattison" not in increase:

                    increase["pattison"] = 0
                increase["pattison"] += funds
                data["current"] += funds
                data["count"] += 1
            if "direct" in block:
                if "kitchen" not in increase:
                    increase["kitchen"] = 0
                increase["kitchen"] += funds
                data["current"] += funds
                data["count"] += 1
            
        elif "service" in block:
            location = "service"
            if location not in decrease:
                decrease[location] = 0
            a = block.split("charges")[1]
            funds = clean_num(a)
            decrease[location] += funds
            data["current"] -= funds
            data["count"] += 1

        elif "etransfer" in block:
                a = block.split("-")[1]
                location = ""
                
                for index, char in enumerate(a):
                    
                    if char.isalpha():
                        
                        location += char
                    else:
                        
                        break
                b = a[index:]
                c = b.split("\xa0")[1]
                clean = clean_num(c)
                if location not in increase:
                    increase[location] = 0
                increase[location] += clean
                data["current"] += clean
                data["count"] += 1

        else:
            print(block)
            raise Exception("Nothing should be here, if there is, need to implement a new condition")
            
            
    def sanitize(data):
        for dat in data:
            if isinstance(data[dat], dict):
                for spot in data[dat]:
                    if sensitive.TOWN in spot:
                        new = spot.replace(sensitive.TOWN, "")
                        data[dat][new] = data[dat][spot]
                        del data[dat][spot]
                        sanitize(data)
                        return data
                    if "store" in spot:
                        new = spot.replace("store", "")
                        data[dat][new] = data[dat][spot]
                        del data[dat][spot]
                        sanitize(data)
                        return data
        return data
    data = sanitize(data)                  
            
    print(data)
    
    
    pass

def clean_num(string: str) -> int:
    if sensitive.AREA in string:
        a = string.split(sensitive.AREA)[1].split("\xa0")[0]
    else:
        a = string.split("\xa0")[0]
    b = a.strip().replace(",", "").replace(".", "")
    return int(b)
