from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Pydantic model for validation


class Student(BaseModel):
    id: int
    name: str
    age: int


# In-memory list of students
students = [
    {"id": 1, "name": "Sudan", "age": 20},
    {"id": 2, "name": "Biraj", "age": 19},
    {"id": 3, "name": "Sajan", "age": 21}
]

# Create a new student

@app.post("/student")
def add_student(student: Student):
    # Add student to the list
    students.append({
        "id": student.id,
        "name": student.name,
        "age": student.age
    })
    return {"message": "Student added successfully", "student": student}




# View a student by ID
@app.get("/student/{student_id}")
def view_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student
    return {"message": "Student not found"}



# UPDATE
@app.patch("/student/update")
def update_student(student_id: int , name: str= None, age: int =None):
    for student in students:
        if student["id"] == student_id:
            if name:
                student["name"] = name
            if age:
                student["age"] = age
            print("Student updated")
            return {"message": " student not found" ,"student": student}
    
# DELETE


@app.delete("/student/{student_id}")
def delete_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            students.remove(student)
            return {"message": " Student deleted"}
    return {"message": " student not found"}
    
