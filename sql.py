import sqlite3

### Connction to sqlite
connection=sqlite3.connect('student.db')
cursor=connection.cursor()
### Creating table
cursor.execute('''CREATE TABLE IF NOT EXISTS students
                  (id INTEGER PRIMARY KEY,
                   name TEXT NOT NULL,
                   CLASS VARCHAR(25),
                   SECTION VARCHAR(25),MARKS INTEGER);''')
cursor.execute('''CREATE TABLE IF NOT EXISTS teachers
                    (id INTEGER PRIMARY KEY,
                     name TEXT NOT NULL,
                     subject VARCHAR(25));''')
#Inserting data into teachers table
teachers_data = [
    (1, 'Mr. Smith', 'Mathematics'),
    (2, 'Ms. Johnson', 'Science'),
    (3, 'Mrs. Lee', 'English')
]
cursor.executemany('INSERT OR REPLACE INTO teachers VALUES (?,?,?)', teachers_data)

 
### Inserting data
students_data = [
    (1, 'Alice', '10th', 'A', 85),
    (2, 'Bob', '10th', 'B', 90),
    (3, 'Charlie', '9th', 'A', 78),
    (4, 'David', '9th', 'C', 88),
    (5, 'Eva', '10th', 'A', 92)
]   
cursor.executemany('INSERT OR REPLACE INTO students VALUES (?,?,?,?,?)', students_data) 

# ✅ Commit the changes before fetching
connection.commit()

# Displaying data
print("The inserted data are:")
cursor.execute('SELECT * FROM teachers')
for row in cursor.fetchall():
    print(row)

# Close connection
connection.close()