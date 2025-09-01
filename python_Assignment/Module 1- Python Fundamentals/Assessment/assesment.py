student={}

def main():
    while True:
        print("\n----Studet Management System----")
        print("\nPress 1 for Conseller")
        print("Press 2 for Faculty")
        print("Press 3 for student")
        print("Press 4 for Exit")

        choice = input("\nEnter a role id: ")
        if choice == "1":
            counseller_menu()
        elif choice == "2":
            feculty_menu()
        elif choice == "3":
            view_specific_student()
        elif choice == "4":
            print("Exiting system...")
            break
        else:
            print("Invalid role ID!")

def counseller_menu():

    while True:
        print("\nConsellor Menu:-")
        print("1.Add Studnet")
        print("2.Remove Student")
        print("3.View ALL Students")
        print("4.View Specific Student")
        print("5.Exit")
        choice=input("\nEnter a choice by counseller:")

        if choice=="1":
            add_student()
        elif choice=="2":
            remove_student()
        elif choice=="3":
            view_all_students()
        elif choice=="4":
            view_specific_student()
        elif choice=="5":
            break
        else:
            print("Invalid choice! Please try again.")

def add_student():
    sid = input("Enter a Serial Number:")
    Firstname = input("Enter a First Name:")
    Lastname = input("Enter a Last Name:")
    number = input("Enter a Contact Number:")
    Subject = input("Enter a Subject:")
    marks = input("ENter a Marks:")
    fess = input("Enter a Fees:")

    student[sid]={
        "Firstname":Firstname,
        "Lastname":Lastname,
        "Contact": number,
        "Subject": Subject,
        "Marks": marks,
        "Fees": fess
        }
    print("Student added succesfully")
    for sid, details in student.items():
        print(f"{sid}. {details['Firstname']} {details['Lastname']} - "
              f"Contact: {details['Contact']}, Subject: {details['Subject']}, "
              f"Marks: {details['Marks']}, Fees: {details['Fees']}")

def remove_student():
    sid = input("Enter the Serial Number of the student to remove: ")
    if sid in student:
        del student[sid]
        print("Student removed successfully!")
    else:
        print("Student not found!")

def view_all_students():
    if not student:
        print("No students found!")
        return
    print("\nList of Students:")
    for sid, details in student.items():
        print(f"{sid}. {details['Firstname']} {details['Lastname']} - "
              f"Contact: {details['Contact']}, Subject: {details['Subject']}, "
              f"Marks: {details['Marks']}, Fees: {details['Fees']}")
        
def view_specific_student():
    sid = input("Enter the Serial Number of the student: ")
    if sid in student:
        details = student[sid]
        print(f"\nStudent Details for {sid}:")
        print(f"Name: {details['Firstname']} {details['Lastname']}")
        print(f"Contact: {details['Contact']}")
        print(f"Subject: {details['Subject']}")
        print(f"Marks: {details['Marks']}")
        print(f"Fees: {details['Fees']}")
    else:
        print("Student not found!")

def add_marks():
    sid = input("Enter the Serial Number of the student: ")
    if sid in student:
        marks = input("Enter marks to assign: ")
        student[sid]["Marks"] = marks
        print("Marks updated successfully!")
    else:
        print("Student not found!")


def feculty_menu():
    print("\n===== Faculty Menu =====")
    print("1. Add marks to student")
    print("2. View all students")

    choice = input("Enter a choice by Faculty: ")

    if choice == "1":
         add_marks()
    elif choice == "2":
        view_all_students()
    else:
        print("Invalid choice! Please try again.")


main()