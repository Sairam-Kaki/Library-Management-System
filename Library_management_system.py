
import psycopg2

class Book:
    # Initailizing a book object with required data
    
    def __init__(self, title, author, isbn, publisher, subject, category, tags, description):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publisher = publisher
        self.subject = subject
        self.category = category
        self.tags = tags
        self.description = description

    # To return a string representation of the Book
    def __str__(self):
        return f"Title: {self.title}\nAuthor: {self.author}\nISBN: {self.isbn}\nPublisher: {self.publisher}\nSubject: {self.subject}\nCategory: {self.category}\nTags: {self.tags}\nDescription: {self.description}"

class Library:
    
    # Initializing the Library object and connecting it to the database
    # A table "books" is created if not existed before
    
    def __init__(self):
        self.conn = psycopg2.connect("dbname='library' user='postgres' password='your_password_here' host='localhost' port='5432'")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS books (id SERIAL PRIMARY KEY, title VARCHAR(255), author VARCHAR(255), isbn VARCHAR(255), publisher VARCHAR(255), subject VARCHAR(255), category VARCHAR(255), tags VARCHAR(255), description TEXT)")
        self.conn.commit()

    # Inserts a book into the books table
    def insert_book(self, book):
        self.cur.execute("INSERT INTO books (title, author, isbn, publisher, subject, category, tags, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (book.title, book.author, book.isbn, book.publisher, book.subject, book.category, book.tags, book.description))
        self.conn.commit()

    #Shows Available Books
    def available_books(self):
        query = "SELECT title FROM books;"
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result
        
    # Searches the required book matching the given data if existed
    def search_books(self, title=None, author=None, isbn=None, tags=None):
        query = "SELECT * FROM books WHERE "
        params = []
        conditions = []
        if author:
            conditions.append("author ILIKE %s")
            params.append(f"%{author}%")
        if isbn:
            conditions.append("isbn ILIKE %s")
            params.append(f"%{isbn}%")
        if tags:
            conditions.append("tags ILIKE %s")
            params.append(f"%{tags}%")
        if title:
            conditions.append("title ILIKE %s")
            params.append(f"%{title}%")
        if conditions:
            query += " OR ".join(conditions)
            query += "ORDER BY 1;"
            self.cur.execute(query, params)
            result = self.cur.fetchall()
            return result
        else:
            return None

    # to modify the book which is already existed in the table
    def update_book(self, book_id, title=None, author=None, isbn=None, publisher=None, subject=None, category=None, tags=None, description=None):
        query = f"UPDATE books SET "
        params = []
        conditions = []
        if title:
            conditions.append("title = %s")
            params.append(title)
        if author:
            conditions.append("author = %s")
            params.append(author)
        if isbn:
            conditions.append("isbn = %s")
            params.append(isbn)
        if publisher:
            conditions.append("publisher = %s")
            params.append(publisher)
        if subject:
            conditions.append("subject = %s")
            params.append(subject)
        if category:
            conditions.append("category = %s")
            params.append(category)
        if tags:
            conditions.append("tags = %s")
            params.append(tags)
        if description:
            conditions.append("description = %s")
            params.append(description)
        if conditions:
            query += ", ".join(conditions) + " WHERE id = %s"
            params.append(book_id)
            self.cur.execute(query, params)
            self.conn.commit()
            return True
        else:
            return None

    # Deletes a book from the table
    def delete_book(self, book_id):
        query = "DELETE FROM books WHERE id = %s"
        self.cur.execute(query, (book_id,))
        self.conn.commit()

def main():
    library = Library()

    print("\nWelcome to the Library!\n")
    
    while True:
        
        # Showing the options available to the user
        print("1. Insert a book")
        print("2. Update a book")
        print("3. Delete a book")
        print("4. See available books")
        print("5. Search for a book")
        print("6. Exit")
        
        choice = input("Enter your choice: ")

        # Collects the required data to insert a book into table
        if choice == "1":
            title = input("\nEnter the title of the book: ")
            author = input("Enter the author of the book: ")
            isbn = input("Enter the ISBN of the book: ")
            publisher = input("Enter the publisher of the book: ")
            subject = input("Enter the subject of the book: ")
            category = input("Enter the category of the book: ")
            tags = input("Enter the tags of the book: ")
            description = input("Enter the description of the book: ")
            book = Book(title, author, isbn, publisher, subject, category, tags, description)
            library.insert_book(book)
            print("\nBook added successfully!\n")
        
        # Asks the user what data to be updated for the book and updates it 
        elif choice == "2":
            book_id = input("\nEnter the ID of the book to update: ")
            title = input("Enter the new title of the book: ")
            author = input("Enter the new author of the book: ")
            isbn = input("Enter the new ISBN of the book: ")
            publisher = input("Enter the new publisher of the book: ")
            subject = input("Enter the new subject of the book: ")
            category = input("Enter the new category of the book: ")
            tags = input("Enter the new tags of the book: ")
            description = input("Enter the new description of the book: ")
            if library.update_book(book_id, title, author, isbn, publisher, subject, category, tags, description):
                print("\nBook updated successfully!")
            else:
                print("\nInvalid book ID!")
        
        # Deletes the book according to the given ID from user
        elif choice == "3":
            book_id = input("\nEnter the ID of the book to delete: ")
            library.delete_book(book_id)
            print("\nBook deleted successfully!")
        
        #Shows the books available
        elif choice == "4":
            print()
            num = 1
            for book in library.available_books():
                print(f"{num}-{book[0]}")
                num+=1
            print()
        
        # searches for the book against user's given data 
        elif choice == "5":
            print("\nPlease enter atleast one detail and you can skip the rest.\n")
            
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            isbn = input("Enter the ISBN of the book: ")
            tags = input("Enter the tags of the book: ")
            result = library.search_books(title, author, isbn, tags)
            if result:
                num = 1
                data = ["Book id","Title", "Author", "ISBN", "Publisher", "Subject", "Category", "Tags", "Description"]
                print()
                for book in result:
                    print("Book - ",num,end=":\n")
                    num+=1
                    for i in range(9):
                        print(f"{data[i]}: {book[i]}")
                    print()    
            else:
                print("\nNo books found!\nPlease check your spellings and try again.\n")
            
        # Exits
        elif choice == "6":
            library.conn.close()
            print("\nThank you for visiting, Have a nice day!\n")
            break
        
        # Asks user for a valid choice
        else:
            print("\nInvalid choice! Please try again.\n")

if __name__ == "__main__":
    main()