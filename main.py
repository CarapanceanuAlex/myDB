from table import Table

table = Table("data.bin", "<?i46s") # we use "<" here to stop padding bytes, because it wants multiples of 4, without < it would add 3 more invisible bytes

while True:
    print("\nChoose action:\n")
    print("1. Insert")
    print("2. Select")
    print("3. Delete")
    print("4. Find by ID")
    print("5. Select all")
    print("6. Quit\n")
    choice = input("Choose an option\n")

    if choice == "1":
        id = int(input("Enter a number as ID: "))
        nameString = input("Enter the name: ")
        nameBytes = nameString.encode('utf-8')
        try:
            table.insert((id, nameBytes))
            print("\nRow added!\n")
        except ValueError as e:
            print("\nError: ", e)
    
    elif choice == "2":
        rowNr = int(input("Enter the row number to read: "))
        try:
            table.select(rowNr)
        except ValueError as e:
            print("Error: ", e)
    
    elif choice == "3":
        rowNr = int(input("Enter the ID to delete: "))
        try:
            table.delete_ID(rowNr)
        except ValueError as e:
            print("Error: ", e)

    elif choice == "4":
        targetID = int(input("Enter the ID: "))
        result = table.find_ID(targetID)
        if result is None:
            print("No row with that ID was found")
        else:
            rowID, name = result
            print("Data from ID " + str(rowID) + " is " + "\"" + name + "\"")
            
    elif choice == "5":
        try:
            table.select_all()
        except ValueError as e:
            print("Error: ", e)

    elif choice == "6":
        break

    else:
        print("\nNot a valid option!\n")