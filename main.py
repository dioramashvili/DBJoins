# Import required libraries
import random
import sqlite3

# https://www.geeksforgeeks.org/python-sqlite-join-clause/

# Connect to SQLite database
# New file created if it doesn't already exist
conn = sqlite3.connect('sqlite3.db')

# Create cursor object
cursor = conn.cursor()

# Create and populate tables
cursor.executescript(''' 
CREATE TABLE Advisor( 
AdvisorID INTEGER NOT NULL, 
AdvisorName TEXT NOT NULL, 
PRIMARY KEY(AdvisorID) 
); 

CREATE TABLE Student( 
StudentID NUMERIC NOT NULL, 
StudentName NUMERIC NOT NULL, 
AdvisorID INTEGER, 
FOREIGN KEY(AdvisorID) REFERENCES Advisor(AdvisorID), 
PRIMARY KEY(StudentID) 
); 

INSERT INTO Advisor(AdvisorID, AdvisorName) VALUES 
(1,"John Paul"), 
(2,"Anthony Roy"), 
(3,"Raj Shetty"), 
(4,"Sam Reeds"), 
(5,"Arthur Clintwood"); 

CREATE TABLE AdvisorStudent( 
AdvisorID INTEGER, 
StudentID NUMERIC, 
PRIMARY KEY(AdvisorID, StudentID), 
FOREIGN KEY(AdvisorID) REFERENCES Advisor(AdvisorID), 
FOREIGN KEY(StudentID) REFERENCES Student(StudentID) 
); 

INSERT INTO Student(StudentID, StudentName, AdvisorID) VALUES 
(501,"Geek1",1), 
(502,"Geek2",1), 
(503,"Geek3",3), 
(504,"Geek4",2), 
(505,"Geek5",4), 
(506,"Geek6",2), 
(507,"Geek7",2), 
(508,"Geek8",3), 
(509,"Geek9",NULL), 
(510,"Geek10",1); 

''')

# Commit changes to database
conn.commit()

# Add random data to the AdvisorStudent table
num_students = 10
num_advisors = 5
students_assigned_to_advisor = 2

advisor_ids = list(range(1, num_advisors + 1))
student_ids = list(range(501, 501 + num_students))

for _ in range(num_advisors):
    advisor_id = random.choice(advisor_ids)
    advisor_ids.remove(advisor_id)
    for _ in range(students_assigned_to_advisor):
        student_id = random.choice(student_ids)
        student_ids.remove(student_id)
        cursor.execute("INSERT INTO AdvisorStudent (AdvisorID, StudentID) VALUES (?, ?)", (advisor_id, student_id))
conn.commit()

# Print the advisors with their corresponding students
cursor.execute("""SELECT Advisor.AdvisorName, Student.StudentName FROM Advisor
                INNER JOIN AdvisorStudent ON Advisor.AdvisorID = AdvisorStudent.AdvisorID
                INNER JOIN Student ON Student.StudentID = AdvisorStudent.StudentID""")

results = cursor.fetchall()

print("Advisor: Student")
for result in results:
    print(f"{result[0]}: {result[1]}")


# Commit changes to database
conn.commit()

# Closing the connection
conn.close()
