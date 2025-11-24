import sqlite3
from datetime import datetime

# SQLite database se connection banao
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

def list_available_books():
    """
    Library me available sabhi kitabon ke naam dikhayein.
    """
    cursor.execute("SELECT book_name FROM books WHERE status='available'")
    books = cursor.fetchall()

    if not books:
        print("\nNo book available.")
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
        print(f"Book '{book_name}' issued to {student_name} (ID: {student_id}). Return by {return_date}.")
    else:
        print("Book not available for issue.")

def submit_book(student_id, actual_return_date):
    
    cursor.execute("SELECT book_name, return_date FROM student WHERE student_id=?", (student_id,))
    record = cursor.fetchone()

    if record:
        book_name, expected_return_date = record
        try:
            expected_dt = datetime.strptime(expected_return_date, "%Y-%m-%d")
            actual_dt = datetime.strptime(actual_return_date, "%Y-%m-%d")
        except ValueError:
            print("Please enter dates in YYYY-MM-DD format.")
            return

        days_late = (actual_dt - expected_dt).days
        if days_late > 0:
            fine = days_late * 30
            print(f"Book returned {days_late} days late. Fine: Rs {fine}")
        else:
            print("Book returned on time. No fine.")

        cursor.execute("UPDATE books SET status = 'available' WHERE book_name=?", (book_name,))
        cursor.execute("DELETE FROM student WHERE student_id=?", (student_id,))
        conn.commit()
        print(f"Book '{book_name}' returned successfully.")
    else:
        print("No issued book found for this student ID.")

def main():
    while True:
        print("\nPress 1 for available books")
        print("Press 2 for issue book")
        print("Press 3 for submission (return book)")
        print("Press 4 to exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            list_available_books()
        elif choice == '2':
            try:
                sid = int(input("Enter student ID: "))
            except ValueError:
                print("Student ID should be a number.")
                continue
            sname = input("Enter student name: ").strip()
            bname = input("Enter book name to issue: ").strip()
            issue_d = input("Enter issue date (YYYY-MM-DD): ").strip()
            return_d = input("Enter return date (YYYY-MM-DD): ").strip()
            issue_book(sid, sname, bname, issue_d, return_d)
        elif choice == '3':
            try:
                sid = int(input("Enter student ID for return: "))
            except ValueError:
                print("Student ID should be a number.")
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

