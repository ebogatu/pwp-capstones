class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        return "The email address of this user has been updated to {email}".format(email = address)


    def __repr__(self):
        return "User {username}, email {email_address}, books read: {nr_of_books} ".format(username = self.name, email_address = self.email, \
        nr_of_books = len(self.books))

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating=None):
        self.books[book] = rating

    def get_average_rating(self):
        return sum([rating for rating in self.books.values() if rating is not None]) / len(self.books)


class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("The book \"{title} \" isbn has been chnaged to {isbn_value}".format(title = self.title, isbn_value=new_isbn))

    def add_rating(self, rating):
        if (rating is not None and rating >=0 and rating <= 4):
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def get_average_rating(self):
        return sum(rating for rating in self.ratings) / len(self.ratings)

    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "{title} with isbn {isbn}".format(title = self.title, isbn = self.isbn)

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)

    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email, "No user with email: {email}".format(email = email))
        if user:
            user.read_book(book, rating)
            book.add_rating(rating)
            self.books[book] = self.books.get(book, 0) + 1

    def add_user(self, name, email, user_books=None):
        if email not in self.users.keys():
            self.users[email] = User(name, email)
            if user_books is not None:
                for book in user_books:
                    self.add_book_to_user(book, email)
        else:
            print("An user with this email {email} address already exists.".format(email = email))

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)


    def most_read_book(self):
        return max(self.books, key=self.books.get)

    def highest_rated_book(self):
        hrb = max(rating.get_average_rating() for rating in self.books.keys())
        return [book for book in self.books.keys() if book.get_average_rating() == hrb]

    def most_positive_user(self):
        positive_user = None
        highest_rating = 0
        for user in self.users.values():
            avg_user_rating = user.get_average_rating()
            if avg_user_rating > highest_rating:
                positive_user = user
                highest_rating = avg_user_rating
        return positive_user
