import pickle

class Person:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name


class Librarian(Person):
    def show_menu(self):
        print("\nБиблиотекарь")
        print("1. Добавить книгу")
        print("2. Удалить книгу") 
        print("3. Добавить пользователя")
        print("4. Список пользователей")
        print("5. Список книг")
        print("0. Выход")


class User(Person):
    def __init__(self, name):
        super().__init__(name)
        self._books = []

    def get_books(self):
        return self._books[:]

    def add_book(self, book):
        self._books.append(book)

    def remove_book(self, book):
        if book in self._books:
            self._books.remove(book)

    def show_menu(self):
        print("\nПользователь")
        print("1. Доступные книги")
        print("2. Взять книгу")
        print("3. Вернуть книгу")
        print("4. Мои книги")
        print("0. Выход")


class Book:
    def __init__(self, title, author):
        self._title = title
        self._author = author
        self._status = "доступна"

    def is_free(self):
        return self._status == "доступна"

    def set_status(self, status):
        self._status = status

    def get_title(self):
        return self._title

    def get_author(self):
        return self._author

    def __repr__(self):
        return f"Book('{self._title}', '{self._author}', '{self._status}')"


class Library:
    FILE_NAME = "celka.pkl"

    def __init__(self):
        self._books = []
        self._users = []
        self._current = None
        self._load()

    def _load(self):
        try:
            with open(self.FILE_NAME, "rb") as f:
                saved = pickle.load(f)
                self._books = saved._books
                self._users = saved._users
        except (FileNotFoundError, EOFError, pickle.PickleError):
            pass

    def _save(self):
        try:
            with open(self.FILE_NAME, "wb") as f:
                pickle.dump(self, f)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def librarian_menu(self):
        lib = self._current
        while True:
            lib.show_menu()
            c = input(">> ")
            if c == "1":
                t = input("Название: ")
                a = input("Автор: ")
                self._books.append(Book(t, a))
                print("Книга добавлена.")
            elif c == "2":
                t = input("Название для удаления: ").strip()
                if not t:
                    print("Нет названия.")
                    continue
                found = False
                for i, b in enumerate(self._books):
                    if b.get_title().lower() == t.lower():
                        self._books.pop(i)
                        print("Книга удалена.")
                        found = True
                        break
                if not found:
                    print("Книга не найдена.")
            elif c == "3":
                name = input("Имя пользователя: ").strip()
                if name:
                    if any(u.get_name().lower() == name.lower() for u in self._users):
                        print("Такой пользователь уже есть.")
                    else:
                        self._users.append(User(name))
                        print("Пользователь добавлен.")
                else:
                    print("Имя не указано.")
            elif c == "4":
                if self._users:
                    print("Пользователи:", [u.get_name() for u in self._users])
                else:
                    print("Пользователей нет.")
            elif c == "5":
                if self._books:
                    print("Книги:")
                    for b in self._books:
                        print(f"  \"{b.get_title()}\" — {b._status}")
                else:
                    print("Книг нет.")
            elif c == "0":
                break
            else:
                print("Неверная команда.")
            input("Enter...")

    def user_menu(self):
        user = self._current
        while True:
            user.show_menu()
            c = input(">> ")
            if c == "1":
                free = [b.get_title() for b in self._books if b.is_free()]
                if free:
                    print("Доступные книги:", free)
                else:
                    print("Нет доступных книг.")
            elif c == "2":
                t = input("Название книги: ").strip()
                if not t:
                    print("Нет названия.")
                    continue
                for b in self._books:
                    if b.get_title().lower() == t.lower() and b.is_free():
                        b.set_status("выдана")
                        user.add_book(b.get_title())
                        print(f"Книга \"{t}\" выдана.")
                        break
                else:
                    print("Книга не найдена или занята.")
            elif c == "3":
                t = input("Название книги для возврата: ").strip()
                books = user.get_books()
                if t not in books:
                    print("У вас нет такой книги.")
                else:
                    user.remove_book(t)
                    for b in self._books:
                        if b.get_title().lower() == t.lower():
                            b.set_status("доступна")
                            print("Книга возвращена.")
                            break
            elif c == "4":
                my_books = user.get_books()
                if my_books:
                    print("Ваши книги:", my_books)
                else:
                    print("У вас нет книг.")
            elif c == "0":
                break
            else:
                print("Неверная команда.")
            input("Enter...")

    def run(self):
        while True:
            print("\n1. Библиотекарь\n2. Пользователь\n0. Выход")
            c = input(">> ").strip()
            if c == "1":
                name = input("Имя библиотекаря: ").strip()
                if name:
                    self._current = Librarian(name)
                    self.librarian_menu()
                else:
                    print("Имя не указано.")
            elif c == "2":
                name = input("Имя пользователя: ").strip()
                if not name:
                    print("Имя не указано.")
                    continue
                matched = None
                for u in self._users:
                    if u.get_name().lower() == name.lower():
                        matched = u
                        break
                if matched:
                    self._current = matched
                    self.user_menu()
                else:
                    print("Пользователь не найден. Зарегистрируйтесь у библиотекаря.")
            elif c == "0":
                print("Сохранение данных...")
                self._save()
                print("Выход из программы.")
                break
            else:
                print("Неверный пункт меню.")


lib = Library()
lib.run()

