from flask import Flask, request, jsonify, session, redirect, url_for
from datetime import datetime
import mysql.connector
import bcrypt, json, os
from decimal import Decimal

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD', 'harshrajput147')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB', 'school_db')

try:
    db = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )
    cursor = db.cursor()
    print("Connected to MySQL successfully")
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    raise SystemExit(1)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'message': 'Bad request'}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'message': 'Unauthorized access'}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Internal server error'}), 500

def convert_decimal(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

@app.route('/')
def index():
    return jsonify({'message': 'Welcome to School Management System Application!!'})

@app.route('/admin/home', methods=['GET'])
def home():
    return jsonify({'message': 'Welcome to Home Page!', 'links': {'admin_dashboard': '/admin/dashboard'}})


@app.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Bad Request: No data provided'}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    if username == 'admin' and password == 'admin':
        session['admin_logged_in'] = True
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401



@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    admin_dashboard_links = {
        'staff': '/admin/staff_data',
        'students': '/admin/students_data',
        'about_us': '/admin/about_us',
        'contact_us': '/admin/contact_us',
        'reviews': '/admin/reviews',
        'query': '/admin/query', 
        'enquiries': '/admin/enquiries',
        'attendance': '/attendances',
        'filter_by_section': '/attendances/section/<section_name>',
        'filter_by_date': '/attendances/date/<YYYY-MM-DD>'
    }

    return jsonify({'message': 'Welcome to Admin Dashboard!', 'links': admin_dashboard_links})
@app.route('/admin/staff_data', methods=['GET'])
def admin_staff_data():
    try:
        cursor.execute("SELECT * FROM staff")
        staff_data = cursor.fetchall()
        return jsonify({'staff_data': staff_data})
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error fetching staff data: {err}"}), 500

@app.route('/admin/students_data', methods=['GET'])
def admin_students_data():
    try:
        cursor.execute("SELECT * FROM students")
        students_data = cursor.fetchall()
        return jsonify({'students_data': students_data})
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error fetching students data: {err}"}), 500

@app.route('/admin/about_us', methods=['GET'])
def admin_about_us():
    about_us_info = "About Us: This webpage provides information about our services and team. Our school, XYZ School, is committed to providing quality education to students. Our dedicated team of educators and staff ensures a nurturing environment for learning and growth. The school management oversees the smooth functioning of academic and extracurricular activities, aiming to foster holistic development among students."
    return jsonify({'message': about_us_info})


@app.route('/attendances', methods=['GET'])
def get_attendances():
    try:
        cursor.execute("SELECT * FROM students_attendance")
        records = cursor.fetchall()
        attendance_records = []
        for record in records:
            attendance_record = {
                'id': record[0],
                'student_id': record[1],
                'date': record[2].strftime('%Y-%m-%d'),
                'section': record[3],
                'status': record[4]
            }
            attendance_records.append(attendance_record)
        return jsonify({'attendance_records': attendance_records})
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error fetching attendance records: {err}"}), 500


@app.route('/attendances/section/<string:section>', methods=['GET'])
def get_attendance_by_section(section):
    try:
        cursor.execute("SELECT * FROM students_attendance WHERE section=%s", (section,))
        records = cursor.fetchall()
        attendance_records = []
        for record in records:
            attendance_record = {
                'id': record[0],
                'student_id': record[1],
                'date': record[2].strftime('%Y-%m-%d'),
                'section': record[3],
                'status': record[4]
            }
            attendance_records.append(attendance_record)
        return jsonify({'attendance_records': attendance_records})
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error fetching attendance records: {err}"}), 500


@app.route('/attendances/date/<string:date>', methods=['GET'])
def get_attendance_by_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students_attendance WHERE date=%s", (date,))
        records = cursor.fetchall()
        cursor.close()

        attendance_records = []
        for record in records:
            attendance_record = {
                'id': record[0],
                'student_id': record[1],
                'date': record[2].strftime('%Y-%m-%d'),
                'section': record[3],
                'status': record[4]
            }
            attendance_records.append(attendance_record)
        return jsonify({'attendance_records': attendance_records})
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error fetching attendance records: {err}"}), 500



@app.route('/admin/contact_us', methods=['GET'])
def admin_contact_us():
    contact_info = {
        'email': 'example@example.com',
        'contact_number': '123-456-7890',
        'school_address': '123 School Street, City, Country',
        'office_address': '456 Office Avenue, City, Country',
        'facebook': 'facebook.com/XYZSchool',
        'twitter': 'twitter.com/XYZSchool',
        'instagram': 'instagram.com/XYZSchool',
        'youtube_channel': 'youtube.com/c/XYZSchool'
    }
    return jsonify({'message': 'Contact Us:', 'contact_info': contact_info})

@app.route('/admin/reviews', methods=['GET'])
def admin_reviews():
    try:
        cursor.execute("SELECT id, parent_id, institution_id, review_text, rating, created_at FROM reviewsratings")
        reviews = cursor.fetchall()
        reviews_data = []
        for review in reviews:
            review_info = {
                'id': review[0],
                'parent_id': review[1],
                'institution_id': review[2],
                'review_text': review[3],
                'rating': review[4],
                'created_at': review[5].strftime('%Y-%m-%d %H:%M:%S')
            }
            reviews_data.append(review_info)
        return jsonify({'reviews': reviews_data})
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error fetching reviews: {err}"}), 500


@app.route('/admin/query', methods=['GET'])
def admin_query():
    try:
        cursor.execute("SELECT id, student_id, query_text, answer_text FROM query")
        queries = cursor.fetchall()
        queries_data = []
        for query in queries:
            query_info = {
                'id': query[0],
                'student_id': query[1],
                'query_text': query[2],
                'answer_text': query[3]
            }
            queries_data.append(query_info)
        return jsonify({'queries': queries_data})
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error fetching queries: {err}"}), 500


@app.route('/admin/enquiries', methods=['GET'])
def admin_enquiries():
    try:
        cursor.execute("SELECT id, parent_name, email, phone, institution_id, institution_category, message FROM parentenquiries")
        enquiries = cursor.fetchall()
        enquiries_data = []
        for enquiry in enquiries:
            enquiry_info = {
                'id': enquiry[0],
                'parent_name': enquiry[1],
                'email': enquiry[2],
                'phone': enquiry[3],
                'institution_id': enquiry[4],
                'institution_category': enquiry[5],
                'message': enquiry[6]
            }
            enquiries_data.append(enquiry_info)
        return jsonify({'enquiries': enquiries_data})
    except mysql.connector.Error as err:
        return jsonify({'message': f"Error fetching enquiries: {err}"}), 500






@app.route('/students', methods=['GET'])
def students():
    return jsonify("Welcome to Students!!")

@app.route('/students/register', methods=['POST'])
def student_register():
    data = request.get_json()
    if not data or not all(key in data for key in ('firstname', 'lastname', 'email', 'students_rollnumber', 'password')):
        return jsonify({'message': 'Missing required fields!'}), 400

    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    students_rollnumber = data['students_rollnumber']
    password = data['password']

    cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        return jsonify({'message': 'Email already exists!'}), 400

    cursor.execute("SELECT * FROM students WHERE students_rollnumber=%s", (students_rollnumber,))
    rollnumber = cursor.fetchone()

    if rollnumber:
        return jsonify({'message': 'Student roll number already exists!'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO students (firstname, lastname, email, students_rollnumber, password) VALUES (%s, %s, %s, %s, %s)", (firstname, lastname, email, students_rollnumber, hashed_password))
    db.commit()

    return jsonify({'message': 'Student registered successfully!'})

@app.route('/students/login', methods=['POST'])
def student_login():
    data = request.get_json()
    if not data or not all(key in data for key in ('email', 'password')):
        return jsonify({'message': 'Missing email or password!'}), 400

    email = data['email']
    password = data['password']

    cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'message': 'Invalid email or password'}), 401

    if bcrypt.checkpw(password.encode('utf-8'), user[5].encode('utf-8')):
        session['user_id'] = user[0]
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/students/forgot_password', methods=['POST'])
def student_forgot_password():
    data = request.get_json()
    if not data or not all(key in data for key in ('email', 'newpassword', 'confirmpassword')):
        return jsonify({'message': 'Missing email, new password, or confirm password!'}), 400

    email = data['email']
    new_password = data['newpassword']
    confirm_password = data['confirmpassword']

    if new_password != confirm_password:
        return jsonify({'message': 'New password and confirm password do not match!'}), 400

    cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'message': 'Email is not registered!'}), 404

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE students SET password=%s WHERE email=%s", (hashed_password, email))
    db.commit()

    return jsonify({'message': 'Password reset successfully!'})

