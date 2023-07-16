from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    ...


class Phone(Field):
    ...


class Birthday(Field):
    def __init__(self, date):
        super().__init__(date)

    def days_to_birthday(self):
        current_date = datetime.now().date()
        given_date = datetime.strptime(self.value, "%Y-%m-%d").date()
        delta = given_date - current_date
        return abs(delta.days)


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.birthday = Birthday(birthday) if birthday else None
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
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
            return f'{self.name}: {", ".join(str(p) for p in self.phones)} (Birthday: {self.birthday.date})'
        else:
            return f'{self.name}: {", ".join(str(p) for p in self.phones)}'


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} added"

    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i : i + n]

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
