from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Helper function to establish a connection to the database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to create a new student record
@app.route('/students', methods=['POST'])
def create_student():
    student_id = request.form.get("student_id")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    dob = request.form.get("dob")
    amount_due = float(request.form.get("amount_due"))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO student (student_id, first_name, last_name, dob, amount_due)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, first_name, last_name, dob, amount_due))
        conn.commit()
        conn.close()
        return jsonify({"message": "Student record created successfully."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to read a specific student record by student_id
@app.route('/students', methods=['GET'])
def get_student():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        student_id = request.args.get("read_id")
        cursor.execute('SELECT * FROM student WHERE student_id = ?', (student_id,))
        student = cursor.fetchone()
        conn.close()

        if student:
            return jsonify(dict(student)), 200
        else:
            return jsonify({"message": "Student not found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/students/showall', methods=['GET'])
def showall():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student')
        students = cursor.fetchall()
        conn.close()

        if students:
            # Convert the list of tuples to a list of dictionaries for JSON serialization
            students_list = [dict(student) for student in students]
            return jsonify(students_list), 200
        else:
            return jsonify({"message": "No students found."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to update an existing student record by student_id
@app.route('/students/update', methods=['POST'])
def update_student():
    try:
        student_id = request.form.get("student_id")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        dob = request.form.get("dob")
        amount_due = float(request.form.get("amount_due"))
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE students
            SET first_name = ?, last_name = ?, dob = ?, amount_due = ?
            WHERE student_id = ?
        ''', (first_name, last_name, dob, amount_due, student_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Student record updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to delete a student record by student_id
@app.route('/students/delete', methods=['POST'])
def delete_student():
    try:
        student_id = int(request.form.get("student_id"))
        print(student_id)
        conn = get_db_connection()
        cursor = conn.cursor()

        # Execute the DELETE operation
        cursor.execute('DELETE FROM student WHERE student_id = ?', (student_id,))

        # Check if any rows were affected
        if cursor.rowcount > 0:
            conn.commit()
            conn.close()
            return jsonify({"message": "Student record deleted successfully."}), 200
        else:
            conn.rollback()  # Rollback the transaction since no rows were deleted
            conn.close()
            return jsonify({"message": "Student record not found."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route to show all student records
@app.route('/students', methods=['GET'])
def get_all_students():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM student')
        students = cursor.fetchall()
        conn.close()

        student_list = [dict(student) for student in students]
        return jsonify(student_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Run the Flask app
if __name__ == '__main__':
    # Create the student table if it doesn't exist
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student (
            student_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            amount_due REAL
        )
    ''')
    conn.close()

    app.run(debug=True)