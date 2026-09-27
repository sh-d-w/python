import csv

firstRow = True
dataType = ""

def selectInputType(row):
    # " + keyWord + "
    if row[0] == "datepicker":
        keyWord = row[1]
        keyPhrase = row[2]
        tags = row[3]
        print("\t<div class=\"form-group\">")
        print("\t\t<label for=\"" + keyWord + "\">" + keyPhrase + ":</label>")
        print("\t\t<input type=\"date\" name=\"" + keyWord + "\" id=\"" + keyWord + "\" " + tags + ">")
        print("\t</div>")
        print("")
    elif row[0] == "timepicker":
        keyWord = row[1]
        keyPhrase = row[2]
        tags = row[3]
        print("\t<div class=\"form-group\">")
        print("\t\t<label for=\"" + keyWord + "\">" + keyPhrase + ":</label>")
        print("\t\t<input type=\"time\" id=\"" + keyWord + "\" name=\"" + keyWord + "\" " + tags + ">")
        print("\t</div>")
        print("")
    elif row[0] == "editbox":
        keyWord = row[1]
        keyPhrase = row[2]
        tags = row[3]
        print("\t<div class=\"form-group\">")
        print("\t\t<label for=\"" + keyWord + "\">" + keyPhrase + ":</label>")
        print("\t\t<input type=\"text\" id=\"" + keyWord + "\" name=\"" + keyWord + "\" placeholder=\"" + keyPhrase + "\" " + tags + ">")
        print("\t</div>")
        print("")
    elif row[0] == "optionbox":
        keyWord = row[1]
        keyPhrase = row[2]
        tags = row[3]
        print("\t<div class=\"form-group\">")
        print("\t\t<label for=\"pestPresence\">Any Presence of Pests:</label>")
        print("\t\t<select id=\"pestPresence\" name=\"pestPresence\" " + tags + ">")

        firstItem = True
        for item in row[4:]:
            if (firstItem):
                print("\t\t\t<option value=\"\" disabled selected>" + item + "</option>")
                firstItem = False
            else:
                print("\t\t\t<option value=\"" + item + "\">" + item + "</option>")
                # <option value="item">item</option>
        print("\t\t</select>")
        print("\t</div>")
        print("")

    elif row[0] == "numberbox":
        keyWord = row[1]
        keyPhrase = row[2]
        tags = row[3]
        print("\t<div class=\"form-group\">")
        print("\t\t<label for=\"" + keyWord + "\">" + keyPhrase + ":</label>")
        print("\t\t<input type=\"number\" id=\"" + keyWord + "\" name=\"" + keyWord + "\" " + tags+ ">")
        print("\t</div>")
        print("")
    else:
        print(row)
    pass

def printType(row):
    global dataType

    if row[0] == "Form":
        endpoint = row[1]
        method = row[2]
        tags = row[3]
        dataType = "Form"
        print("<div class=\"form-container\">")
        print("<form action=\"" + endpoint + "\" method=\"" + method + "\" " + tags + ">")
    else:
        print(row)
    pass

# Open the file safely using a 'with' block
with open('inputs.csv', mode='r', newline='', encoding='utf-8') as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    
    # Optional: Skip the header row if your file has one
    # header = next(reader)
    
    # Process line by line
    for row in reader:
        if firstRow :
            printType(row)
            # dataType = "Form"
            firstRow = False
        else:
            selectInputType(row)
            # print(row)  # 'row' is a list of values, e.g., ['value1', 'value2', 'value3']

if dataType:
    print("</div>")
