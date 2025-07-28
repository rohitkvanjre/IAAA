from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
import sqlite3
import subprocess
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management and flash messages

# Paths
ATTENDANCE_DIR = r"D:/Sai Ram/5th Sem/Mini Project/IAAA/Attendance"  # Base attendance folder
DATABASE_PATH = r"D:/Sai Ram/Projects/Final Project IAAA/IAAA/attendance_system.db"  # Database file

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Home route
@app.route("/")
def home():
    return redirect(url_for("login"))

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE user_id = ? AND password = ?", (user_id, password)).fetchone()
        conn.close()

        if user:
            session["user_id"] = user_id
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password. Please try again.", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")

# Dashboard route
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/manage_students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        usn = request.form['usn']
        name = request.form['name']

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO students (reg_number, usn, name) VALUES (?, ?, ?)", (reg_number, usn, name))
                conn.commit()
            flash("Student added successfully!", "success")
        except sqlite3.IntegrityError:
            flash("Duplicate Registration Number or USN. Student not added.", "danger")

    with get_db_connection() as conn:
        students = conn.execute("SELECT * FROM students").fetchall()

    return render_template('manage_students.html', students=students)

@app.route('/delete_student/<reg_number>', methods=['POST'])
def delete_student(reg_number):
    with get_db_connection() as conn:
        conn.execute("DELETE FROM students WHERE reg_number = ?", (reg_number,))
        conn.commit()
    flash("Student deleted successfully.", "info")
    return redirect(url_for('manage_students'))

@app.route("/view_attendance", methods=["GET", "POST"])
def view_attendance():
    if request.method == "POST":
        selected_date = request.form.get("date")  # Safely get the 'date' field
        selected_file = request.form.get("file")  # Safely get the 'file' field

        # If both date and file are selected
        if selected_date and selected_file:
            file_path = os.path.join(ATTENDANCE_DIR, selected_date, selected_file)

            if os.path.exists(file_path):
                # Read the Excel file and convert it to HTML for display
                df = pd.read_excel(file_path)
                table_html = df.to_html(index=False)
                return render_template(
                    "view_attendance.html",
                    dates=os.listdir(ATTENDANCE_DIR),
                    selected_date=selected_date,
                    files=os.listdir(os.path.join(ATTENDANCE_DIR, selected_date)),
                    selected_file=selected_file,
                    table_html=table_html,
                    file_path=file_path,
                )
            else:
                flash("The selected file does not exist.", "danger")
                return redirect(url_for("view_attendance"))

        # If only date is selected, load available files
        elif selected_date:
            files = os.listdir(os.path.join(ATTENDANCE_DIR, selected_date))
            return render_template(
                "view_attendance.html",
                dates=os.listdir(ATTENDANCE_DIR),
                selected_date=selected_date,
                files=files,
            )

    # Initial GET request: load available dates
    dates = os.listdir(ATTENDANCE_DIR)
    return render_template("view_attendance.html", dates=dates)


# Route for downloading attendance file
@app.route("/download", methods=["POST"])
def download():
    file_path = request.form["file_path"]
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        flash("The requested file does not exist.", "danger")
        return redirect(url_for("view_attendance"))

# Route for Take Attendance
@app.route("/take_attendance")
def take_attendance():
    script_path = r"D:/Sai Ram/5th Sem/Mini Project/IAAA/attendance_manager.py"
    try:
        subprocess.run(["python", script_path], check=True)
        flash("Attendance process started successfully!", "success")
    except Exception as e:
        flash(f"Error while starting attendance: {e}", "danger")
    return redirect(url_for("dashboard"))

# Route for Capture
@app.route("/capture")
def capture():
    script_path = r"D:/Sai Ram/5th Sem/Mini Project/IAAA/capture.py"
    try:
        subprocess.run(["python", script_path], check=True)
        flash("Capture process started successfully!", "success")
    except Exception as e:
        flash(f"Error while starting capture: {e}", "danger")
    return redirect(url_for("dashboard"))

# Logout route
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)