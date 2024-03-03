'''Author: Sara Yasser Ahmed Meshrif
Description: This code outlines a program that manages student records, news articles, and courses using an SQLite database.
Each function handles different aspects of the program, such as adding/removing students, managing courses, and displaying news.
The main menus provide options for control users and student users to interact with the system.
'''

import sqlite3
import sys

# Establish a connection to the SQLite database
with sqlite3.connect('student.db') as conn:
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Create tables if they don't already exist: students, news, and courses
    cursor.execute('''CREATE TABLE IF NOT EXISTS students
                   (id TEXT, name TEXT NOT NULL, grade INTEGER, gpa INTEGER,courses TEXT, password TEXT, group_type INTEGER)
                   ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS news
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL)
                   ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS courses
                    (id INTEGER PRIMARY KEY,name TEXT UNIQUE)
                ''')

    # Function to add a new student to the database
    def add_student():
        while True:
            id = input("\nEnter student ID: ").strip()
            if not id:
                print("\nID cannot be empty. Please try again.")
                continue
            cursor.execute('SELECT * FROM students WHERE id = ?', (id))
            existing_student = cursor.fetchone()
            if existing_student:
                print(f"\nStudent with ID {id} already exists. Please enter a different ID.")
            else:
                break

        while True:
            name = input("Enter student name: ").strip()
            if not name:
                print("\nName cannot be empty. Please try again.")
                continue
            break

        while True:
            grade = input("Enter student grade: ").strip()
            if not grade:
                print("\nGrade cannot be empty. Please try again.")
                continue
            try:
                grade = int(grade)
                if not 1 <= grade <= 5:
                    print("Invalid grade. Please enter a value between 1 and 5.")
                    continue
                break
            except ValueError:
                print("Invalid grade. Please enter an integer value.")

        while True:
            gpa = input("Enter student GPA: ").strip()
            if not gpa:
                print("\nGPA cannot be empty. Please try again.")
                continue
            try:
                gpa = float(gpa)
                if not 0.0 <= gpa <= 4.0:
                    print("Invalid GPA. Please enter a value between 0.0 and 4.0.")
                    continue
                break
            except ValueError:
                print("Invalid GPA. Please enter a numeric value.")
                continue

        while True:
            password = input("Enter student password: ").strip()
            if not password:
                print("\nPassword cannot be empty. Please try again.")
                continue
            break

        cursor.execute('INSERT INTO students (id, name, grade, gpa, password) VALUES (?, ?, ?, ?, ?)',
                    (id, name, grade, gpa, password))
        conn.commit()
        print(f"\nStudent '{name}' added successfully!")

        while True:
            print("\nA) Add another student\nB) Exit")
            choice = input("\nEnter your choice: ").upper()
            if choice == 'A':
                add_student()
            elif choice == 'B':
                return
            else:
                print("\nInvalid choice. Please enter 'A' or 'B'.")

    # Function to remove a student from the database
    def remove_student():
        while True:
            student_id = input("\nEnter the student ID you want to remove (type 'exit' to cancel): ")
            if student_id.lower() == 'exit':
                print("\nRemoval canceled.")
                break

            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            student = cursor.fetchone()

            if student:
                while True:
                    print("\nA) Yes, remove the student\nB) No, Do not remove the student")
                    confirmation = input(f"\nAre you sure you want to remove the student '{student[1]}'?: ").upper()
                    if confirmation == 'A':
                        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
                        conn.commit()
                        print(f"\nStudent ID {student_id} removed successfully!")
                        break
                    elif confirmation == 'B':
                        print("\nRemoval canceled.")
                        break
                    else:
                        print("\nInvalid choice. Please enter 'A' or 'B'.")
                while True:
                    print("\nA) Yes\nB) No")
                    choice = input("\nDo you want to remove another student?: ").upper()
                    if choice == 'A':
                        break
                    elif choice == 'B':
                        return
                    else:
                        print("\nInvalid choice. Please enter 'A' or 'B'.")
            else:
                print(f"\nNo student found with ID {student_id}. Please enter a valid ID or type 'exit' to cancel.")

    # Function to update student information
    def update_student():
        valid_fields = ['ID', 'Name', 'Grade', 'GPA', 'Password']
        exit_flag = False
        same_student_flag = False

        while not exit_flag:
            if not same_student_flag:
                while True:
                    student_id = input("\nEnter the student ID you want to update (type 'exit' to cancel): ").strip().lower()
                    if student_id == 'exit':
                        print("\nUpdate process is cancelled")
                        return

                    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
                    student = cursor.fetchone()

                    if student:
                        print(f"\nCurrent Information for Student ID {student[0]}:")
                        print(f"\nName of the student: {student[1]}\nGrade of the student: {student[2]}\nGPA of the student: {student[3]}\nCourses registered: {student[4]} \nPassword: {student[5]}\nGroup Type: {student[6]}")
                        break
                    else:
                        print(f"\nNo student found with ID {student_id}. Please enter a valid ID or type 'exit' to cancel.")

            while True:
                print("\nChoose a field to update:")
                for i, field in enumerate(valid_fields, 1):
                    print(f"{i}. {field}")

                try:
                    choice_index = int(input("\nEnter the number corresponding to the field you want to update: ")) - 1

                    if 0 <= choice_index < len(valid_fields):
                        field_to_update = valid_fields[choice_index]
                        while True:
                            try:
                                if field_to_update == 'ID':
                                    new_value = input(f"\nEnter the new value for {field_to_update}: ")
                                    new_id = new_value
                                    cursor.execute('SELECT * FROM students WHERE id = ?', (new_id,))
                                    existing_student = cursor.fetchone()
                                    if existing_student:
                                        raise ValueError(f"\nAnother student with ID {new_id} already exists. Please enter a different ID.")
                                    else:
                                        cursor.execute('UPDATE students SET "ID" = ? WHERE id = ?', (new_id, student_id))
                                        conn.commit()
                                        print(f"\nStudent ID updated successfully!")
                                        student_id = new_id
                                        break
                                elif field_to_update == 'GPA':
                                    while True:
                                        new_value = input(f"\nEnter the new value for {field_to_update}: ")
                                        try:
                                            new_gpa = float(new_value)
                                            if 0.0 <= new_gpa <= 4.0:
                                                cursor.execute(f'UPDATE students SET "{field_to_update}" = ? WHERE id = ?', (new_gpa, student_id))
                                                conn.commit()
                                                print(f"\nStudent {field_to_update} updated successfully!")
                                                successfull_update = True
                                                break
                                            else:
                                                raise ValueError ("\nInvalid GPA. Please enter a value between 0.0 and 4.0.")
                                        except ValueError:
                                            print("\nInvalid GPA. Please enter a value between 0.0 and 4.0.")
                                            continue
                                    if successfull_update:
                                        break

                                elif field_to_update == 'Grade':
                                    while True:
                                        new_value = input(f"\nEnter the new value for {field_to_update}: ")
                                        try:
                                            new_grade = int(new_value)
                                            if 1 <= new_grade <= 5:
                                                cursor.execute(f'UPDATE students SET "{field_to_update}" = ? WHERE id = ?', (new_grade, student_id))
                                                conn.commit()
                                                print(f"\nStudent {field_to_update} updated successfully!")
                                                successfull_update = True
                                                break
                                            else:
                                                raise ValueError ("\nInvalid grade. Please enter a value between 1 and 5.")
                                        except ValueError:
                                            print("\nInvalid grade. Please enter a value between 1 and 5.")
                                            continue
                                    if successfull_update:
                                        break

                                else:
                                    new_value = input(f"\nEnter the new value for {field_to_update}: ")
                                    cursor.execute(f'UPDATE students SET "{field_to_update}" = ? WHERE id = ?', (new_value, student_id))
                                    conn.commit()
                                    print(f"\nStudent ID {student_id} updated successfully!")
                                    break
                            except ValueError as ve:
                                print(str(ve))
                            except Exception as e:
                                print(f"\nError occurred: {str(e)}")
                        break
                    else:
                        print("\nInvalid choice. Please enter a valid number.")
                except ValueError:
                    print("\nInvalid choice. Please enter a valid number.")
                except Exception as e:
                    print(f"\nError occurred: {str(e)}")
            while True:
                print("\nA) Update another field for the same student\nB) Update another student\nC) I'm done updating students")
                choice = input("\nEnter your choice: ").upper()
                if choice == 'A':
                    same_student_flag = True
                    break
                elif choice == 'B':
                    same_student_flag = False
                    break
                elif choice == 'C':
                    exit_flag = True
                    break
                else:
                    print("\nInvalid choice. Please enter 'A', 'B', or 'C'.")


    def get_all_students():
        cursor.execute('SELECT * FROM students')
        students = cursor.fetchall()
        return students

    # Function to display information of a specific student
    def get_all_info():
        while True:
            while True:
                student_id = input("\nEnter the student ID to retrieve information (type 'exit' to cancel): ")
                if student_id.lower() == 'exit':
                    print("\nInformation retrieval canceled.")
                    return

                cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
                student = cursor.fetchone()

                if student:
                    print(f"\nInformation for Student ID {student[0]}:")
                    print(f"\nName of the student: {student[1]}\nGrade of the student: {student[2]}\nGPA of the student: {student[3]}\nCourses registered: {student[4]} \nPassword: {student[5]}\nGroup Type: {student[6]}")
                    break
                else:
                    print(f"\nNo student found with ID {student_id}. Please enter a valid ID.")

            while True:
                print("\nA) Yes\nB) No")
                choice = input("\nDo you want to retrieve information for another student?: ").upper()
                if choice == 'A':
                    break
                elif choice == 'B':
                    return
                else:
                    print("Invalid choice. Please enter 'A' or 'B'.")



    def add_news():
        while True:
            news_content = input("\nEnter the news content (type 'exit' to cancel): ")
            if news_content.lower() == 'exit':
                print("\nAdding news canceled.")
                break
            elif not news_content.strip():
                print("\nNews content cannot be empty. Please enter some text.")
                continue

            cursor.execute('INSERT INTO news (content) VALUES (?)', (news_content,))
            conn.commit()
            print("\nNews added successfully!")

            while True:
                print("\nA) Yes\nB) No\n")
                another_news = input("\nDo you want to add another news article?: ").upper()
                if another_news == 'A':
                    break
                elif another_news == 'B':
                    return
                else:
                    print("\nInvalid choice. Please enter 'A' or 'B'.")

    def remove_news():
        while True:
            news_id = input("\nEnter the news ID you want to remove (type 'exit' to cancel): ")
            if news_id.lower() == 'exit':
                print("\nRemoval canceled.")
                break

            cursor.execute('SELECT * FROM news WHERE id = ?', (news_id,))
            news = cursor.fetchone()

            if news:
                while True:
                    print("\nA) Yes, remove the news\nB) No, Do not remove the news")
                    confirmation = input(f"\nAre you sure you want to remove the news with ID {news_id}?: ").upper()
                    if confirmation == 'A':
                        cursor.execute('DELETE FROM news WHERE id = ?', (news_id,))
                        conn.commit()
                        print(f"\nNews with ID {news_id} removed successfully!")
                        break
                    elif confirmation == 'B':
                        print("\nRemoval canceled.")
                        break
                    else:
                        print("\nInvalid choice. Please enter 'A' or 'B'.")
            else:
                print(f"\nNo news found with ID {news_id}. Please enter a valid ID or type 'exit' to cancel.")

    def get_all_news():
        cursor.execute('SELECT * FROM news')
        news_list = cursor.fetchall()
        return news_list

    def add_course():
        while True:
            course_name = input("\nEnter the name of the course to add (type 'exit' to cancel): ").strip()
            if course_name.lower() == 'exit':
                print("\nAdd course operation cancelled.")
                return

            if not course_name:
                print("\nCourse name cannot be empty. Please try again.")
                continue

            if not course_name.isalpha():
                print("\nCourse name should only contain alphabetic characters. Please enter a valid course name.")
                continue

            try:
                cursor.execute('INSERT INTO courses (name) VALUES (?)', (course_name,))
                conn.commit()
                print(f"\nThe course '{course_name}' has been added successfully.")
            except sqlite3.IntegrityError:
                print(f"\nThe course '{course_name}' already exists. Please enter a different course name.")

            while True:
                print("\nA) Yes\nB) No")
                add_another = input("\nDo you want to add another course?: ").strip().upper()
                if add_another == 'A':
                    break
                elif add_another == 'B':
                    return
                else:
                    print("\nInvalid choice. Please enter 'A' or 'B'.")


    def remove_course():
        while True:
            while True:
                course_name = input("\nEnter the name of the course to remove (type 'exit' to cancel): ").strip()
                if course_name.lower() == 'exit':
                    print("\nRemove course operation cancelled.")
                    return

                if not course_name:
                    print("\nCourse name cannot be empty. Please try again.")
                    continue

                cursor.execute('DELETE FROM courses WHERE name = ?', (course_name,))
                if cursor.rowcount > 0:
                    conn.commit()
                    print(f"\nThe course '{course_name}' has been removed successfully.")
                    break
                else:
                    print(f"\nThe course '{course_name}' does not exist. Please enter a valid course name.")

            while True:
                print("\nA) Yes\nB) No")
                remove_another = input("\nDo you want to remove another course?: ").strip().upper()
                if remove_another == 'A':
                    break
                elif remove_another == 'B':
                    return
                else:
                    print("Invalid choice. Please enter 'A' or 'B'.")



    def authenticate_control_user():
        correct_username = 'sara'
        correct_password = '0'

        while True:
            entered_username = input("Enter username: ")
            entered_password = input("Enter password: ")

            if entered_username == correct_username and entered_password == correct_password:
                return True
            else:
                print("\nInvalid username or password. Access denied. Please try again.")

    def authenticate_student_user(student_id, password):
        cursor.execute('SELECT * FROM students WHERE id = ? AND password = ?', (student_id, password))
        student = cursor.fetchone()

        if student:
            return True
        else:
            return False

    def register_courses(student_id):
        while True:
            cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
            student = cursor.fetchone()

            if not student:
                print("\nStudent ID not found.")
                return

            print("\nAvailable Courses:")
            cursor.execute('SELECT * FROM courses')
            courses = cursor.fetchall()
            for course in courses:
                print(f"{course[0]}. {course[1]}")

            selected_course_id = input("\nEnter the ID of the course to register (type 'exit' to cancel): ").strip()

            if selected_course_id.lower() == 'exit':
                print("\nCourse registration canceled.")
                return

            try:
                selected_course_id = int(selected_course_id)
                if selected_course_id not in [course[0] for course in courses]:
                    print("\nInvalid course ID. Please select a valid course ID.")
                    continue
            except ValueError:
                print("\nInvalid input. Please enter a valid course ID.")
                continue

            cursor.execute('SELECT courses FROM students WHERE id = ?', (student_id,))
            registered_courses = cursor.fetchone()[0]

            if registered_courses:
                registered_courses = set(registered_courses.split(','))  # Split courses into a set
            else:
                registered_courses = set()

            if str(selected_course_id) in registered_courses:
                print("\nYou are already registered for this course.")
                continue

            cursor.execute('SELECT name FROM courses WHERE id = ?', (selected_course_id,))
            course_name = cursor.fetchone()[0]

            if registered_courses:
                registered_courses.add(str(selected_course_id))
                new_registered_courses = ','.join(registered_courses)
            else:
                new_registered_courses = str(selected_course_id)

            cursor.execute('UPDATE students SET courses = ? WHERE id = ?', (new_registered_courses, student_id))
            conn.commit()
            print(f"\nYou have successfully registered for the course: {course_name}.")
            return

    def edit_available_courses(student_id):
        while True:
            cursor.execute('SELECT * FROM courses')
            available_courses = cursor.fetchall()

            print("\nAvailable Courses:")
            for i, course in enumerate(available_courses, 1):
                print(f"{i}. {course[1]}")

            print("\nA) Add Course\nB) Remove Course\nC) Done")
            choice = input("\nEnter your choice: ").strip().upper()

            if choice == 'A':
                add_course_to_student(student_id, available_courses)
            elif choice == 'B':
                remove_course_from_student(student_id, available_courses)
            elif choice == 'C':
                print("\nCourse selection completed.")
                return
            else:
                print("\nInvalid choice. Please enter 'A', 'B', or 'C'.")


    def add_course_to_student(student_id, available_courses):
        try:
            course_index = int(input("\nEnter the number corresponding to the course you want to add: ")) - 1
            if 0 <= course_index < len(available_courses):
                course_id = available_courses[course_index][0]
                cursor.execute('SELECT courses FROM students WHERE id = ?', (student_id,))
                current_courses = cursor.fetchone()[0]
                if current_courses:
                    current_courses = current_courses.split(',')
                else:
                    current_courses = []

                if str(course_id) in current_courses:
                    print("\nYou are already registered for this course.")
                else:
                    current_courses.append(str(course_id))
                    updated_courses = ','.join(current_courses)
                    cursor.execute('UPDATE students SET courses = ? WHERE id = ?', (updated_courses, student_id))
                    conn.commit()
                    print("\nCourse added successfully.")
            else:
                print("\nInvalid course selection.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")

    def remove_course_from_student(student_id, available_courses):
        try:
            course_index = int(input("\nEnter the number corresponding to the course you want to remove: ")) - 1
            if 0 <= course_index < len(available_courses):
                course_id = available_courses[course_index][0]
                cursor.execute('SELECT courses FROM students WHERE id = ?', (student_id,))
                current_courses = cursor.fetchone()[0]
                if current_courses:
                    current_courses = current_courses.split(',')
                    if str(course_id) in current_courses:
                        current_courses.remove(str(course_id))
                        updated_courses = ','.join(current_courses)
                        cursor.execute('UPDATE students SET courses = ? WHERE id = ?', (updated_courses, student_id))
                        conn.commit()
                        print("\nCourse removed successfully.")
                    else:
                        print("\nYou are not registered for this course.")
                else:
                    print("\nYou are not registered for any courses.")
            else:
                print("\nInvalid course selection.")
        except ValueError:
            print("\nInvalid input. Please enter a number.")

    def choose_group(student_id):
        while True:
            print("\nChoose your group:")
            print("A) Group A")
            print("B) Group B")
            choice = input("\nEnter your choice: ").strip().upper()

            if choice == 'A' or choice == 'B':
                cursor.execute('UPDATE students SET group_type = ? WHERE id = ?', (choice, student_id))
                conn.commit()
                print(f"\nYou have been assigned to Group {choice}.")
                return
            else:
                print("\nInvalid choice. Please enter 'A' or 'B'.")

    def see_news():
        cursor.execute('SELECT * FROM news')
        news_list = cursor.fetchall()

        if not news_list:
            print("\nNo news articles available.")
            return

        print("\nList of News Articles:")
        for news in news_list:
            print(f"News number: {news[0]} | Content: {news[1]}")


