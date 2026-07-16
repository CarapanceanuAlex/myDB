from table import Table

table = Table("data.bin", "<?i46s") # we use "<" here to stop padding bytes, because it wants multiples of 4, without < it would add 3 more invisible bytes

while True:
    print("\nChoose action:\n")
    print("1. Insert row")
    print("2. Read row")
    print("3. Delete row")
    print("4. Quit\n")
    choice = input("Choose an option\n")

    if choice == "1":
        id = int(input("Enter a number as ID: "))
        nameString = input("Enter a name: ")
        nameBytes = nameString.encode('utf-8')
        table.insert((id, nameBytes))
        print("\nRow added!\n")
    
    elif choice == "2":
        rowNr = int(input("Enter the row number to read: "))
        try:
            table.select(rowNr)
        except ValueError as e:
            print("Error: ", e)
    
    elif choice == "3":
        rowNr = int(input("Enter the row to delete: "))
        try:
            table.delete(rowNr)
        except ValueError as e:
            print("Error: ", e)

    elif choice == "4":
        break

    else:
        print("\nNot a valid option!\n")