from flask import Flask, redirect, url_for, request, render_template
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


@app.route('/bruh')
def bruh():
    cursor = conn.cursor()

    # Define a SQL query to create a new table
    
    create_table_query = """
        INSERT INTO courseInfo (className, classCode, seatTaken, totalSeatsTaken, isFull)
        VALUES
        ('Computer Science 101', 'CS101', 30, 50, 0)
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
            SELECT * FROM courseInfo WHERE classCode = %s
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



#Route to get the courses based on a course code
@app.route('/find_course/<string:class_code>', methods = ['GET'])
def findCourse(class_code):
    if request.method == 'GET':

        cursor = conn.cursor()

        grab_from_table = """
            SELECT * FROM courseInfo WHERE classCode = %s
        """

        cursor.execute(grab_from_table, (class_code,))
        #return all data from query 
        result = cursor.fetchall()
        cursor.close()

        if(result):
            
            class_info = ""

            for row in result:
                class_info += f' Class Name: {row[1]}, Seats Taken: {row[3]}, Total Seats: {row[4]}, Is Full: {row[5]}'
            #return render_template('classInfo.html', class_info = class_info)
            return class_info + "\n"

    return 'Invalid request'



@app.route('/add_courses', methods=['POST', 'GET'])
def add_courses():
    if request.method == 'POST':
        class_Name = request.form['className']
        class_code = request.form['classCode']
        seat_taken = int(request.form['seatTaken'])
        total_seats = int(request.form['totalSeatsTaken'])

        cursor = conn.cursor()

        add_to_table = """
            INSERT INTO courseInfo (className, classCode, seatTaken, totalSeatsTaken, isFull)
            VALUES (%s, %s, %s, %s, %s)
        """

        # Execute the query to create the 'courses' table
        cursor.execute(add_to_table, (class_Name, class_code, seat_taken, total_seats, 0))

        # Commit the changes to the database
        conn.commit()

        # Close the cursor
        cursor.close()
        return 'class added successfully'
        
    return render_template('addClass.html')

if __name__ == "__main__":
    app.run(debug=True)