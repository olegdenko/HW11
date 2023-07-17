from collections import UserDict
from datetime import datetime
import re


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
            'Input path for address book (Default path is "addressbook.txt"): '
        )
        if not path:
            path = "addressbook.txt"
        try:
            with open(path, "r") as file:
                lines = file.readlines()
                if not lines:
                    return "Address book file is empty."
                for line in lines:
                    values = line.strip().split(":")
                    if len(values) == 2:
                        n, p = values
                        name = Name(n)
                        phones = [Phone(phone.strip()) for phone in p.split(",")]

                        contact = Record(name, phones)
                        self.add_record(contact)
        except FileNotFoundError:
            pass
        return self

    def save_address_book(self, path=None):
        if not path:
            path = input('Input path for saving (Default path is "addressbook.txt"): ')
        if not path:
            path = "addressbook.txt"
        with open(path, "w") as file:
            for name, record in self.data.items():
                if isinstance(record, Record):
                    phones = [
                        phone.value if isinstance(phone, Phone) else str(phone)
                        for phone in record.phones
                    ]
                    phones_str = ", ".join(filter(None, phones))
                    file.write(f"{name}:{phones_str}\n")
                else:
                    file.write(f"{name}:{record}\n")

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
