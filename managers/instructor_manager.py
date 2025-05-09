from utils.db_connector import create_connection
from mysql.connector import Error

def add_instructor(name, expertise, email):
    """Add a new instructor to the Instructors table."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO Instructors (InstructorName, Expertise, Email) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, expertise, email))
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error adding instructor: {e}")
        return None
    finally:
        connection.close()

def get_instructor_by_id(instructor_id):
    """Retrieve an instructor by their ID."""
    connection = create_connection()
    if not connection:
        return None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Instructors WHERE InstructorID = %s"
            cursor.execute(query, (instructor_id,))
            return cursor.fetchone()
    except Error as e:
        print(f"Error retrieving instructor: {e}")
        return None
    finally:
        connection.close()

def update_instructor_info(instructor_id, name=None, expertise=None, email=None):
    """Update instructor information."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            updates = []
            params = []
            if name:
                updates.append("InstructorName = %s")
                params.append(name)
            if expertise:
                updates.append("Expertise = %s")
                params.append(expertise)
            if email:
                updates.append("Email = %s")
                params.append(email)
            if not updates:
                return False
            params.append(instructor_id)
            query = f"UPDATE Instructors SET {', '.join(updates)} WHERE InstructorID = %s"
            cursor.execute(query, params)
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating instructor: {e}")
        return False
    finally:
        connection.close()

def list_all_instructors():
    """Retrieve all instructors."""
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM Instructors"
            cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        print(f"Error listing instructors: {e}")
        return []
    finally:
        connection.close()

def delete_instructor(instructor_id):
    """Delete an instructor from the Instructors table."""
    connection = create_connection()
    if not connection:
        return False
    try:
        with connection.cursor() as cursor:
            query = "DELETE FROM Instructors WHERE InstructorID = %s"
            cursor.execute(query, (instructor_id,))
            connection.commit()
            return cursor.rowcount > 0
    except Error as e:
        print(f"Error deleting instructor: {e}")
        return False
    finally:
        connection.close()

def get_instructor_workload(instructor_id: int):
    """
    Retrieves the teaching workload (number of courses) for a specific instructor
    by querying the InstructorTeachingLoad view and filtering.
    Args:
        instructor_id: The ID of the instructor.
    Returns:
        A dictionary with 'InstructorName' and 'NumberOfCourses' if found, 
        or None if the instructor or their workload is not found or an error occurs.
        Example: {'InstructorName': 'Prof. Dumbledore', 'NumberOfCourses': 5}
    """
    connection = create_connection()
    if not connection:
        return None

    # First, get the instructor's name using their ID, as the view uses names for display
    # and we need to ensure we're filtering the view correctly.
    instructor_name = None
    try:
        with connection.cursor(dictionary=True) as cursor:
            query_get_name = "SELECT InstructorName FROM Instructors WHERE InstructorID = %s"
            cursor.execute(query_get_name, (instructor_id,))
            instructor_data = cursor.fetchone()
            if instructor_data:
                instructor_name = instructor_data['InstructorName']
            else:
                print(f"No instructor found with ID: {instructor_id}")
                return None # Instructor not found
    except Error as e:
        print(f"Error fetching instructor name: {e}")
        # Don't close connection here if we intend to use it again immediately
    # No finally here, as we want to reuse the connection if name fetch was successful

    if not instructor_name:
        if connection and connection.is_connected():
            connection.close()
        return None # Instructor name could not be fetched

    # Now query the view using the fetched instructor_name
    try:
        with connection.cursor(dictionary=True) as cursor:
            # The view already has InstructorName, so we filter by it.
            # It's important that InstructorName is unique or that the view's grouping
            # correctly represents the instructor tied to the original InstructorID.
            # Since the view groups by InstructorID and InstructorName, this should be safe.
            query_view = """
                SELECT InstructorName, NumberOfCourses 
                FROM InstructorTeachingLoad 
                WHERE InstructorName = %s
            """
            # Note: If the InstructorTeachingLoad view also selected i.InstructorID,
            # filtering by i.InstructorID would be more robust:
            # query_view = "SELECT InstructorName, NumberOfCourses FROM InstructorTeachingLoad WHERE InstructorID = %s"
            # And you wouldn't need the separate name fetch.
            # For now, we'll use the name as per the current view structure.

            cursor.execute(query_view, (instructor_name,))
            workload_data = cursor.fetchone()
            
            if workload_data:
                return workload_data # Returns {'InstructorName': 'Name', 'NumberOfCourses': X}
            else:
                # This case means the instructor exists (name was found) but has 0 courses
                # and the LEFT JOIN in the view included them with COUNT = 0 (if they have an entry in Instructors)
                # Or, if an instructor was deleted after view creation and name changed, it might not be found.
                # The view should handle instructors with 0 courses if the LEFT JOIN is correct.
                # Let's return 0 courses for an existing instructor not in the view (e.g., 0 courses).
                return {'InstructorName': instructor_name, 'NumberOfCourses': 0}

    except Error as e:
        print(f"Error retrieving instructor workload from view: {e}")
        return None
    finally:
        if connection and connection.is_connected():
            connection.close()

def get_all_instructors_workload(): # Cai nay menu chua co  
    """
    Retrieves the teaching workload for all instructors using the InstructorTeachingLoad view.
    Returns:
        A list of dictionaries, each with 'InstructorName' and 'NumberOfCourses',
        or an empty list if no data or an error.
    """
    connection = create_connection()
    if not connection:
        return []
    try:
        with connection.cursor(dictionary=True) as cursor:
            query = "SELECT InstructorName, NumberOfCourses FROM InstructorTeachingLoad ORDER BY NumberOfCourses DESC, InstructorName ASC"
            cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        print(f"Error retrieving all instructors workload: {e}")
        return []
    finally:
        if connection and connection.is_connected():
            connection.close()
