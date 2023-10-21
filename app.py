from flask import Flask, redirect, url_for, request, render_template
import pymysql

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Lion1234!"
app.config['MYSQL_DB'] = "classlist"
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

conn = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)

#mysql = MySQL(app)

@app.route('/bruh')
def index():
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
        return 'calss added successfully'
    
    return render_template('addClass.html')

if __name__ == "__main__":
    app.run(debug=True)