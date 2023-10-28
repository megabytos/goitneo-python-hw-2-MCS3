from collections import UserDict


class CustomExeption(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidPhoneFormat(Exception):
    pass


class InvalidPhoneLegnth(Exception):
    pass


class ContactAlreadyExist(CustomExeption):
    pass


class PhoneAlreadyExist(CustomExeption):
    pass


class ContactNotFound(CustomExeption):
    pass


class PhoneNotFound(CustomExeption):
    pass


def errors_handler(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid data."
        except KeyError:
            return "Item not found."
        except InvalidPhoneLegnth:
            print("Invalid Phone Legnth")
        except InvalidPhoneFormat:
            print("Invalid Phone Format")
        except PhoneAlreadyExist as arg:
            print(f'Phone "{arg.value}" already exist ')
        except PhoneNotFound as arg:
            print(f'Phone "{arg.value}" not Found ')
        except ContactNotFound as arg:
            print(f'Contact "{arg.value}" not Found ')
        except ContactAlreadyExist as arg:
            print(f'Contact "{arg.value}" already exist ')

    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    @errors_handler
    def add_phone(self, phone):
        if self.find_phone(phone):
            raise PhoneAlreadyExist(phone)
        if len(phone) != 10:
            raise InvalidPhoneLegnth
        if not phone.isdigit():
            raise InvalidPhoneFormat
        self.phones.append(Phone(phone))

    @errors_handler
    def remove_phone(self, phone):
        if not self.find_phone(phone):
            raise PhoneNotFound(phone)
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)

    @errors_handler
    def edit_phone(self, phone, new_phone):
        if self.find_phone(new_phone):
            raise PhoneAlreadyExist(new_phone)
        for p in self.phones:
            if p.value == phone:
                p.value = new_phone

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return phone
        return False

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    @errors_handler
    def add_record(self, record):
        name = record.name.value
        if name in self.data:
            raise ContactAlreadyExist(name)
        self.data[name] = record

    @errors_handler
    def find(self, name):
        if name in self.data:
            return self.data.get(name)
        raise ContactNotFound(name)

    @errors_handler
    def delete(self, name):
        if name not in self.data:
            raise ContactNotFound(name)
        self.data.pop(name)



# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_phone("5555555555")
john_record.add_phone("5555578965412")
john_record.add_phone("55555hjgku")
john_record.remove_phone("7777777777")

# Додавання запису John до адресної книги
book.add_record(john_record)
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
bill = book.find("Marry")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")
book.delete("Bill")

