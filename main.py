from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["school_db"]
students_col = db["students"]


def add_student():
    name = input("Enter student name: ").strip()

    # Check for duplicate
    if students_col.find_one({"name": name}):
        print("❌ Student already exists.")
        return

    try:
        age = int(input("Enter student age: "))
        if age <= 0:
            print("❌ Age must be a positive number.")
            return
    except ValueError:
        print("❌ Age must be a number.")
        return

    students_col.insert_one({"name": name, "age": age})
    print("✅ Student added successfully.")


def view_students():
    students = list(students_col.find())

    if not students:
        print("📭 No students found.")
        return

    print("\n📋 Student List")
    print("-" * 30)
    for s in students:
        print(f"Name: {s['name']} | Age: {s['age']}")


def search_student():
    name = input("Enter student name to search: ").strip()
    student = students_col.find_one({"name": name})

    if student:
        print(f"✅ Found: Name: {student['name']} | Age: {student['age']}")
    else:
        print("❌ Student not found.")


def update_student():
    name = input("Enter student name to update: ").strip()

    try:
        new_age = int(input("Enter new age: "))
        if new_age <= 0:
            print("❌ Age must be positive.")
            return
    except ValueError:
        print("❌ Age must be a number.")
        return

    result = students_col.update_one(
        {"name": name},
        {"$set": {"age": new_age}}
    )

    if result.matched_count:
        print("✅ Student updated successfully.")
    else:
        print("❌ Student not found.")


def delete_student():
    name = input("Enter student name to delete: ").strip()
    result = students_col.delete_one({"name": name})

    if result.deleted_count:
        print("🗑️ Student deleted successfully.")
    else:
        print("❌ Student not found.")


def menu():
    while True:
        print("\n🎓 Student Management System")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")


menu()

