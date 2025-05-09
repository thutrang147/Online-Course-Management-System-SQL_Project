from utils.db_connector import create_connection
from mysql.connector import Error

def add_lecture(course_id, title, content):
    """Add a new lecture to the Lectures table."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Lectures (CourseID, Title, Content) VALUES (%s, %s, %s)"
            cursor.execute(query, (course_id, title, content))
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error adding lecture: {e}")
        return None
    finally:
        connection.close()

def get_lecture_by_id(lecture_id):
    """Retrieve a lecture by its ID."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Lectures WHERE LectureID = %s"
            cursor.execute(query, (lecture_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving lecture: {e}")
        return None
    finally:
        connection.close()

def get_lectures_by_course(course_id):
    """Retrieve all lectures for a course, ordered by LectureID."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Lectures WHERE CourseID = %s ORDER BY LectureID"
            cursor.execute(query, (course_id,))
            return cursor.fetchall()
    except Error as e:
        print(f"Error retrieving lectures: {e}")
        return []
    finally:
        connection.close()

def update_lecture_content(lecture_id, title=None, content=None):
    """Update lecture information."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            updates = []
            params = []
            if title:
                updates.append("Title = %s")
                params.append(title)
            if content:
                updates.append("Content = %s")
                params.append(content)
            if not updates:
                return False
            params.append(lecture_id)
            query = f"UPDATE Lectures SET {', '.join(updates)} WHERE LectureID = %s"
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating lecture: {e}")
        return False
    finally:
        connection.close()

def delete_lecture(lecture_id):
    """Delete a lecture from the Lectures table."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM Lectures WHERE LectureID = %s"
            cursor.execute(query, (lecture_id,))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting lecture: {e}")
        return False
    finally:
        connection.close()

def get_lectures_with_view_status(learner_id: int, course_id: int):
    """
    Retrieves all lectures for a given course and indicates the view status
    for a specific learner.
    Returns:
        list: A list of dictionaries, where each dictionary represents a lecture
              and includes 'LectureID', 'Title', 'ViewStatus' ('Viewed' or 'Not Viewed'),
              and 'ViewDate' (datetime object if viewed, None otherwise).
              Returns an empty list if no lectures are found or an error occurs.
    """
    connection = create_connection()
    if not connection:
        return []

    lectures_status_data = []
    try:
        with connection.cursor(dictionary=True) as cursor:
            # Select all lectures for the course.
            # LEFT JOIN with LectureViews specific to the learner and lecture.
            # If a match is found in LectureViews, the lecture is 'Viewed'.
            # Otherwise (due to LEFT JOIN), LectureViews columns will be NULL, indicating 'Not Viewed'.
            query = """
                SELECT 
                    L.LectureID,
                    L.Title,
                    L.Content, -- Included L.Content in case the UI wants to display it later without another query
                    CASE 
                        WHEN LV.LearnerID IS NOT NULL THEN 'Viewed'
                        ELSE 'Not Viewed'
                    END AS ViewStatus,
                    LV.ViewDate
                FROM Lectures L
                LEFT JOIN LectureViews LV 
                    ON L.LectureID = LV.LectureID AND LV.LearnerID = %s  -- Join condition for the specific learner
                WHERE L.CourseID = %s
                ORDER BY L.LectureID ASC; -- Or any other preferred order, e.g., L.Title
            """
            cursor.execute(query, (learner_id, course_id))
            lectures_status_data = cursor.fetchall()
            
    except Error as e:
        print(f"Error retrieving lectures with view status for learner {learner_id}, course {course_id}: {e}")
        # lectures_status_data remains []
    finally:
        if connection and connection.is_connected():
            connection.close()
    return lectures_status_data