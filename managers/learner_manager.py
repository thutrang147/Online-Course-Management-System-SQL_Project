from utils.db_connector import create_connection
from mysql.connector import Error

def add_learner(name, email, phone, password):
    """Add a new learner with user account."""
    from managers import user_manager
    
    connection = create_connection()
    if not connection:
        return None
    
    try:
        connection.start_transaction()
        
        # 1. Create user account first
        user_id = user_manager.create_user(email, password, 'learner')
        if not user_id:
            connection.rollback()
            return None
        
        # 2. Create learner profile
        with connection.cursor() as cursor:
            query = "INSERT INTO Learners (LearnerName, PhoneNumber, UserID) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, phone, user_id))
            learner_id = cursor.lastrowid
            
        connection.commit()
        return learner_id
        
    except Error as e:
        connection.rollback()
        print(f"Error adding learner: {e}")
        return None
    finally:
        connection.close()

def get_learner_by_id(learner_id):
    """Retrieve a learner by their ID."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT 
                    l.LearnerID,
                    l.LearnerName,
                    l.PhoneNumber,
                    u.Email
                FROM Learners l
                JOIN Users u ON l.UserID = u.UserID
                WHERE l.LearnerID = %s
            """
            cursor.execute(query, (learner_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving learner: {e}")
        return None
    finally:
        connection.close()

def get_learner_by_email(email):
    """Retrieve a learner by their email."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Learners WHERE Email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving learner: {e}")
        return None
    finally:
        connection.close()

def get_learner_by_user_id(user_id):
    """Retrieve a learner by their User ID."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT 
                    l.LearnerID,
                    l.LearnerName,
                    l.PhoneNumber,
                    u.Email
                FROM Learners l
                JOIN Users u ON l.UserID = u.UserID
                WHERE u.UserID = %s
            """
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving learner by user ID: {e}")
        return None
    finally:
        connection.close()

def update_learner_info(learner_id, name=None, email=None, phone=None):
    """Update learner information."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            updates = []
            params = []
            if name:
                updates.append("LearnerName = %s")
                params.append(name)
            if phone:
                updates.append("PhoneNumber = %s")
                params.append(phone)
            # Update Learners table if needed
            if updates:
                params.append(learner_id)
                query = f"UPDATE Learners SET {', '.join(updates)} WHERE LearnerID = %s"
                cursor.execute(query, params)
            # Update email in Users table if needed
            if email:
                # Get UserID from LearnerID
                cursor.execute("SELECT UserID FROM Learners WHERE LearnerID = %s", (learner_id,))
                user_row = cursor.fetchone()
                if user_row:
                    user_id = user_row[0] if isinstance(user_row, tuple) else user_row['UserID']
                    cursor.execute("UPDATE Users SET Email = %s WHERE UserID = %s", (email, user_id))
            connection.commit()
            return True
    except Error as e:
        print(f"Error updating learner: {e}")
        return False
    finally:
        connection.close()

def list_all_learners():
    """Retrieve all learners."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT 
                    l.LearnerID, 
                    l.LearnerName, 
                    u.Email, 
                    l.PhoneNumber
                FROM Learners l
                JOIN Users u ON l.UserID = u.UserID
            """
            cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        print(f"Error listing learners: {e}")
        return []
    finally:
        connection.close()

def delete_learner(learner_id):
    """Delete a learner from the Learners table."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM Learners WHERE LearnerID = %s"
            cursor.execute(query, (learner_id,))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting learner: {e}")
        return False
    finally:
        connection.close()

def check_password(learner_id, password):
    """Check if the provided password matches the stored password for the learner."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "SELECT Password FROM Learners WHERE LearnerID = %s"
            cursor.execute(query, (learner_id,))
            result = cursor.fetchone()
            if result and result['Password'] == password:
                return True
            return False
    except Error as e:
        print(f"Error checking password: {e}")
        return False
    finally:
        connection.close()

def update_password(learner_id, new_password):
    """Update the password for the learner."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "UPDATE Learners SET Password = %s WHERE LearnerID = %s"
            cursor.execute(query, (new_password, learner_id))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        connection.close()

def get_learner_courses(learner_id):
    """Retrieve all courses for a specific learner."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT Courses.CourseID, Courses.CourseName
                FROM Enrollments
                JOIN Courses ON Enrollments.CourseID = Courses.CourseID
                WHERE Enrollments.LearnerID = %s
            """
            cursor.execute(query, (learner_id,))
            return cursor.fetchall()
    except Error as e:
        print(f"Error retrieving learner courses: {e}")
        return []
    finally:
        connection.close()

def enroll_in_course(learner_id, course_id):
    """Enroll a learner in a specific course."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Enrollments (LearnerID, CourseID) VALUES (%s, %s)"
            cursor.execute(query, (learner_id, course_id))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error enrolling in course: {e}")
        return False
    finally:
        connection.close()

def unenroll_from_course(learner_id, course_id):
    """Unenroll a learner from a specific course."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM Enrollments WHERE LearnerID = %s AND CourseID = %s"
            cursor.execute(query, (learner_id, course_id))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error unenrolling from course: {e}")
        return False
    finally:
        connection.close()

def get_learner_progress(learner_id, course_id):
    """Retrieve the progress of a learner in a specific course."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT Progress
                FROM CourseProgress
                WHERE LearnerID = %s AND CourseID = %s
            """
            cursor.execute(query, (learner_id, course_id))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving learner progress: {e}")
        return None
    finally:
        connection.close()

def update_learner_progress(learner_id, course_id, progress):
    """Update the progress of a learner in a specific course."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = """
                UPDATE CourseProgress
                SET Progress = %s
                WHERE LearnerID = %s AND CourseID = %s
            """
            cursor.execute(query, (progress, learner_id, course_id))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating learner progress: {e}")
        return False
    finally:
        connection.close()

def get_user_id_by_learner_id(learner_id):
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT UserID FROM Learners WHERE LearnerID = %s", (learner_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['UserID'] if result else None