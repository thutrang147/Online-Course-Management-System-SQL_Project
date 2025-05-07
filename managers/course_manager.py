from utils.db_connector import create_connection
from mysql.connector import Error

def add_course(name, description, instructor_id):
    """Add a new course to the Courses table."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Courses (CourseName, CourseDescription, InstructorID) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, description, instructor_id))
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error adding course: {e}")
        return None
    finally:
        connection.close()

def get_course_by_id(course_id):
    """Retrieve a course by its ID."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Courses WHERE CourseID = %s"
            cursor.execute(query, (course_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving course: {e}")
        return None
    finally:
        connection.close()

def update_course_info(course_id, name=None, description=None, instructor_id=None):
    """Update course information."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            updates = []
            params = []
            if name:
                updates.append("CourseName = %s")
                params.append(name)
            if description:
                updates.append("CourseDescription = %s")
                params.append(description)
            if instructor_id:
                updates.append("InstructorID = %s")
                params.append(instructor_id)
            if not updates:
                return False
            params.append(course_id)
            query = f"UPDATE Courses SET {', '.join(updates)} WHERE CourseID = %s"
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating course: {e}")
        return False
    finally:
        connection.close()

def list_all_courses():
    """Retrieve all courses with instructor names."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT C.*, I.InstructorName 
                FROM Courses C 
                LEFT JOIN Instructors I ON C.InstructorID = I.InstructorID
            """
            cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        print(f"Error listing courses: {e}")
        return []
    finally:
        connection.close()

def get_courses_by_instructor(instructor_id):
    """Retrieve all courses by an instructor."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Courses WHERE InstructorID = %s"
            cursor.execute(query, (instructor_id,))
            return cursor.fetchall()
    except Error as e:
        print(f"Error retrieving courses: {e}")
        return []
    finally:
        connection.close()

def list_courses_with_details():
    """Retrieve all courses with lecture count and enrollment count."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT 
                    C.CourseID, 
                    C.CourseName, 
                    C.CourseDescription, 
                    I.InstructorName, 
                    COUNT(DISTINCT L.LectureID) AS LectureCount, 
                    COUNT(DISTINCT E.EnrollmentID) AS EnrollmentCount
                FROM Courses C
                LEFT JOIN Instructors I ON C.InstructorID = I.InstructorID
                LEFT JOIN Lectures L ON C.CourseID = L.CourseID
                LEFT JOIN Enrollments E ON C.CourseID = E.CourseID
                GROUP BY C.CourseID, C.CourseName, C.CourseDescription, I.InstructorName
            """
            cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        print(f"Error listing courses with details: {e}")
        return []
    finally:
        connection.close()

def delete_course(course_id):
    """Delete a course from the Courses table."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM Courses WHERE CourseID = %s"
            cursor.execute(query, (course_id,))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting course: {e}")
        return False
    finally:
        connection.close()