@app.route('/students/logout', methods=['POST'])
def student_logout():
    if 'user_id' in session:
        session.pop('user_id')
        return jsonify({'message': 'Logout successful!'})
    else:
        return jsonify({'message': 'No student is currently logged in!'}), 401

@app.route('/students/dashboard', methods=['GET'])
def student_dashboard():
    if 'user_id' not in session:  
        return jsonify({'message': 'Login required to access this page!'}), 401

    student_dashboard_links = {
        'home': '/students/home',
        'about_us': '/students/about_us',
        'contact_us': '/students/contact_us',
        'attendance_records': '/students/attendance_records',
        'reviews': '/students/reviews',
        'query': '/students/query'
    }

    return jsonify({'message': 'Welcome to Student Dashboard!', 'links': student_dashboard_links})

@app.route('/students/home', methods=['GET'])
def students_home():
    if 'user_id' in session:  
        return jsonify({'message': 'Welcome to Home Page for students!'})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401

@app.route('/students/about_us', methods=['GET'])
def students_about_us():
    if 'user_id' in session:  
        about_us_info = "About Us: This webpage provides information about our services and team. Our school, XYZ School, is committed to providing quality education to students. Our dedicated team of educators and staff ensures a nurturing environment for learning and growth. The school management oversees the smooth functioning of academic and extracurricular activities, aiming to foster holistic development among students."
        return jsonify({'message': about_us_info})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401

