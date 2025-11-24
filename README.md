# library-management-system-
Collection of practice projects and sample code showcasing my learning journey with Git, GitHub, and programming fundamentals. Includes simple apps, experiments, and notes, all organized for easy reuse and improvement as I build better software over time.
list_available_books():
Fetches from the database and displays the names of all books whose status is 'available'. Lets users see what books can be taken.

issue_book(student_id, student_name, book_name, issue_date, return_date):
Checks if the requested book is available. If yes, inserts a record of the issue for the student, marks the book as 'taken', and confirms the issue with return deadline.

submit_book(student_id, actual_return_date):
Looks up the issued book for the given student ID. Calculates if the book is returned late and computes fine accordingly. Updates book status to 'available' and deletes the issued record upon return.

main():
Provides a menu-driven loop for the user to view available books, issue books, return books, or exit the system with clean input handling and messages.
