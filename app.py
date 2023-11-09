from flask import Flask, redirect, url_for, request, render_template, jsonify
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_Db')


conn = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

#mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('homePage.html')


''' In production DELTE function
@app.route('/CourseList/<int:id>')
def delete():
    cursor = conn.cursor()

    delete_class_query = """
    DELETE FROM courseInfo WHERE %
    """
 '''

@app.route('/delete_course')
def deleteCourse():
    return render_template('deleteCourse.html')

@app.route('/update_course')
def updateCourse():
    return render_template('updateCourse.html')


@app.route('/bruh')
def bruh():
    cursor = conn.cursor()

    # Define a SQL query to create a new table
    
    create_table_query = """
        INSERT INTO courses2 (classCode, className, seatTaken, totalSeatsTaken, profssorName, modality, classSchedule)
        VALUES
        ('CS101', 'Progrmaming I',  20, 50, 'M. Charters', 'Online', 'Monday 9:30 AM - 12:30 PM')
    """

    cursor.execute(create_table_query)

    # Commit the changes to the database
    conn.commit()

    # Close the cursor
    cursor.close()
    return 'helo there'



@app.route('/search_course', methods = ['GET'])
def searchCourse():
    if request.method == 'GET':
        cursor = conn.cursor()
        class_code = request.args.get('classCode')

        check_exist = """
            SELECT * FROM courses2 WHERE classCode = %s
        """
        cursor.execute(check_exist, (class_code,))
        result = cursor.fetchall()

        
        if result:
            return redirect(url_for('findCourse', class_code=class_code))
        """
        else:
            return "Class not found"
        """
        
    return render_template('findClass.html')


@app.route('/admin_login')
def admingLoginPage():
    return render_template('adminLogin.html')


@app.route('/find_course/<string:class_code>', methods = ['GET'])
def findCourse(class_code):
    if request.method == 'GET':
        
        cursor = conn.cursor()

        grab_from_table = """
            SELECT * FROM courses2 WHERE classCode = %s
        """

        cursor.execute(grab_from_table, (class_code,))
        result = cursor.fetchall()
        cursor.close()
        
        if result:
            course_list = []
            
            for row in result:
                course_data = {                    
                    "classCode": row[1],
                    "ClassName": row[2],
                    "SeatsTaken": row[3],
                    "TotalSeats": row[4],
                    "professorName": row[5],
                    "modality": row[6],
                    "classSchedule": row[7]
                }
                course_list.append(course_data)
            
            return render_template('classInfo.html', course_list=course_list, class_code=class_code)
        
    return jsonify({"error": "Invalid request"})



@app.route('/add_courses', methods=['POST', 'GET'])
def add_courses():
    if request.method == 'POST':
        class_Name = request.form['className']
        class_code = request.form['classCode']
        seat_taken = int(request.form['seatTaken'])
        total_seats = int(request.form['totalSeatsTaken'])
        professor_name = request.form['profssorName']
        modality = request.form['modality']
        class_schedule = request.form['classSchedule']

        cursor = conn.cursor()

        add_to_table = """
            INSERT INTO courses2 (className, classCode, seatTaken, totalSeatsTaken, profssorName, modality, classSchedule)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        # Execute the query to create the 'courses' table
        cursor.execute(add_to_table, (class_Name, class_code, seat_taken, total_seats, professor_name, modality, class_schedule))

        # Commit the changes to the database
        conn.commit()

        # Close the cursor
        cursor.close()
        return 'class added successfully'
        
    return render_template('addClass.html')

if __name__ == "__main__":
    app.run(debug=True)