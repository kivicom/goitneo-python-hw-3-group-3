"""
This module provides a contact management system including classes for storing contact information,
managing an address book, and performing operations like adding, deleting, and editing contacts,
as well as setting and retrieving birthdays.
"""

from datetime import datetime, timedelta
from collections import defaultdict

class Field:
    """Base class for record fields"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """A class for storing a contact name. Mandatory field."""

class Phone(Field):
    """A class for storing a phone number. Has format validation (at least 10 digits)."""
    def __init__(self, value):
        if (len(value) < 10 or len(value) > 12) or not value.isdigit():
            raise ValueError("Phone number must be 10 or 12 digits long.")
        super().__init__(value)

class Birthday(Field):
    """Class for storing birthday. Has format validation (DD.MM.YYYY)."""
    def __init__(self, date_str):
        super().__init__(date_str)
        # Converting a date string to a datetime.date object
        if date_str:
            try:
                self.date = datetime.strptime(self.value, "%d.%m.%Y").date()
            except ValueError as exc:
                raise ValueError("Invalid birthday format. Use DD.MM.YYYY.") from exc
        else:
            self.date = None

    def __str__(self):
        return self.date.strftime("%d.%m.%Y") if self.date else "No birthday set"


class Record:
    """A class to hold information about a contact, including name, phone number, and birthday."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        """Adding a phone to a record"""
        self.phones.append(Phone(phone))

    def delete_phone(self, phone):
        """Deleting a phone from the record"""
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        """Editing a phone in a recording"""
        for p in self.phones:
            if str(p) == old_phone:
                p.value = new_phone

    def add_birthday(self, birthday):
        """Adding a birthday to a record"""
        self.birthday = Birthday(birthday)

    def __str__(self):
        """Representation of the record as a string"""
        phones_str = "; ".join(str(p) for p in self.phones)
        birthday_str = str(self.birthday) if self.birthday else "Not specified"
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {birthday_str}"

class AddressBook:
    """A class for storing and managing records"""
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        """Adding a new entry to the contact book"""
        self.data[record.name.value] = record

    def delete_record(self, name):
        """Deleting an entry by name from the contact book"""
        if name in self.data:
            del self.data[name]

    def find(self, name):
        """Search for a record by name"""
        return self.data.get(name)

    def get_birthdays_per_week(self):
        """We are creating a dictionary to store usernames by day of the week"""
        birthdays_per_week = defaultdict(list)
        today = datetime.today().date()
        one_week_ahead = today + timedelta(days=7)

        for record in self.data.values():
            name = record.name.value

            if record.birthday:
                birthday_this_year = record.birthday.date.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                if today <= birthday_this_year <= one_week_ahead:
                    if birthday_this_year.weekday() >= 5:  # Субота або неділя
                        birthday_weekday = "Monday"
                    else:
                        birthday_weekday = birthday_this_year.strftime("%A")

                    birthdays_per_week[birthday_weekday].append(name)

        return dict(birthdays_per_week)

    def __str__(self):
        """Representation of the contact book as a string"""
        return "\n".join(str(record) for record in self.data.values())

class Contact:
    """Main class for managing contact operations in an address book."""
    def __init__(self):
        self.address_book = AddressBook()

    def add_contact(self, name, phone):
        """add contact"""
        record = Record(name)
        record.add_phone(phone)
        self.address_book.add_record(record)
        print("Contact added successfully.")

    def change_phone(self, name, new_phone):
        """change phone"""
        record = self.address_book.find(name)
        if record:
            record.edit_phone(record.phones[0].value, new_phone)
            print("Phone number changed successfully.")
        else:
            print("Contact not found.")

    def show_phone(self, name):
        """show phone"""
        record = self.address_book.find(name)
        if record:
            print(f"Phone number for {name}: {record.phones[0]}")
        else:
            print("Contact not found.")

    def add_birthday(self, name, birthday):
        """add birthday"""
        record = self.address_book.find(name)
        if record:
            record.add_birthday(birthday)
            print("Birthday added successfully.")
        else:
            print("Contact not found.")

    def show_birthday(self, name):
        """show birthday"""
        record = self.address_book.find(name)
        if record and record.birthday:
            print(f"Birthday for {name}: {record.birthday}")
        elif record and not record.birthday:
            print(f"No birthday specified for {name}.")
        else:
            print("Contact not found.")

    def birthdays_this_week(self):
        """birthdays this week"""
        birthdays_per_week = self.address_book.get_birthdays_per_week()
        if birthdays_per_week:
            print("Birthdays for the next week:")
            for day, users in birthdays_per_week.items():
                print(f"{day}: {', '.join(users)}")
        else:
            print("No birthdays for the next week.")

    def list_all_contacts(self):
        """list all contacts"""
        print("All contacts in the address book:")
        print(self.address_book)

    def hello(self):
        """Say hello"""
        print("Hello! I'm your address book bot.")
