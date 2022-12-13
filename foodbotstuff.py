#imports#
#
import webbrowser
#
#variables#
#
login_details = -1
url_test = "https://www.google.com/maps/search/" # Default google maps url
#
#definitions#
#
def return_file():
    with(open("data.txt","r"))as(file): # Opens the file as "file"
        data = eval(file.read()) # Turns the string file into a readable list()
    # File closed with sub-proccess
    return(data) # Returns the list
#
def login():
    username_passwords = return_file()[0] # Collects username/passwords from the file.
    username_input = input("username-: ")
    password_input = input("password-: ")
    for(user_data)in(username_passwords):
        if(username_input==user_data[0] and password_input==user_data[1]):
            username_passwords = username_passwords.index(user_data)
    return(username_passwords) # Returns all of the usernames and passwords
#
def display(data): # Essentially another print() but in a different format. the argument "data" is a list of strings to be printed.
    print("\n"*100)
    print("[   {|>=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=<|}   ]") #                             #
    print("[   {|- - - - - - - - -[ FOODBOT ]- - - - - - - - -|}   ]") # Displays the foodbot topbar #
    print("[   {|>=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=<|}   ]") #                             #
    print("[   {|"+(" "*45)+"|}   ]")
    for(data_packet)in(data): # Loops round each given line to print.
        #######################################################################
        # The block of code below aligns the text into the middle of the menu #
        #######################################################################
        _len = (" "*round((45-len(data_packet))/2))
        end_result = "[   {|¬"+_len+data_packet+_len+"¬|}   ]"
        split_results = end_result.split("¬")
        if(len(end_result)>59):
            end_result = split_results[0]+split_results[1][1:]+split_results[2]
        elif(len(end_result)<59):
            end_result = split_results[0]+" "+split_results[1]+split_results[2]
        else:
            end_result = split_results[0]+split_results[1]+split_results[2]
        print(end_result)
        #######################################################################
    print("[   {|"+(" "*45)+"|}   ]")
    print("[   {|>=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=<|}   ]")
    print("\n"*5)
#
def open_website(food,location):
    display([
            "Results for "+food+" in "+location+".",
            "Would you like results for","currently open restaurants?","","",
            "(0) EXIT          ","",
            "(1) YES           ","",
            "(2) NO            ","","","",""
        ])
    input2 = input("~=> ")
    while(input2 not in ["0","1","2"]): # Waits until the user inputs a valid number.
        input2 = input("~=> ")
    if input2 == "0":return  # If 0 is pressed the webbrowser module will not be called and the first menu is shown
    webbrowser.open(url_test+food+"+"+location+({"1":" open"}.get(input2)or"")) # Adds data onto the end of a url to change the search filter on google maps.
#
def location():
    locations = return_file()[1] # Opens the file list, selecting all items in the nested array.
    data = [[],["PLEASE SELECT ONE OF","THE FOLLOWING LOCATIONS",""],[],[]]
    for key in locations: # Adds all of the locations to a list accessible via the display() function
        data[1].append("")
        index = str(list(locations).index(key)+1)
        text = "("+index+") "+key
        data[1].append(text+ " "*(35-len(text)))
        data[2].append(index)
        data[3].append(key)
    display(data[1])
    input2 = input("~=> ")
    while(input2 not in data[2]):
        input2 = input("~=> ")
    data[3] = data[3][int(input2)-1]
    data[0] = locations.get(data[3])
    return data # Returns "data"; the selected location.
#
def food_type_tab(typeoffood,location_data): # Displays the type of food depending on what location was selected.
    file = return_file()[2].get(typeoffood)
    print2 = [typeoffood.upper()]
    list2 = []
    minus = 0
    for item in file:
        if item not in location_data[0]: minus+=1;continue
        index = file.index(item)+1-minus
        text = "("+str(index)+") "+item
        text = text + " "*(15-len(text))
        print2.append("")
        print2.append(text)
        list2.append(str(index))
    text = "(0) RETURN" ###### vv
    print2.append("")
    print2.append(text+ " "*(15-len(text))) # Adds another option onto the last slot in the menu with the option to EXIT/RETURN to the previous 'slide'
    list2.append("0")
    display(print2)
    input2 = input("~=> ")
    while(input2 not in list2):
        input2 = input("~=> ")
    if input2 == "0": return # Returns nothing as the menu has been exited.
    else:
        return(file[int(input2)-1]) # Returns list of food in set locations and their type.

#
#maincode#
#
for(index)in(range(3)): # Goes through a loop 3 times expecting login_details to be set to anything other than -1 which means it is logged in.
    login_details = login()
    try:
        if(login_details>-1):
            print("Successfully logged in.\n")
            break
    except:
        print("ERROR! You have entered an incorrect username/password.")
        try:
            print("You have "+["Two","One"][index]+" attempts remaining.\n")
        except:
            print("You have entered an incorrect username/password 3 times, program exitting.")
            login_details = -1
#
while(login_details!=-1): # If login_detials is set to anything other than -1 then the program has recognised that the user is logged in and they gain access to the full program.
    location_data = location()
    print(location_data)
    while(location_data):
        display([ # First display, showing each available food type
            "Welcome to the foodbot",
            "What food are you interested in?","","","",
            "(0) EXIT          ","",
            "(1) italian       ","",
            "(2) chinese       ","",
            "(3) fast food     ","",
            "(4) western food  ","","",""
        ])
        input2 = input("~=> ")
        while(input2 not in ["0","1","2","3","4"]):
            input2 = input("~=> ")
        if input2 == "0":
            print("goodbye")
            login_details=-1
            break
        chosen = food_type_tab(["italian","chinese","fast food","western food"][int(input2)-1],location_data) # Calls the food_type_tab() function expecting a value seelected from the food list.
        if not chosen: continue
        else:
            open_website(chosen,location_data[3]) # Opens the website function sending through all required data
#