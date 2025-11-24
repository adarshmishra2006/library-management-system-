import sqlite3
from datetime import datetime

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

def list_available_books():
    """
    Show all books currently available in the library.
    """
    cursor.execute("SELECT book_name FROM books WHERE status='available'")
    books = cursor.fetchall()

    if not books:
        print("\nNo books are available right now.")
        return

    print("\nAvailable Books:")
    for book in books:
        print(f" - {book[0]}")

def issue_book(student_id, student_name, book_name, issue_date, return_date):
    cursor.execute("SELECT status FROM books WHERE book_name=?", (book_name,))
    status = cursor.fetchone()

    if status and status[0] == 'available':
        cursor.execute('''
            INSERT INTO student (student_id, student_name, book_name, issue_date, return_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, student_name, book_name, issue_date, return_date))
        cursor.execute("UPDATE books SET status = 'taken' WHERE book_name=?", (book_name,))
        conn.commit()
        print(f"Book '{book_name}' has been issued to {student_name} (ID: {student_id}). Please return by {return_date}.")
    else:
        print("Sorry, this book is currently not available for issue.")

def submit_book(student_id, actual_return_date):
    cursor.execute("SELECT book_name, return_date FROM student WHERE student_id=?", (student_id,))
    record = cursor.fetchone()

    if record:
        book_name, expected_return_date = record
        try:
            expected_dt = datetime.strptime(expected_return_date, "%Y-%m-%d")
            actual_dt = datetime.strptime(actual_return_date, "%Y-%m-%d")
        except ValueError:
            print("Please enter dates in the correct format: YYYY-MM-DD.")
            return

        days_late = (actual_dt - expected_dt).days
        if days_late > 0:
            fine = days_late * 30
            print(f"The book was returned {days_late} days late. Your fine is Rs {fine}.")
        else:
            print("Thank you for returning the book on time. No fine charged.")

        cursor.execute("UPDATE books SET status = 'available' WHERE book_name=?", (book_name,))
        cursor.execute("DELETE FROM student WHERE student_id=?", (student_id,))
        conn.commit()
        print(f"Book '{book_name}' has been successfully returned.")
    else:
        print("No book issued under this student ID was found.")

def main():
    while True:
        print("\nPress 1 to view available books")
        print("Press 2 to issue a book")
        print("Press 3 to return a book")
        print("Press 4 to exit")

        choice = input("Please enter your choice: ").strip()
        if choice == '1':
            list_available_books()
        elif choice == '2':
            try:
                sid = int(input("Enter student ID: "))
            except ValueError:
                print("Student ID must be a number.")
                continue
            sname = input("Enter student name: ").strip()
            bname = input("Enter the book name to issue: ").strip()
            issue_d = input("Enter issue date (YYYY-MM-DD): ").strip()
            return_d = input("Enter expected return date (YYYY-MM-DD): ").strip()
            issue_book(sid, sname, bname, issue_d, return_d)
        elif choice == '3':
            try:
                sid = int(input("Enter student ID for book return: "))
            except ValueError:
                print("Student ID must be a number.")
                continue
            actual_return_date = input("Enter actual return date (YYYY-MM-DD): ").strip()
            submit_book(sid, actual_return_date)
        elif choice == '4':
            print("Thank you for using the Library Management System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    conn.close()