@app.route('/students/contact_us', methods=['GET'])
def students_contact_us():
    if 'user_id' in session:  
        contact_info = {
            'email': 'example@example.com',
            'contact_number': '123-456-7890',
            'school_address': '123 School Street, City, Country',
            'office_address': '456 Office Avenue, City, Country',
            'facebook': 'facebook.com/XYZSchool',
            'twitter': 'twitter.com/XYZSchool',
            'instagram': 'instagram.com/XYZSchool',
            'youtube_channel': 'youtube.com/c/XYZSchool'
        }
        return jsonify({'message': 'Contact Us:', 'contact_info': contact_info})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401

@app.route('/students/attendance_records', methods=['POST'])
def create_attendance_record():
    if 'user_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    data = request.get_json()
    student_id = data.get('student_id')
    date = data.get('date')
    section = data.get('section')
    status = data.get('status')

    cursor.execute("INSERT INTO students_attendance (student_id, date, section, status) VALUES (%s, %s, %s, %s)",
                   (student_id, date, section, status))
    db.commit()
    return jsonify({'message': 'Attendance record created successfully!'})

@app.route('/students/attendance_records/<int:id>', methods=['GET'])
def get_attendance_record_by_id(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    cursor.execute("SELECT * FROM students_attendance WHERE id=%s", (id,))
    record = cursor.fetchone()

    if record:
        attendance_record = {
            'id': record[0],
            'student_id': record[1],
            'date': record[2].strftime('%Y-%m-%d'),
            'section': record[3],
            'status': record[4]
        }
        return jsonify({'attendance_record': attendance_record})
    else:
        return jsonify({'message': 'Attendance record not found!'}), 404

@app.route('/students/attendance_records', methods=['GET'])
def get_all_stuattendance_records():
    if 'user_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    cursor.execute("SELECT * FROM students_attendance")
    records = cursor.fetchall()
    attendance_records = []
    for record in records:
        attendance_record = {
            'id': record[0],
            'student_id': record[1],
            'date': record[2].strftime('%Y-%m-%d'),
            'section': record[3],
            'status': record[4]
        }
        attendance_records.append(attendance_record)
    return jsonify({'attendance_records': attendance_records})

@app.route('/students/attendance_records/<int:id>', methods=['PUT'])
def update_stuattendance_record(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    data = request.get_json()
    student_id = data.get('student_id')
    date = data.get('date')
    section = data.get('section')
    status = data.get('status')

    cursor.execute("UPDATE students_attendance SET student_id=%s, date=%s, section=%s, status=%s WHERE id=%s",
                   (student_id, date, section, status, id))
    db.commit()
    return jsonify({'message': 'Attendance record updated successfully!'})

@app.route('/students/attendance_records/<int:id>', methods=['DELETE'])
def delete_attendance_record(id):
    if 'user_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    cursor.execute("DELETE FROM students_attendance WHERE id=%s", (id,))
    db.commit()
    return jsonify({'message': 'Attendance record deleted successfully!'})

@app.route('/students/reviews', methods=['GET'])
def students_reviews():
    if 'user_id' in session:  
        try:
            cursor.execute("SELECT id, parent_id, institution_id, review_text, rating, created_at FROM reviewsratings")
            reviews = cursor.fetchall()
            reviews_info = []
            for review in reviews:
                review_info = {
                    'id': review[0],
                    'parent_id': review[1],
                    'institution_id': review[2],
                    'review_text': review[3],
                    'rating': review[4],
                    'created_at': review[5].strftime('%Y-%m-%d %H:%M:%S')
                }
                reviews_info.append(review_info)
            return jsonify({'reviews': reviews_info})
        except mysql.connector.Error as err:
            return jsonify({'message': f"Error fetching reviews: {err}"}), 500
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401


@app.route('/students/query', methods=['POST'])
def create_query():
    if 'user_id' in session:
        data = request.get_json()
        student_id = data.get('student_id')
        query_text = data.get('query_text')

        cursor.execute("INSERT INTO Query (student_id, query_text) VALUES (%s, %s)", (student_id, query_text))
        db.commit()
        return jsonify({'message': 'Query submitted successfully!'})
    else:
        return jsonify({'message': 'Login required to submit a query!'}), 401

@app.route('/students/query', methods=['GET'])
def students_query():
    if 'user_id' in session:
        cursor.execute("SELECT * FROM Query WHERE student_id=%s", (session['user_id'],))
        queries = cursor.fetchall()
        student_queries = []
        for query in queries:
            query_info = {
                'id': query[0],
                'student_id': query[1],
                'query_text': query[2],
                'answer_text': query[3]
            }
            student_queries.append(query_info)
        return jsonify({'queries': student_queries})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401




@app.route('/staff', methods=['GET'])
def staff():
        return jsonify({'message': 'Welcome to Staff!'})


@app.route('/staff/register', methods=['POST'])
def staff_register():
    data = request.get_json()
    if not data or 'firstname' not in data or 'lastname' not in data or 'email' not in data or 'staff_idnumber' not in data or 'password' not in data:
        return jsonify({'message': 'Missing required fields!'}), 400

    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    staff_idnumber = data['staff_idnumber']
    password = data['password']

    cursor.execute("SELECT * FROM staff WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        return jsonify({'message': 'Email already exists!'}), 400

    cursor.execute("SELECT * FROM staff WHERE staff_idnumber=%s", (staff_idnumber,))
    staff_member = cursor.fetchone()

    if staff_member:
        return jsonify({'message': 'Staff ID number already exists!'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO staff (firstname, lastname, email, staff_idnumber, password) VALUES (%s, %s, %s, %s, %s)", (firstname, lastname, email, staff_idnumber, hashed_password))
    db.commit()

    return jsonify({'message': 'Staff member registered successfully!'})



@app.route('/staff/login', methods=['POST'])
def staff_login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Missing email or password!'}), 400

    email = data['email']
    password = data['password']

    cursor.execute("SELECT * FROM staff WHERE email=%s", (email,))
    staff_member = cursor.fetchone()

    if not staff_member:
        return jsonify({'message': 'Invalid email or password'}), 401

    if bcrypt.checkpw(password.encode('utf-8'), staff_member[5].encode('utf-8')):
        session['staff_id'] = staff_member[0]
        return jsonify({'message': 'Login successful!'})

    return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/staff/forgot_password', methods=['POST'])
def staff_forgot_password():
    data = request.get_json()
    if not data or 'email' not in data or 'newpassword' not in data or 'confirmpassword' not in data:
        return jsonify({'message': 'Missing email, new password, or confirm password!'}), 400

    email = data['email']
    new_password = data['newpassword']
    confirm_password = data['confirmpassword']

    if new_password != confirm_password:
        return jsonify({'message': 'New password and confirm password do not match!'}), 400

    cursor.execute("SELECT * FROM staff WHERE email=%s", (email,))
    staff_member = cursor.fetchone()

    if not staff_member:
        return jsonify({'message': 'Email is not registered!'}), 404

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE staff SET password=%s WHERE email=%s", (hashed_password, email))
    db.commit()

    return jsonify({'message': 'Password reset successfully!'})

@app.route('/staff/logout', methods=['POST'])
def staff_logout():
    session.pop('staff_id', None)
    return jsonify({'message': 'Logout successful!'})


@app.route('/staff/home', methods=['GET'])
def staff_home():
    if 'staff_id' in session:  
        return jsonify({'message': 'Welcome to Home Page for staff!'})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401 


@app.route('/staff/dashboard', methods=['GET'])
def staff_dashboard():
    if 'staff_id' not in session:  
        return jsonify({'message': 'Login required to access this page!'}), 401

    staff_dashboard_links = {
        'home': '/staff/home',
        'about_us': '/staff/about_us',
        'contact_us': '/staff/contact_us',
        'attendance_records': {
            'all': '/staff/attendance_records',
            'update_status': '/staff/attendance_records/update/<int:student_id>',
            'filter_by_student_id': '/staff/attendance_records/<int:student_id>',
            'filter_by_section': '/staff/attendance_records/section/<string:section>',
            'filter_by_date': '/staff/attendance_records/date/<string:date>'
        },
        'reviews': '/staff/reviews',
        'query': '/staff/query'
    }

    return jsonify({'message': 'Welcome to Staff Dashboard!', 'links': staff_dashboard_links})



@app.route('/staff/attendance_records', methods=['GET'])
def get_all_attendance_records():
    if 'staff_id' in session:
        cursor.execute("SELECT * FROM students_attendance")
        records = cursor.fetchall()
        attendance_records = []
        for record in records:
            attendance_record = {
                'id': record[0],
                'student_id': record[1],
                'date': record[2].strftime('%Y-%m-%d'),
                'section': record[3],
                'status': record[4]
            }
            attendance_records.append(attendance_record)
        return jsonify({'attendance_records': attendance_records})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401

@app.route('/staff/attendance_records/update/<int:student_id>', methods=['PUT'])
def update_attendance_record(student_id):
    if 'staff_id' in session:
        data = request.get_json()
        status = data.get('status')

        cursor.execute("UPDATE students_attendance SET status=%s WHERE student_id=%s", (status, student_id))
        db.commit()
        return jsonify({'message': 'Attendance record updated successfully!'})
    else:
        return jsonify({'message': 'Login required to update attendance records!'}), 401

@app.route('/staff/attendance_records/<int:student_id>', methods=['GET'])
def get_attendance_records_by_student_id(student_id):
    if 'staff_id' in session:
        cursor.execute("SELECT * FROM students_attendance WHERE student_id=%s", (student_id,))
        records = cursor.fetchall()
        attendance_records = []
        for record in records:
            attendance_record = {
                'id': record[0],
                'student_id': record[1],
                'date': record[2].strftime('%Y-%m-%d'),
                'section': record[3],
                'status': record[4]
            }
            attendance_records.append(attendance_record)
        return jsonify({'attendance_records': attendance_records})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401

@app.route('/staff/attendance_records/section/<string:section>', methods=['GET'])
def filter_attendance_records_by_section(section):
    if 'staff_id' in session:
        cursor.execute("SELECT * FROM students_attendance WHERE section=%s", (section,))
        records = cursor.fetchall()
        attendance_records = []
        for record in records:
            attendance_record = {
                'id': record[0],
                'student_id': record[1],
                'date': record[2].strftime('%Y-%m-%d'),
                'section': record[3],
                'status': record[4]
            }
            attendance_records.append(attendance_record)
        return jsonify({'attendance_records': attendance_records})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401

@app.route('/staff/attendance_records/date/<string:date>', methods=['GET'])
def filter_attendance_records_by_date(date):
    if 'staff_id' in session:
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({'message': 'Invalid date format!'}), 400

        cursor.execute("SELECT * FROM students_attendance WHERE date=%s", (date,))
        records = cursor.fetchall()
        attendance_records = []
        for record in records:
            attendance_record = {
                'id': record[0],
                'student_id': record[1],
                'date': record[2].strftime('%Y-%m-%d'),
                'section': record[3],
                'status': record[4]
            }
            attendance_records.append(attendance_record)
        return jsonify({'attendance_records': attendance_records})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401



@app.route('/staff/about_us', methods=['GET'])
def staff_about_us():
    if 'user_id' in session:  
        about_us_info = "About Us: This webpage provides information about our services and team. Our school, XYZ School, is committed to providing quality education to students. Our dedicated team of educators and staff ensures a nurturing environment for learning and growth. The school management oversees the smooth functioning of academic and extracurricular activities, aiming to foster holistic development among students."
        return jsonify({'message': about_us_info})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401


@app.route('/staff/contact_us', methods=['GET'])
def staff_contact_us():
    if 'user_id' in session:  
        contact_info = {
            'email': 'example@example.com',
            'contact_number': '123-456-7890',
            'school_address': '123 School Street, City, Country',
            'office_address': '456 Office Avenue, City, Country',
            'facebook': 'facebook.com/XYZSchool',
            'twitter': 'twitter.com/XYZSchool',
            'instagram': 'instagram.com/XYZSchool',
            'youtube_channel': 'youtube.com/c/XYZSchool'
        }
        return jsonify({'message': 'Contact Us:', 'contact_info': contact_info})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401



@app.route('/staff/reviews', methods=['GET'])
def staff_reviews():
    if 'staff_id' in session:
        try:
            cursor.execute("SELECT id, parent_id, institution_id, review_text, rating, created_at FROM reviewsratings")
            reviews = cursor.fetchall()
            reviews_info = []
            for review in reviews:
                review_info = {
                    'id': review[0],
                    'parent_id': review[1],
                    'institution_id': review[2],
                    'review_text': review[3],
                    'rating': review[4],
                    'created_at': review[5].strftime('%Y-%m-%d %H:%M:%S')
                }
                reviews_info.append(review_info)
            return jsonify({'reviews': reviews_info})
        except mysql.connector.Error as err:
            return jsonify({'message': f"Error fetching reviews: {err}"}), 500
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401

    
    

@app.route('/staff/query', methods=['GET'])
def staff_query():
    if 'staff_id' in session:
        cursor.execute("SELECT * FROM Query")
        queries = cursor.fetchall()
        all_queries = []
        for query in queries:
            query_info = {
                'id': query[0],
                'student_id': query[1],
                'query_text': query[2],
                'answer_text': query[3]
            }
            all_queries.append(query_info)
        return jsonify({'queries': all_queries})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401

@app.route('/staff/query/answer/<int:id>', methods=['PUT'])
def answer_query(id):
    if 'staff_id' in session:
        data = request.get_json()
        answer_text = data.get('answer_text')

        cursor.execute("UPDATE Query SET answer_text=%s WHERE id=%s", (answer_text, id))
        db.commit()
        return jsonify({'message': 'Query answered successfully!'})
    else:
        return jsonify({'message': 'Login required to answer queries!'}), 401



@app.route('/parents', methods=['GET'])
def parents():
    return jsonify({'message': 'Welcome to Parents!'})

@app.route('/parents/register', methods=['POST'])
def parent_register():
    data = request.get_json()
    if not data or not all(key in data for key in ('first_name', 'last_name', 'email', 'password')):
        return jsonify({'message': 'Missing required fields!'}), 400

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

    cursor.execute("SELECT * FROM Parents WHERE email=%s", (email,))
    user = cursor.fetchone()

    if user:
        return jsonify({'message': 'Email already exists!'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO Parents (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, hashed_password))
    db.commit()

    return jsonify({'message': 'Parent registered successfully!'})

@app.route('/parents/login', methods=['POST'])
def parent_login():
    data = request.get_json()
    if not data or not all(key in data for key in ('email', 'password')):
        return jsonify({'message': 'Missing email or password!'}), 400

    email = data['email']
    password = data['password']

    cursor.execute("SELECT parent_id, password FROM Parents WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'message': 'Invalid email or password'}), 401

    parent_id, hashed_password = user

    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
        session['parent_id'] = parent_id
        return jsonify({'message': 'Login successful!'})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/parents/forgot_password', methods=['POST'])
def parent_forgot_password():
    data = request.get_json()
    if not data or not all(key in data for key in ('email', 'new_password', 'confirm_password')):
        return jsonify({'message': 'Missing email, new password, or confirm password!'}), 400

    email = data['email']
    new_password = data['new_password']
    confirm_password = data['confirm_password']

    if new_password != confirm_password:
        return jsonify({'message': 'New password and confirm password do not match!'}), 400

    cursor.execute("SELECT * FROM Parents WHERE email=%s", (email,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'message': 'Email is not registered!'}), 404

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("UPDATE Parents SET password=%s WHERE email=%s", (hashed_password, email))
    db.commit()

    return jsonify({'message': 'Password reset successfully!'})


@app.route('/parents/logout', methods=['POST'])
def parent_logout():
    if 'parent_id' in session:
        session.pop('parent_id')
        return jsonify({'message': 'Logout successful!'})
    else:
        return jsonify({'message': 'No parent is currently logged in!'}), 401


@app.route('/parents/dashboard', methods=['GET'])
def parent_dashboard():
    if 'parent_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    parent_dashboard_links = {
        'home': '/parents/home',
        'schools': '/parents/dashboard/schools',
        'colleges': '/parents/dashboard/colleges',
        'universities': '/parents/dashboard/universities',
        'awards_certifications': '/parents/dashboard/awards_certifications',
        'reviews_ratings': '/parents/dashboard/reviews_ratings',
        'contact_us': '/parents/dashboard/contact_us',
        'career': '/parents/dashboard/career',
        'support': '/parents/dashboard/support'
    }

    return jsonify({'message': 'Welcome to Parent Dashboard!', 'links': parent_dashboard_links})



@app.route('/parents/home', methods=['GET'])
def parents_home():
    if 'parent_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    category = request.args.get('category')
    sort_by = request.args.get('sort_by', 'rating')
    sort_order = request.args.get('sort_order', 'DESC')
    cursor = db.cursor(dictionary=True) 

    query = "SELECT * FROM Institutions WHERE category IN ('school', 'college', 'university')"
    params = []

    if category:
        query += " AND category = %s"
        params.append(category)

    query += f" ORDER BY {sort_by} {sort_order} LIMIT 5"
    
    cursor.execute(query, params)
    institutions = cursor.fetchall()

    schools = [inst for inst in institutions if inst['category'] == 'school']
    colleges = [inst for inst in institutions if inst['category'] == 'college']
    universities = [inst for inst in institutions if inst['category'] == 'university']

    response = {
        'message': 'Welcome to the Parent Home Page!',
        'top_schools': schools,
        'top_colleges': colleges,
        'top_universities': universities,
        'enquiry_form_link': '/parents/dashboard/support'
    }

    cursor.close()
    db.close()

    return app.response_class(
        response=json.dumps(response, default=convert_decimal),
        status=200,
        mimetype='application/json'
    )



def insert_parent_enquiry(parent_name, email, phone, institution_id, institution_category, message):
    cursor.execute("""
    INSERT INTO ParentEnquiries (parent_name, email, phone, institution_id, institution_category, message)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (parent_name, email, phone, institution_id, institution_category, message))
    db.commit()

@app.route('/parents/dashboard/support', methods=['GET', 'POST'])
def parent_support():
    if request.method == 'GET':
        return jsonify({'message': 'Welcome to Parent Support Page!'})

    if request.method == 'POST':
        data = request.get_json()

        parent_name = data.get('parent_name')
        email = data.get('email')
        phone = data.get('phone')
        institution_id = data.get('institution_id')
        institution_category = data.get('institution_category')
        message = data.get('message')

        if not all([parent_name, email, phone, institution_id, institution_category, message]):
            return jsonify({'message': 'All fields are required!'}), 400

        insert_parent_enquiry(parent_name, email, phone, institution_id, institution_category, message)

        return jsonify({'message': 'Enquiry submitted successfully!'})


@app.route('/parents/dashboard/schools', methods=['GET'])
def get_schools():
    if 'parent_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    try:
        
        if not db.is_connected():
            db.reconnect(attempts=1, delay=0)

        cursor.execute("SELECT * FROM Institutions WHERE category = 'school'")
        schools = cursor.fetchall()

        response = {
            'message': 'List of Schools',
            'schools': schools,
            'enquiry_form_link': '/parents/dashboard/support'
        }
    except mysql.connector.Error as err:
        return jsonify({'message': f'Error: {err}'}), 500

    return app.response_class(
        response=json.dumps(response, default=convert_decimal),
        status=200,
        mimetype='application/json'
    )

@app.route('/parents/dashboard/colleges', methods=['GET'])
def get_colleges():
    if 'parent_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    try:
        if not db.is_connected():
            db.reconnect(attempts=1, delay=0)

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Institutions WHERE category = 'college'")
        colleges = cursor.fetchall()
        cursor.close()

        response = {
            'message': 'List of Colleges',
            'colleges': colleges,
            'enquiry_form_link': '/parents/dashboard/support'
        }
    except mysql.connector.Error as err:
        return jsonify({'message': f'Error: {err}'}), 500

    return app.response_class(
        response=json.dumps(response, default=convert_decimal),
        status=200,
        mimetype='application/json'
    )

@app.route('/parents/dashboard/universities', methods=['GET'])
def get_universities():
    if 'parent_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    try:
        if not db.is_connected():
            db.reconnect(attempts=1, delay=0)

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Institutions WHERE category = 'university'")
        universities = cursor.fetchall()
        cursor.close()

        response = {
            'message': 'List of Universities',
            'universities': universities,
            'enquiry_form_link': '/parents/dashboard/support'
        }
    except mysql.connector.Error as err:
        return jsonify({'message': f'Error: {err}'}), 500

    return app.response_class(
        response=json.dumps(response, default=convert_decimal),
        status=200,
        mimetype='application/json'
    )

@app.route('/parents/dashboard/contact_us', methods=['GET'])
def parents_contact_us():
    if 'parent_id' in session:  
        contact_info = {
            'email': 'example@example.com',
            'contact_number': '123-456-7890',
            'school_address': '123 School Street, City, Country',
            'office_address': '456 Office Avenue, City, Country',
            'facebook': 'facebook.com/XYZSchool',
            'twitter': 'twitter.com/XYZSchool',
            'instagram': 'instagram.com/XYZSchool',
            'youtube_channel': 'youtube.com/c/XYZSchool'
        }
        return jsonify({'message': 'Contact Us:', 'contact_info': contact_info})
    else:
        return jsonify({'message': 'Login required to access this page!'}), 401


@app.route('/parents/dashboard/awards_certifications', methods=['GET'])
def get_awards_certifications():
    if 'parent_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    try:
        if not db.is_connected():
            db.reconnect(attempts=1, delay=0)

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM AwardsCertifications")
        awards_certifications = cursor.fetchall()
        cursor.close()

        for award in awards_certifications:
            for key, value in award.items():
                if isinstance(value, Decimal):
                    award[key] = float(value)

        response = {
            'message': 'List of Awards and Certifications',
            'awards_certifications': awards_certifications
        }
    except mysql.connector.Error as err:
        return jsonify({'message': f'Error: {err}'}), 500

    return jsonify(response)

@app.route('/parents/dashboard/reviews_ratings', methods=['GET'])
def get_reviews_ratings():
    if 'parent_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    try:
        if not db.is_connected():
            db.reconnect(attempts=1, delay=0)

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ReviewsRatings")
        reviews_ratings = cursor.fetchall()
        cursor.close()

        for review in reviews_ratings:
            for key, value in review.items():
                if isinstance(value, Decimal):
                    review[key] = float(value)

        response = {
            'message': 'List of Reviews and Ratings',
            'reviews_ratings': reviews_ratings,
            'enquiry_form_link': '/parents/dashboard/support'
        }
    except mysql.connector.Error as err:
        return jsonify({'message': f'Error: {err}'}), 500

    return jsonify(response)


@app.route('/parents/dashboard/reviews_ratings', methods=['POST'])
def add_review_rating():
    if 'parent_id' not in session:
        return jsonify({'message': 'Login required to access this page!'}), 401

    data = request.get_json()

    parent_id = session['parent_id']
    institution_id = data.get('institution_id')
    review_text = data.get('review_text')
    rating = data.get('rating')

    if not all([institution_id, review_text, rating]):
        return jsonify({'message': 'All fields are required!'}), 400

    try:
        if not db.is_connected():
            db.reconnect(attempts=1, delay=0)

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO ReviewsRatings (parent_id, institution_id, review_text, rating)
            VALUES (%s, %s, %s, %s)
        """, (parent_id, institution_id, review_text, rating))
        db.commit()
        cursor.close()
    except mysql.connector.Error as err:
        return jsonify({'message': f'Error: {err}'}), 500

    return jsonify({'message': 'Review and rating submitted successfully!'})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


