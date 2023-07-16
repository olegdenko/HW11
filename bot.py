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
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
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


@input_error
def exit_command(*args):
    return "Bye"


@input_error
def unknown_command(*args):
    pass


@input_error
def show_all_command(*args):
    return address_book


@input_error
def delete_command(*args):
    pass


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
                # print(cmd)
                data = text[len(kwd) :].strip().split()
                return cmd, data
    return unknown_command, []


def main():
    while True:
        user_input = input("Wait...>")

        cmd, data = parser(user_input)

        result = cmd(*data)
        print(result)

        if cmd == exit_command:
            break


if __name__ == "__main__":
    main()
