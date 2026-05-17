import re
def establish_dictionary_of_locations(chequeing):
    lines = chequeing.split("\n")
    locations = {}
    for index, line in enumerate(lines):
        
        if not re.match(r"[0-9]{2}[a-z]{3,5}[0-9]{2}", line):
            
            continue 
        if "forward" in line:
            forward = line.split("\xa0")
            
            locations["start"] = int(forward[1].replace(",", "").replace(".", "").strip())
            locations["current"] = int(forward[1].replace(",", "").replace(".", "").strip())
        if "withdrawal" in line:
            
            
            section = line.split("withdrawal")[1] + lines[index + 1]
            if re.match(r"[0-9]{2}[a-z]{3,5}[0-9]{2}", lines[index + 1]):
                # special handling of transactions that are all on one line
                right = lines[index].split("withdrawal")[1]
                
                funds = ""
                for char in right:
                    if char.isalpha():
                        continue 
                    funds = funds + char
            elif re.match(r"[0-9]{2}[a-z]{3,5}[0-9]{2}", lines[index + 2]):
                funds = lines[index + 1].split("bcca")[1]
            else:
                funds = lines[index + 2]
            
            withdraw = int(funds.split("\xa0")[0].strip().replace(",", "").replace(".", ""))
            
            current = int(funds.split("\xa0")[1].strip().replace(",", "").replace(".", ""))
            #if (locations["current"] - withdraw != current):
                
             #   raise Exception("math error")
            if "#" in section:
                location = section.split("#")[0].strip()
            else:
                
            if "atm" in line:
                location = "atm"
            
            if "paypal" in lines[index + 1]:
                location = "paypal"
            if "collabria" in lines[index + 1]:
                location = "collabria"
            if location not in locations:
                locations[location] = 0

            locations[location] += withdraw
            locations["current"] -= withdraw
        if "service" in line:
                section = line.split("service")[1] + lines[index + 1]
                money = ""
                for index, char in enumerate(section):
                    if char.isalpha():
                        continue
                    money = section[index:]
                    break 
                money = money.split("totals")[0]
                withdraw = int(money.split("\xa0")[0].strip().replace(",", "").replace(".", ""))
                location = "service"
                if location not in locations:
                    locations[location] = 0    
                locations[location] += withdraw
                locations["current"] -= withdraw
        if "bill" in line:
                section = line.split("-")[1]
                
                money = ""
                for index, char in enumerate(section):
                    if char.isalpha():
                        continue
                    money = section[index:]
                    break 
                
                withdraw = int(money.split("\xa0")[0].strip().replace(",", "").replace(".", ""))
                location = "bills"
                if location not in locations:
                    locations[location] = 0    
                locations[location] += withdraw
                locations["current"] -= withdraw
    return locations
# BOOYAH ALL WITHDRAWALS ACCOUNTED FOR SIRE!
# Gotta get the deposits in next, project for tomorrow