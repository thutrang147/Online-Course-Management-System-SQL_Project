from utils.db_connector import create_connection
from mysql.connector import Error

def enroll_learner(learner_id, course_id):
    """Enroll a learner in a course using the stored procedure."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            cursor.callproc('EnrollLearner', (learner_id, course_id))
            connection.commit()
            return True
    except Error as e:
        print(f"Error enrolling learner: {e}")
        return False
    finally:
        connection.close()

def get_enrollments_by_learner(learner_id):
    """Retrieve all enrollments for a learner."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT E.*, C.CourseName 
                FROM Enrollments E 
                JOIN Courses C ON E.CourseID = C.CourseID 
                WHERE E.LearnerID = %s
            """
            cursor.execute(query, (learner_id,))
            return cursor.fetchall()
    except Error as e:
        print(f"Error retrieving enrollments: {e}")
        return []
    finally:
        connection.close()

def get_enrollments_by_course(course_id):
    """Retrieve all enrollments for a course."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT E.*, L.LearnerName 
                FROM Enrollments E 
                JOIN Learners L ON E.LearnerID = L.LearnerID 
                WHERE E.CourseID = %s
            """
            cursor.execute(query, (course_id,))
            return cursor.fetchall()
    except Error as e:
        print(f"Error retrieving enrollments: {e}")
        return []
    finally:
        connection.close()

def update_enrollment_status(enrollment_id, status):
    """Update the completion status of an enrollment."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "UPDATE Enrollments SET CompletionStatus = %s WHERE EnrollmentID = %s"
            cursor.execute(query, (status, enrollment_id))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating enrollment status: {e}")
        return False
    finally:
        connection.close()

def mark_lecture_viewed(enrollment_id, lecture_id):
    """Mark a lecture as viewed by a learner."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            # Get LearnerID and CourseID from Enrollment
            query = "SELECT LearnerID, CourseID FROM Enrollments WHERE EnrollmentID = %s"
            cursor.execute(query, (enrollment_id,))
            result = cursor.fetchone()
            if not result:
                return False
            learner_id, course_id = result

            # Verify Lecture belongs to the Course
            query = "SELECT LectureID FROM Lectures WHERE LectureID = %s AND CourseID = %s"
            cursor.execute(query, (lecture_id, course_id))
            if not cursor.fetchone():
                return False

            # Insert into LectureViews
            query = "INSERT INTO LectureViews (LearnerID, LectureID, ViewDate) VALUES (%s, %s, NOW())"
            cursor.execute(query, (learner_id, lecture_id))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error marking lecture viewed: {e}")
        return False
    finally:
        connection.close()

def get_learner_progress(enrollment_id):
    """Retrieve progress for an enrollment."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT 
                    E.LearnerID, 
                    E.CourseID, 
                    E.CompletionStatus, 
                    E.ProgressPercentage, 
                    COUNT(DISTINCT LV.LectureID) AS ViewedLectures, 
                    COUNT(DISTINCT L.LectureID) AS TotalLectures
                FROM Enrollments E
                LEFT JOIN LectureViews LV ON E.LearnerID = LV.LearnerID
                LEFT JOIN Lectures L ON E.CourseID = L.CourseID
                WHERE E.EnrollmentID = %s
                GROUP BY E.LearnerID, E.CourseID, E.CompletionStatus, E.ProgressPercentage
            """
            cursor.execute(query, (enrollment_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving progress: {e}")
        return None
    finally:
        connection.close()