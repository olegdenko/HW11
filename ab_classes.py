from collections import UserDict
from datetime import datetime, date
import re
import pickle
import itertools


class BirthdayError(Exception):
    ...


class DuplicatePhoneError(Exception):
    ...


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
            datetime.strptime(self.value, "%d-%m-%Y")
        except ValueError:
            raise BirthdayError("Invalid birthday format. Use DD-MM-YYYY format.")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.validate_birthday()

    def days_to_birthday(self):
        current_date = datetime.now().date()
        given_date = datetime.strptime(self.value, "%d-%m-%Y").date()
        next_birthday = date(current_date.year, given_date.month, given_date.day)

        if next_birthday < current_date:
            next_birthday = date(
                current_date.year + 1, given_date.month, given_date.day
            )

        delta = next_birthday - current_date
        return delta.days

    def __str__(self) -> str:
        return self.value.strftime("%d-%m-%Y")


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.birthday = Birthday(birthday) if birthday else None
        self.name = name
        self.phones = [] if phone else []
        if phone:
            self.phones.append(phone)
        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, phone: Phone):
        if not self.phones:
            self.phones.append(phone)
            return f"Phone {phone} added to contact {self.name}"

        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"Phone {phone} added to contact {self.name}"

        return f"Phone {phone} already present in contact {self.name}"

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phonebook"

    def change_birthday(self, new_birthday):
        self.birthday = Birthday(new_birthday)

    def __str__(self):
        if self.birthday:
            birthday_str = str(self.birthday)
            return f'{self.name}: {", ".join(str(p) for p in self.phones)} (Birthday: {birthday_str})'
        else:
            return f'{self.name}: {", ".join(str(p) for p in self.phones)}'


class AddressBook(UserDict):
    def __init__(self, *args, page_size=5, **kwargs):
        self.page_size = page_size
        super().__init__(*args, **kwargs)

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record.name} added"

    def del_record(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} deleted"
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

    def del_record(self, name):
        if name in self.data:
            del self.data[name]
        return f"Contact {name} does not exist in the phonebook"

    def values(self):
        return iter(self.data.values())

    def iterator(self):
        total_records = len(self.data)
        current_page = 0
        while current_page < total_records:
            yield itertools.islice(
                self.values(), current_page, current_page + self.page_size
            )
            current_page += self.page_size

    def __iter__(self):
        return iter(self.data.values())

    def __str__(self):
        return "\n".join(str(record) for record in self.data)
