"""
This script serves as the user interface for interacting with the contact management system.
It allows the user to add, change, and display contacts, add and show birthdays,
list upcoming birthdays within a week, list all contacts, and greet the user.
Commands are entered interactively, and the script processes these commands,
calling appropriate methods from the Contact class to perform requested actions.
"""

from classes import Contact

def main():
    """main"""
    contact = Contact()
    while True:
        command = input("Enter command: ").strip().lower()
        if command == "add":
            name = input("Enter contact name: ").strip()
            phone = input("Enter contact phone: ").strip()
            contact.add_contact(name, phone)
        elif command == "change":
            name = input("Enter contact name: ").strip()
            new_phone = input("Enter new phone number: ").strip()
            contact.change_phone(name, new_phone)
        elif command == "phone":
            name = input("Enter contact name: ").strip()
            contact.show_phone(name)
        elif command == "add-birthday":
            name = input("Enter contact name: ").strip()
            birthday = input("Enter birthday (DD.MM.YYYY): ").strip()
            contact.add_birthday(name, birthday)
        elif command == "show-birthday":
            name = input("Enter contact name: ").strip()
            contact.show_birthday(name)
        elif command == "birthdays":
            contact.birthdays_this_week()
        elif command == "all":
            contact.list_all_contacts()
        elif command == "hello":
            contact.hello()
        elif command == "close" or command == "exit":
            print("Exiting program...")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
