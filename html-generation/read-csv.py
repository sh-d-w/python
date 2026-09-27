import csv

# Open the file safely using a 'with' block
with open('inputs.csv', mode='r', newline='', encoding='utf-8') as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    
    # Optional: Skip the header row if your file has one
    # header = next(reader)
    
    # Process line by line
    for row in reader:
        print(row)  # 'row' is a list of values, e.g., ['value1', 'value2', 'value3']