def main_menu1():
    while True:
        print("\nA) Control\nB) Student\nC) Exit")
        choice = input("\nPlease select a choice from the list above: ").capitalize()

        if choice == 'A':
            if authenticate_control_user():
                main_menu2()
        elif choice == 'B':
            student_id = input("Enter your student ID: ")
            password = input("Enter your password: ")
            if authenticate_student_user(student_id, password):
                main_menu3(student_id)
            else:
                print("\nInvalid student ID or password. Access denied. Please try again.")
        elif choice == 'C':
            print("\nExiting...")
            sys.exit()
        else:
            print("\n**Invalid choice. Please enter a valid choice**")


def main_menu2():
    while True:
        print("""\nA) Add Student\nB) Remove Student\nC) Modify Student Information\nD) Get Student Information\nE) List of all Students
F) Add News for Students\nG) Remove News\nH) List of all News\nI) Add new course\nJ) Remove course\nK) Back to Previous Menu""")
        choice = input("\nPlease select a choice from the list above: ").capitalize()

        if choice == 'A':
            add_student()
        elif choice == 'B':
            remove_student()
        elif choice == 'C':
            update_student()
        elif choice == 'D':
            get_all_info()
        elif choice == 'E':
            all_students = get_all_students()
            print("\nList of Students:")
            for student in all_students:
                print(f"ID: {student[0]} | Name: {student[1]} | Grade: {student[2]} | GPA: {student[3]} | Courses: {student[4]} | Password: {student[5]} | Group Type: {student[6]}")
        elif choice == 'F':
            add_news()
        elif choice == 'G':
            remove_news()
        elif choice == 'H':
            all_news = get_all_news()
            print("\nList of News:")
            for news in all_news:
                print(f"News number: {news[0]} | Content: {news[1]}")
        elif choice == 'I':
            add_course()
        elif choice == 'J':
            remove_course()
        elif choice == 'K':
            break
        else:
            print("\n**Invalid choice. Please enter a valid choice**")

def main_menu3(student_id):
    while True:
        print("\nA) Register Courses\nB) Edit Courses\nC) Choose Group\nD) See News\nE) Back to Previous Menu")
        choice = input("\nPlease select a choice from the list above: ").capitalize()

        if choice == 'A':
            register_courses(student_id)
        elif choice == 'B':
            edit_available_courses(student_id)
        elif choice == 'C':
            choose_group(student_id)
        elif choice == 'D':
            see_news()
        elif choice == 'E':
            return
        else:
            print("\n**Invalid choice. Please enter a valid choice**")
main_menu1()
