import mysql.connector
from flask import Flask, redirect, render_template, request

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="microsoft@900",   # add your MySQL password
        database="my_db2"
    )

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students(name, email) VALUES (%s, %s)", (name, email))
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("add_student.html")

@app.route("/add_course", methods=["GET", "POST"])
def add_course():
    if request.method == "POST":
        course_name = request.form["course_name"]
        duration = request.form["duration"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses(course_name, duration) VALUES (%s, %s)", (course_name, duration))
        conn.commit()
        conn.close()
        return redirect("/")

    return render_template("add_course.html")

@app.route("/enroll", methods=["GET", "POST"])
def enroll():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    if request.method == "POST":
        student_id = request.form["student_id"]
        course_id = request.form["course_id"]
        cursor.execute("INSERT INTO enrollments(student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
        conn.commit()
        conn.close()
        return redirect("/view_enrollments")

    conn.close()
    return render_template("enroll.html", students=students, courses=courses)

@app.route("/view_enrollments")
def view_enrollments():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT enrollments.id, students.name, students.email, courses.course_name, courses.duration
        FROM enrollments
        JOIN students ON enrollments.student_id = students.id
        JOIN courses ON enrollments.course_id = courses.id
    """)
    data = cursor.fetchall()
    conn.close()
    return render_template("view_enrollments.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
