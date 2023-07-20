from collections import UserDict
from datetime import datetime
import re
import pickle
import os


class Field:
    def __init__(self, value) -> None:
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __str__(self):
        return self.value


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_phone()

    def validate_phone(self):
        if not re.match(r"^\d{7,15}$", self.value):
            raise ValueError("Invalid phone number format")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.validate_phone()

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return self.value


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.validate_birthday()

    def validate_birthday(self):
        try:
            datetime.strptime(self.value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.validate_birthday()

    def days_to_birthday(self):
        current_date = datetime.now().date()
        given_date = datetime.strptime(self.value, "%Y-%m-%d").date()
        delta = given_date - current_date
        return abs(delta.days)

    def __str__(self) -> str:
        return self.value


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.birthday = Birthday(birthday) if birthday else None
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def __hash__(self):
        return hash((self.name, tuple(self.phones)))

    def __eq__(self, other):
        return self.name == other.name and self.phones == other.phones

    def add_phone(self, phone: Phone):
        if phone.value not in [p for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to conyact {self.name}"
        return f"{phone} present in phonebook"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phonebook"

    def __str__(self):
        if self.birthday:
            return f'{self.name}: {", ".join(str(p) for p in self.phones)} (Birthday: {self.birthday.value})'
        else:
            return f'{self.name}: {", ".join(str(p) for p in self.phones)}'


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.page_size = 10  # Розмір однієї сторінки
        self.data = {}

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} added"

    def del_record(self, name: str):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted"
        else:
            return f"Contact {name} does not exist in the phonebook"

    def load_address_book(self):
        path = input(
            'Input path for address book (Default path is "addressbook.pkl"): '
        )
        if not path:
            path = "addressbook.pkl"
        try:
            with open(path, "r+b") as file:
                try:
                    self.data = pickle.load(file)
                except EOFError:
                    print(f"File '{path}' is empty. Creating an empty address book.")
                    self.data = AddressBook()
        except FileNotFoundError:
            print(f"File '{path}' not found. Creating an empty address book.")
            self.data = AddressBook()
        return self

    def save_address_book(self, path=None):
        if not path:
            path = input('Input path for saving (Default path is "addressbook.pkl"): ')
        if not path:
            path = "addressbook.pkl"
        with open(path, "wb") as file:
            pickle.dump(self.data, file)

    def iterator(self):
        records = list(self.data.values())
        total_records = len(records)
        current_page = 0
        while current_page < total_records:
            yield records[current_page : current_page + self.page_size]
            current_page += self.page_size

    def __iter__(self):
        return iter(self.data.values())

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
