from ab_classes import AddressBook, Name, Phone, Record

address_book = AddressBook()


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Invalid command"
        except TypeError:
            return "Please provide the necessary parameters"

    return wrapper


@input_error
def add_command(*args):
    name = Name(args[0])
    phones_data = args[1].split(",")
    phones = [Phone(phone.strip().replace(" ", "")) for phone in phones_data]
    rec: Record = address_book.get(str(name))
    if rec:
        for phone in phones:
            rec.add_phone(phone)
        return f"Phones {', '.join(str(phone) for phone in phones)} added to contact {rec.name}"
    rec = Record(name, phones)
    return address_book.add_record(rec)


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


def exit_command():
    address_book.save_address_book()
    return "Bye"


@input_error
def unknown_command(*args):
    return f"Unknown command: {args[0]}"


def show_all_command(*args):
    n = int(args[0]) if args else 2
    records = list(address_book)
    result = "\n".join(str(record) for record in records[:n])
    return result


@input_error
def delete_command(*args):
    if (
        args in address_book
        and "yes" == input(f"Are you sure delete {args}: Yes/No :").lower()
    ):
        address_book.del_record(args)


COMMANDS = {
    add_command: ("add", "+"),
    change_command: ("change", "зміни"),
    exit_command: ("bye", "exit", "end"),
    show_all_command: ("show all", "покажи все"),
    delete_command: ("del", "delete", "видали"),
}


def parser(text):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd) :].strip().split()
                return cmd, data
    return unknown_command, [text]


def main():
    address_book.load_address_book()
    while True:
        user_input = input("Wait...>")

        cmd, data = parser(user_input)

        result = cmd(*data)
        print(result)

        if cmd == exit_command:
            break


if __name__ == "__main__":
    main()
