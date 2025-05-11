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

def mark_lecture_viewed(learner_id, lecture_id): # Changed signature
# def mark_lecture_viewed(enrollment_id, lecture_id):
    """Mark a lecture as viewed by a learner."""
    connection = create_connection()
    if not connection:
        return False
    try:
        # if replace do it from here 
        with connection.cursor() as cursor:
            query_insert_view = "INSERT INTO LectureViews (LearnerID, LectureID, ViewDate) VALUES (%s, %s, NOW())"
            cursor.execute(query_insert_view, (learner_id, lecture_id))
            connection.commit()
            return cursor.rowcount > 0 # Will be 1 on successful insert
    except Error as e:
        # Check for specific errors, e.g., duplicate entry if PK (LearnerID, LectureID) on LectureViews is violated
        if e.errno == 1062: # MySQL error code for duplicate entry
            print(f"Info: Learner {learner_id} has already viewed lecture {lecture_id}.")
            return False # Or True if "already viewed" is not an error for the UI
        elif 'ViewDate must be on or after EnrollmentDate' in str(e): # From your trigger
            print(f"Error: {e}") # Display the trigger's message
            return False
        print(f"Error marking lecture viewed: {e}")
        return False
    finally:
        if connection and connection.is_connected():
            connection.close()

    #         # Get LearnerID and CourseID from Enrollment
    #         query = "SELECT LearnerID, CourseID FROM Enrollments WHERE EnrollmentID = %s"
    #         cursor.execute(query, (enrollment_id,))
    #         result = cursor.fetchone()
    #         if not result:
    #             return False
    #         learner_id, course_id = result

    #         # Verify Lecture belongs to the Course
    #         query = "SELECT LectureID FROM Lectures WHERE LectureID = %s AND CourseID = %s"
    #         cursor.execute(query, (lecture_id, course_id))
    #         if not cursor.fetchone():
    #             return False

    #         # Insert into LectureViews
    #         query = "INSERT INTO LectureViews (LearnerID, LectureID, ViewDate) VALUES (%s, %s, NOW())"
    #         cursor.execute(query, (learner_id, lecture_id))
    #         connection.commit()
    #         return cursor.rowcount > 0
    # except Error as e:
    #     print(f"Error marking lecture viewed: {e}")
    #     return False
    # finally:
    #     connection.close()

def get_learner_progress(enrollment_id):
    """Retrieve progress for an enrollment."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor: # add EnrollmentDate, EnrollmentID
            query = """
                SELECT 
                    E.EnrollmentID,
                    E.LearnerID, 
                    E.CourseID, 
                    E.EnrollmentDate, 
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

def get_course_progress_summary(course_id: int):
    """
    Retrieves a progress summary for all learners enrolled in a specific course
    by calling the GenerateCompletionSummary stored procedure.
    Returns:
        A list of dictionaries, where each dictionary represents a learner's
        enrollment and progress in that course. Returns an empty list on error.
        Example item: {'LearnerName': 'Alice', 'CourseName': 'Python Intro', 
                       'EnrollmentDate': datetime.date(2024, 1, 5), 
                       'CompletionStatus': 'In Progress', 'ProgressPercentage': 50}
    """
    connection = create_connection()
    if not connection:
        return []

    summary_data = []
    try:
        with connection.cursor(dictionary=True) as cursor:
            # Call the stored procedure
            cursor.callproc('GenerateCompletionSummary', (course_id,))
            
            # Stored procedures that return result sets need to be handled by iterating over stored_results()
            # MySQL Connector/Python returns one result set per SELECT statement in the SP.
            # Your SP has one SELECT.
            for result_set in cursor.stored_results():
                summary_data = result_set.fetchall() # fetchall() from the result_set object
                break # Assuming only one result set from this SP
            
    except Error as e:
        print(f"Error generating course completion summary for course ID {course_id}: {e}")
        # summary_data remains []
    finally:
        if connection and connection.is_connected():
            connection.close()
    return summary_data

def get_all_enrollments_detailed():
    """
    Retrieves all enrollment records, including learner names and course names.
    Returns:
        list: A list of dictionaries, where each dictionary represents an enrollment
              and includes 'EnrollmentID', 'LearnerName', 'CourseName', 'EnrollmentDate',
              'CompletionStatus', and 'ProgressPercentage'.
              Returns an empty list if no enrollments are found or an error occurs.
        Example item:
            {
                'EnrollmentID': 1, 
                'LearnerName': 'Alice Wonderland', 
                'CourseName': 'Introduction to Python', 
                'EnrollmentDate': datetime.date(2024, 1, 5), 
                'CompletionStatus': 'In Progress', 
                'ProgressPercentage': 50
            }
    """
    connection = create_connection()
    if not connection:
        return []

    enrollments_data = []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = """
                SELECT 
                    E.EnrollmentID,
                    L.LearnerName,
                    C.CourseName,
                    E.EnrollmentDate,
                    E.CompletionStatus,
                    E.ProgressPercentage,
                    E.LearnerID,  -- Included for potential further use if needed
                    E.CourseID    -- Included for potential further use if needed
                FROM Enrollments E
                JOIN Learners L ON E.LearnerID = L.LearnerID
                JOIN Courses C ON E.CourseID = C.CourseID
                ORDER BY E.EnrollmentDate DESC, L.LearnerName ASC, C.CourseName ASC;
            """
            cursor.execute(query)
            enrollments_data = cursor.fetchall()
            
    except Error as e:
        print(f"Error retrieving all detailed enrollments: {e}")
        # enrollments_data remains []
    finally:
        if connection and connection.is_connected():
            connection.close()
    return enrollments_data

def get_enrollment_logs():
    """
    Retrieves all enrollment log records, including associated learner and course names.
    Returns:
        Returns an empty list if no logs are found or an error occurs.
        Example item:
            {
                'LogID': 1,
                'EnrollmentID': 101, # Could be None if original enrollment was deleted
                'LearnerName': 'Alice Wonderland', # Could be None if original learner was deleted
                'CourseName': 'Introduction to Python', # Could be None if original course was deleted
                'LogTime': datetime.datetime(2024, 1, 5, 10, 0, 0), # Timestamp object
                'ActionType': 'Enrollment Created'
            }
    """
    connection = create_connection()
    if not connection:
        return []

    logs_data = []
    try:
        with connection.cursor(dictionary=True) as cursor:
            # Join EnrollmentLogs with Learners and Courses to get names.
            # Use LEFT JOINs because LearnerID or CourseID in EnrollmentLogs
            # might be NULL if the original entities were deleted (due to ON DELETE SET NULL).
            query = """
                SELECT 
                    EL.LogID,
                    EL.EnrollmentID,
                    L.LearnerName,    -- Fetched via LEFT JOIN
                    C.CourseName,     -- Fetched via LEFT JOIN
                    EL.LogTime,
                    EL.ActionType
                FROM EnrollmentLogs EL
                LEFT JOIN Learners L ON EL.LearnerID = L.LearnerID
                LEFT JOIN Courses C ON EL.CourseID = C.CourseID
                ORDER BY EL.LogTime DESC, EL.LogID DESC; -- Show newest logs first
            """
            cursor.execute(query)
            logs_data = cursor.fetchall()
            
    except Error as e:
        print(f"Error retrieving enrollment logs: {e}")
        # logs_data remains []
    finally:
        if connection and connection.is_connected():
            connection.close()
    return logs_data