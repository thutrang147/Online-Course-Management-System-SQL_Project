# main.py
# Main application file for the Online Course Management CLI (Role-Based Menu)

import utils.ui_utils as ui
# Import backend manager modules
from managers import course_manager
from managers import enrollment_manager
from managers import instructor_manager
from managers import learner_manager
from managers import lecture_manager
0
# --- Administrator Panel Handlers ---

def admin_handle_learner_management():
    """Handles all actions related to Learner management by an Admin."""
    learner_menu_options = ["List All Learners", "Add New Learner", "View Learner Details",
                            "Update Learner Info", "Delete Learner", "Back to Admin Panel"]
    while True:
        ui.display_menu("Admin: Learner Management", learner_menu_options)
        choice = ui.get_input("Enter your choice", int, allowed_values=[str(i) for i in range(len(learner_menu_options))])

        try:
            if choice == 0: # List All
                learners = learner_manager.list_all_learners()
                ui.display_table(["LearnerID", "LearnerName", "Email", "PhoneNumber"], 
                                 learners, 
                                 "No learners found.")
            elif choice == 1: # Add New
                name = ui.get_input("Enter learner name", str)
                email = ui.get_input("Enter learner email", str)
                phone = ui.get_input("Enter learner phone (optional)", str, required=False)
                learner_id = learner_manager.add_learner(name, email, phone if phone else None)
                if learner_id is not None: # Check if ID is returned (not False/None on error)
                    ui.display_message(f"Learner '{name}' added successfully with ID: {learner_id}", "success")
                else:
                    ui.display_message("Failed to add learner (email might already exist or DB error).", "error")
            elif choice == 2: # View Details
                 learner_id = ui.get_input("Enter Learner ID to view", int)
                 learner = learner_manager.get_learner_by_id(learner_id)
                 if learner:
                     ui.display_table(["LearnerID", "LearnerName", "Email", "PhoneNumber"], 
                                      [{'LearnerID': learner_id, 'LearnerName': learner['LearnerName'], 'Email': learner['Email'], 'PhoneNumber': learner.get('PhoneNumber', 'N/A')}])
                 else: # get
                     ui.display_message(f"Learner with ID {learner_id} not found.", "error")
            elif choice == 3: # Update
                learner_id = ui.get_input("Enter Learner ID to update", int)
                learner = learner_manager.get_learner_by_id(learner_id)
                if not learner:
                     ui.display_message(f"Learner with ID {learner_id} not found.", "error")
                     continue
                name = ui.get_input(f"Enter new name (current: {learner['LearnerName']}, blank to keep)", str, required=False)
                email = ui.get_input(f"Enter new email (current: {learner['Email']}, blank to keep)", str, required=False)
                phone = ui.get_input(f"Enter new phone (current: {learner.get('PhoneNumber', 'N/A')}, blank to keep)", str, required=False)
                if learner_manager.update_learner_info(learner_id, name=name or None, email=email or None, phone=phone or None):
                    ui.display_message(f"Learner ID {learner_id} updated successfully.", "success")
                else:
                    ui.display_message("Failed to update learner.", "error")
            elif choice == 4: # Delete
                learner_id = ui.get_input("Enter Learner ID to delete", int)
                if learner_manager.get_learner_by_id(learner_id): # Check if exists before confirming
                    if ui.confirm_action(f"Delete Learner ID {learner_id}? This cascades to enrollments & lecture views."):
                        if learner_manager.delete_learner(learner_id):
                            ui.display_message(f"Learner ID {learner_id} deleted successfully.", "success")
                        else:
                            ui.display_message("Failed to delete learner.", "error")
                else:
                    ui.display_message(f"Learner with ID {learner_id} not found.", "error")
            elif choice == 5: # Back
                break
            if choice != 5 : ui.pause_screen()
        except Exception as e:
            ui.display_message(f"An unexpected error occurred in Learner Management: {e}", "error")
            ui.pause_screen()


def admin_handle_instructor_management():
    """Handles all actions related to Instructor management by an Admin."""
    instructor_menu_options = ["List All Instructors", "Add New Instructor", "View Instructor Details",
                               "Update Instructor Info", "Delete Instructor", "Back to Admin Panel"]
    while True:
        ui.display_menu("Admin: Instructor Management", instructor_menu_options)
        choice = ui.get_input("Enter your choice", int, allowed_values=[str(i) for i in range(len(instructor_menu_options))])
        try:
            if choice == 0: # List All
                instructors = instructor_manager.list_all_instructors()
                ui.display_table(["InstructorID", "InstructorName", "Expertise", "Email"], 
                                 instructors, 
                                 "No instructors found.")
            elif choice == 1: # Add New
                name = ui.get_input("Enter instructor name", str)
                expertise = ui.get_input("Enter instructor expertise (optional)", str, required=False)
                email = ui.get_input("Enter instructor email", str)
                instructor_id = instructor_manager.add_instructor(name, expertise if expertise else None, email)
                if instructor_id is not None:
                    ui.display_message(f"Instructor '{name}' added successfully with ID: {instructor_id}", "success")
                else:
                    ui.display_message("Failed to add instructor (email might already exist or DB error).", "error")
            elif choice == 2: # View Details
                instructor_id = ui.get_input("Enter Instructor ID to view", int)
                instructor = instructor_manager.get_instructor_by_id(instructor_id)
                if instructor:
                    ui.display_table(["InstructorID", "InstructorName", "Expertise", "Email"], 
                                     [instructor])
                else:
                    ui.display_message(f"Instructor with ID {instructor_id} not found.", "error")
            elif choice == 3: # Update
                instructor_id = ui.get_input("Enter Instructor ID to update", int)
                instructor = instructor_manager.get_instructor_by_id(instructor_id)
                if not instructor:
                     ui.display_message(f"Instructor with ID {instructor_id} not found.", "error")
                     continue
                name = ui.get_input(f"Enter new name (current: {instructor['InstructorName']}, blank to keep)", str, required=False)
                expertise = ui.get_input(f"Enter new expertise (current: {instructor.get('Expertise', 'N/A')}, blank to keep)", str, required=False)
                email_val = ui.get_input(f"Enter new email (current: {instructor['Email']}, blank to keep)", str, required=False) # Use different var name
                if instructor_manager.update_instructor_info(instructor_id, name=name or None, expertise=expertise or None, email=email_val or None): # Corrected
                    ui.display_message(f"Instructor ID {instructor_id} updated successfully.", "success")
                else:
                    ui.display_message("Failed to update instructor.", "error")
            elif choice == 4: # Delete
                instructor_id = ui.get_input("Enter Instructor ID to delete", int)
                if instructor_manager.get_instructor_by_id(instructor_id):
                    if ui.confirm_action(f"Delete Instructor ID {instructor_id}? Courses assigned will have InstructorID set to NULL."):
                        if instructor_manager.delete_instructor(instructor_id):
                            ui.display_message(f"Instructor ID {instructor_id} deleted successfully.", "success")
                        else:
                            ui.display_message("Failed to delete instructor.", "error")
                else:
                    ui.display_message(f"Instructor with ID {instructor_id} not found.", "error")
            elif choice == 5: # Back
                break
            if choice != 5: ui.pause_screen()
        except Exception as e:
            ui.display_message(f"An unexpected error occurred in Instructor Management: {e}", "error")
            ui.pause_screen()


def admin_handle_course_management():
    """Handles all actions related to Course management by an Admin."""
    course_menu_options = [
        "List All Courses (with Details)", "Add New Course", "View Course Details & Lectures",
        "Update Course Info", "Delete Course", "Manage Lectures for a Course", "Back to Admin Panel"
    ]
    while True:
        ui.display_menu("Admin: Course Management", course_menu_options)
        choice = ui.get_input("Enter your choice", int, allowed_values=[str(i) for i in range(len(course_menu_options))])
        try:
            if choice == 0: # List All Courses
                courses = course_manager.list_courses_with_details() 
                if courses: # Expects list of dicts: {'CourseID', 'CourseName', 'Description', 'InstructorName', 'LectureCount', 'EnrollmentCount'}
                    ui.display_table(["CourseID", "CourseName", "CourseDescription", "InstructorName", "LectureCount", "EnrollmentCount"], 
                                     courses, 
                                     "No courses found.")
                else:
                    ui.display_message("No courses found.", "info")
            elif choice == 1: # Add New Course
                name = ui.get_input("Enter course name", str)
                description = ui.get_input("Enter course description (optional)", str, required=False)
                instructors = instructor_manager.list_all_instructors()
                instructor_id_to_assign = None
                if instructors:
                    ui.display_message("Available Instructors:")
                    ui.display_table(["InstructorID", "InstructorName"], instructors)
                    instructor_id_str = ui.get_input("Enter Instructor ID to assign (optional, blank for none)", str, required=False,
                                                  allowed_values=[str(i['InstructorID']) for i in instructors] + [''])
                    if instructor_id_str: instructor_id_to_assign = int(instructor_id_str)
                else:
                    ui.display_message("No instructors available to assign.", "info")

                course_id = course_manager.add_course(name, description if description else None, instructor_id_to_assign)
                if course_id is not None:
                    ui.display_message(f"Course '{name}' added successfully with ID: {course_id}","success")
                else:
                    ui.display_message(f"Failed to add course '{name}'.","error")
            elif choice == 2: # View Course Details & Lectures
                course_id = ui.get_input("Enter Course ID to view", int)
                course = course_manager.get_course_by_id(course_id)
                if not course:
                     ui.display_message(f"Course with ID {course_id} not found.", "error")
                     continue
                
                instructor_name = "N/A"
                if course.get('InstructorID'):
                    instr = instructor_manager.get_instructor_by_id(course['InstructorID'])
                    if instr: instructor_name = instr['InstructorName']
                
                ui.display_message(f"\nDetails for Course: {course['CourseName']} (ID: {course['CourseID']})")
                print(f"  Description: {course.get('CourseDescription', 'N/A')}")
                print(f"  Instructor: {instructor_name}")
                lectures = lecture_manager.get_lectures_by_course(course_id)
                ui.display_message("Lectures in this course:")
                ui.display_table(["LectureID", "Title"], 
                                 lectures, # vua xoa if else  
                                 "NO lectures found.")
            elif choice == 3: # Update Course Info
                course_id = ui.get_input("Enter Course ID to update", int)
                course = course_manager.get_course_by_id(course_id)
                if not course:
                     ui.display_message(f"Course with ID {course_id} not found.", "error")
                     continue
                name_val = ui.get_input(f"New name (current: {course['CourseName']}, blank to keep)", str, required=False)
                desc_val = ui.get_input(f"New desc (current: {course.get('CourseDescription','N/A')}, blank to keep)", str, required=False)
                current_instructor_id = course.get('InstructorID')
                
                change_instructor = ui.get_input("Change instructor? (y/n)", str, allowed_values=['y', 'n'], required=False)
                new_instructor_id = current_instructor_id # Keep current unless changed
                if change_instructor == 'y':
                     instructors = instructor_manager.list_all_instructors()
                     if instructors:
                         ui.display_table(["InstructorID", "InstructorName"], instructors)
                         new_instructor_id_str = ui.get_input("New Instructor ID (blank for none, '0' to remove)", str, required=False,
                                                          allowed_values=[str(i['InstructorID']) for i in instructors] + ['', '0'])
                         if new_instructor_id_str == '0':
                             new_instructor_id = None
                         elif new_instructor_id_str:
                             new_instructor_id = int(new_instructor_id_str)
                         # If blank, new_instructor_id remains current_instructor_id
                     else: ui.display_message("No instructors available.", "info")

                if course_manager.update_course_info(course_id, name=name_val or None, description=desc_val or None, instructor_id=new_instructor_id):
                     ui.display_message(f"Course ID {course_id} updated successfully.", "success")
                else:
                     ui.display_message("Failed to update course.", "error")
            elif choice == 4: # Delete Course
                course_id = ui.get_input("Enter Course ID to delete", int)
                if course_manager.get_course_by_id(course_id):
                    if ui.confirm_action(f"Delete Course ID {course_id}? This cascades to lectures, enrollments, lecture views."):
                        if course_manager.delete_course(course_id):
                            ui.display_message(f"Course ID {course_id} deleted successfully.", "success")
                        else:
                            ui.display_message("Failed to delete course.", "error")
                else:
                    ui.display_message(f"Course with ID {course_id} not found.", "error")
            elif choice == 5: # Manage Lectures for a Course
                all_courses = course_manager.list_all_courses()
                if not all_courses:
                    ui.display_message("No courses available to manage lectures for.", "info")
                    continue
                ui.display_table(["CourseID", "CourseName"], all_courses)
                course_id_to_manage = ui.get_input("Enter Course ID to manage its lectures", int,
                                                allowed_values=[str(c['CourseID']) for c in all_courses])
                if course_manager.get_course_by_id(course_id_to_manage):
                    admin_handle_lecture_management(course_id_to_manage)
                else:
                     ui.display_message(f"Course with ID {course_id_to_manage} not found.", "error")
            elif choice == 6: # Back
                break
            if choice != 6: ui.pause_screen()
        except Exception as e:
            ui.display_message(f"An unexpected error in Course Management: {e}", "error")
            ui.pause_screen()

# CHECKED
def admin_handle_lecture_management(course_id: int):
    """Handles lecture management for a specific course by an Admin."""
    lecture_menu_options = [
        "List Lectures for this Course", "Add New Lecture", "Update Lecture Content", "Delete Lecture", "Back"
    ]
    course_details = course_manager.get_course_by_id(course_id)
    if not course_details:
        ui.display_message(f"Course ID {course_id} not found for lecture management.", "error")
        return
    course_name = course_details["CourseName"]

    while True:
        ui.display_menu(f"Admin: Lecture Management for '{course_name}' (ID: {course_id})", lecture_menu_options)
        choice = ui.get_input("Enter your choice", int, allowed_values=[str(i) for i in range(len(lecture_menu_options))])
        try:
            if choice == 0: # List Lectures
                lectures = lecture_manager.get_lectures_by_course(course_id)
                ui.display_table(["LectureID", "Title", "Content"],
                                 lectures if lectures else [],
                                 "NO lectures found for this course.")
            elif choice == 1: # Add New Lecture
                title = ui.get_input("Enter lecture title", str)
                content = ui.get_input("Enter lecture content (optional)", str, required=False)
                lecture_id = lecture_manager.add_lecture(course_id, title, content if content else None)
                if lecture_id is not None:
                    ui.display_message(f"Lecture '{title}' added successfully with ID: {lecture_id}", "success")
                else:
                    ui.display_message("Failed to add lecture.", "error")
            elif choice == 2: # Update Lecture Content
                lecture_id_to_update = ui.get_input("Enter Lecture ID to update", int)
                lecture = lecture_manager.get_lecture_by_id(lecture_id_to_update)
                if not lecture or lecture['CourseID'] != course_id:
                     ui.display_message(f"Lecture ID {lecture_id_to_update} not found in this course.", "error")
                     continue
                title_val = ui.get_input(f"New title (current: {lecture['Title']}, blank to keep)", str, required=False)
                content_val = ui.get_input(f"New content (blank to keep)", str, required=False)
                if lecture_manager.update_lecture_content(lecture_id_to_update, title=title_val or None, content=content_val or None):
                     ui.display_message(f"Lecture ID {lecture_id_to_update} updated successfully.", "success")
                else:
                     ui.display_message("Failed to update lecture.", "error")
            elif choice == 3: # Delete Lecture
                 lecture_id_to_delete = ui.get_input("Enter Lecture ID to delete", int)
                 lecture = lecture_manager.get_lecture_by_id(lecture_id_to_delete)
                 if not lecture or lecture['CourseID'] != course_id:
                     ui.display_message(f"Lecture ID {lecture_id_to_delete} not found in this course.", "error")
                     continue
                 if ui.confirm_action(f"Delete Lecture ID {lecture_id_to_delete} ('{lecture['Title']}')? This cascades to lecture views."):
                     if lecture_manager.delete_lecture(lecture_id_to_delete):
                         ui.display_message(f"Lecture ID {lecture_id_to_delete} deleted successfully.", "success")
                     else:
                         ui.display_message("Failed to delete lecture.", "error")
            elif choice == 4: # Back
                break
            if choice != 4: ui.pause_screen()
        except Exception as e:
            ui.display_message(f"An unexpected error in Lecture Management: {e}", "error")
            ui.pause_screen()

def admin_handle_enrollment_management():
    """Admin functions for managing enrollments."""
    enrollment_menu_options = [
        "View Enrollments (Filterable)",
        "Manually Enroll a Learner",
        "View Enrollment Logs",
        "Back to Admin Panel"
    ]
    while True:
        ui.display_menu("Admin: Enrollment Management", enrollment_menu_options)
        choice = ui.get_input("Enter your choice", int, allowed_values=[str(i) for i in range(len(enrollment_menu_options))])
        try:
            if choice == 0: # View Enrollments
                filter_by = ui.get_input("Filter by? (all, learner, course)", str, allowed_values=['all', 'learner', 'course'])
                headers = ["EnrollmentID", "LearnerName", "CourseName", "EnrollmentDate", "CompletionStatus", "ProgressPercentage"]
                display_data = []

                if filter_by == 'all':
                    enrollments_data = enrollment_manager.get_all_enrollments_detailed() 
                    if enrollments_data:
                        # Data is already a list of dictionaries with the correct keys
                        display_data = enrollments_data

                elif filter_by == 'learner':
                    learners = learner_manager.list_all_learners()
                    if not learners: ui.display_message("No learners to filter by.", "info"); continue
                    ui.display_table(["LearnerID", "LearnerName"], [{k : l[k] for k in ['LearnerID', 'LearnerName']} for l in learners])
                    learner_id_filter = ui.get_input("Enter Learner ID", int, allowed_values=[str(l['LearnerID']) for l in learners])
                    
                    # get_enrollments_by_learner returns: E.* (all from Enrollments), C.CourseName
                    enrollments_data = enrollment_manager.get_enrollments_by_learner(learner_id_filter)
                    if enrollments_data:
                        learner_info = learner_manager.get_learner_by_id(learner_id_filter)
                        selected_learner_name = learner_info['LearnerName'] if learner_info else "Unknown Learner"
                        
                        for e_data in enrollments_data:
                            # Construct a new dictionary with all required header keys
                            display_data.append({
                                "EnrollmentID": e_data['EnrollmentID'],
                                "LearnerName": selected_learner_name, # Add LearnerName
                                "CourseName": e_data['CourseName'],   # Already present
                                "EnrollmentDate": e_data['EnrollmentDate'],
                                "CompletionStatus": e_data['CompletionStatus'],
                                "ProgressPercentage": e_data['ProgressPercentage']
                            })
                elif filter_by == 'course':
                    courses = course_manager.list_all_courses()
                    if not courses: ui.display_message("No courses to filter by.", "info"); continue
                    ui.display_table(["CourseID", "CourseName"], [{k : c[k] for k in ['CourseID', 'CourseName']} for c in courses])
                    course_id_filter = ui.get_input("Enter Course ID", int, allowed_values=[str(c['CourseID']) for c in courses])
                    enrollments_data = enrollment_manager.get_enrollments_by_course(course_id_filter) # Returns E.*, L.LearnerName
                    if enrollments_data:
                        course_info = course_manager.get_course_by_id(course_id_filter)
                        selected_course_name = course_info['CourseName'] if course_info else "Unknown Course"

                        for e_data in enrollments_data:
                            # Construct a new dictionary with all required header keys
                            display_data.append({
                                "EnrollmentID": e_data['EnrollmentID'],
                                "LearnerName": e_data['LearnerName'],     # Already present
                                "CourseName": selected_course_name,     # Add CourseName
                                "EnrollmentDate": e_data['EnrollmentDate'],
                                "CompletionStatus": e_data['CompletionStatus'],
                                "ProgressPercentage": e_data['ProgressPercentage']
                            })
                
                if display_data:
                    # Pass the list of dictionaries directly to ui.display_table
                    ui.display_table(headers, display_data, "No enrollments found for the given filter.")
                else:
                    ui.display_message("No enrollments found for the given filter.", "info")

            elif choice == 1: # Manually Enroll
                learners = learner_manager.list_all_learners()
                if not learners: ui.display_message("No learners available.", "error"); continue
                ui.display_table(["LearnerID", "LearnerName"], [{k : l[k] for k in ['LearnerID', 'LearnerName']} for l in learners])
                learner_id_enroll = ui.get_input("Enter Learner ID", int, allowed_values=[str(l['LearnerID']) for l in learners])

                courses = course_manager.list_all_courses()
                if not courses: ui.display_message("No courses available.", "error"); continue
                ui.display_table(["CourseID", "CourseName"], [{k : c[k] for k in ['CourseID', 'CourseName']} for c in courses])
                course_id_enroll = ui.get_input("Enter Course ID", int, allowed_values=[str(c['CourseID']) for c in courses])
                
                if enrollment_manager.enroll_learner(learner_id_enroll, course_id_enroll): # Uses SP
                    ui.display_message(f"Learner ID {learner_id_enroll} enrolled in Course ID {course_id_enroll}.", "success")
                else:
                    ui.display_message("Failed to enroll (perhaps already enrolled, or SP error).", "error")
            
            elif choice == 2: # View Enrollment Logs
                logs = enrollment_manager.get_enrollment_logs() # Expects: LogID, EnrollmentID, LearnerName, CourseName, LogTime, ActionType
                if logs:
                    ui.display_table(["LogID", "EnrollmentID", "LearnerName", "CourseName", "LogTime", "ActionType"], 
                                     [{k : l[k] for k in ['LogID', 'EnrollmentID', 'LearnerName', 'CourseName', 'LogTime', 'ActionType']} for l in logs], 
                                     "NO enrollment logs found.")
                else:
                    ui.display_message("No enrollment logs found.", "info")

            elif choice == 3: # Back
                break
            if choice != 3: ui.pause_screen()
        except Exception as e:
            ui.display_message(f"Error in Enrollment Management: {e}", "error")
            ui.pause_screen()


def admin_handle_reports():
    """Handles displaying reports and statistics for an Admin."""
    report_menu_options = [
        "Total Number of Learners",
        "Instructor Teaching Load (All Instructors)",
        "Course Completion Summary (Per Course)",
        "List Active Courses (with Enrollment Count)",
        "Back to Admin Panel"
    ]
    while True:
        ui.display_menu("Admin: Reporting and Statistics", report_menu_options)
        choice = ui.get_input("Enter your choice", int, allowed_values=[str(i) for i in range(len(report_menu_options))])
        try:
            if choice == 0: # Total Learners
                count = len(learner_manager.list_all_learners())
                ui.display_message(f"Total number of learners: {count}")
            elif choice == 1: # Instructor Workload
                workload = instructor_manager.get_all_instructors_workload() # Queries View
                if workload:
                    ui.display_table(["InstructorName", "NumberOfCourses"], 
                                     [{k: w[k] for k in ['InstructorName', 'NumberOfCourses']} for w in workload], 
                                     "NO workload data.")
                else:
                    ui.display_message("No instructor workload data found.", "info")
            elif choice == 2: # Course Completion Summary
                courses = course_manager.list_all_courses()
                if not courses: ui.display_message("No courses available.", "error"); continue
                ui.display_table(["CourseID", "CourseName"], [{k: c[k] for k in ['CourseID', 'CourseName']} for c in courses])
                course_id_summary = ui.get_input("Enter Course ID for summary", int, allowed_values=[str(c['CourseID']) for c in courses])
                summary = enrollment_manager.get_course_progress_summary(course_id_summary) # Calls SP
                if summary:
                    ui.display_table(["LearnerName", "CourseName", "EnrollmentDate", "CompletionStatus", "ProgressPercentage"], 
                                     [{k: s[k] for k in ['LearnerName', 'CourseName', 'EnrollmentDate', 'CompletionStatus', 'ProgressPercentage']} for s in summary], 
                                     "NO summary data.")
                else:
                    ui.display_message("No completion summary found for this course.", "info")
            elif choice == 3: # List Active Courses
                active_courses_list = course_manager.list_active_courses()
                if active_courses_list:
                    ui.display_table(["CourseID", "CourseName", "EnrollmentCount"],
                                     [{k: ac[k] for k in ['CourseID', 'CourseName', 'EnrollmentCount']} for ac in active_courses_list],
                                     "No active courses found.")
                else:
                    ui.display_message("No active courses found (courses with >=1 enrollment).", "info")
            elif choice == 4: # Back
                break
            if choice != 4: ui.pause_screen()
        except Exception as e:
             ui.display_message(f"An error occurred while generating the report: {e}", "error")
             ui.pause_screen()

# --- Learner Portal Handlers ---
def handle_learner_portal():
    ui.display_message("--- Learner Portal ---")
    learners = learner_manager.list_all_learners()
    if not learners:
        ui.display_message("No learners registered in the system. Cannot proceed.", "error")
        ui.pause_screen()
        return

    ui.display_message("Available Learners:")
    ui.display_table(["LearnerID", "LearnerName"], learners)
    learner_id_portal = ui.get_input("Enter Learner ID to access their portal", int, 
                                     allowed_values=[str(l['LearnerID']) for l in learners])
    selected_learner = learner_manager.get_learner_by_id(learner_id_portal)
    if not selected_learner:
        ui.display_message(f"Learner with ID {learner_id_portal} not found.", "error"); ui.pause_screen(); return
    learner_name_portal = selected_learner['LearnerName']
    ui.display_message(f"Welcome to the Learner Portal, {learner_name_portal} (ID: {learner_id_portal})!", "success")
    ui.pause_screen()

    portal_menu_options = [
        "View My Enrolled Courses & Progress",
        "View Available Courses & Enroll",
        "Access an Enrolled Course (View/Mark Lectures)",
        "Back to Main Menu"
    ]
    while True:
        ui.display_menu(f"Learner Portal: {learner_name_portal} (ID: {learner_id_portal})", portal_menu_options)
        choice = ui.get_input("Enter your choice", int, allowed_values=[str(i) for i in range(len(portal_menu_options))])
        try:
            if choice == 0: # View My Enrolled Courses
                my_courses = enrollment_manager.get_enrollments_by_learner(learner_id_portal) 
                print(my_courses)
                if my_courses:
                    ui.display_table(["CourseName", "EnrollmentDate", "CompletionStatus", "ProgressPercentage"], 
                                     [{k: mc[k] for k in ['CourseName', 'EnrollmentDate', 
                                                                 'CompletionStatus', 'ProgressPercentage'] if k in mc}
                                                                 for mc in my_courses], 
                                     "You are NOT enrolled in any courses.")
                else:
                    ui.display_message("You are not enrolled in any courses.", "info")
            elif choice == 1: # View Available Courses & Enroll
                available_courses = course_manager.list_all_courses() 
                if not available_courses:
                    ui.display_message("No courses currently available for enrollment.", "info"); continue
                ui.display_table(["CourseID", "CourseName", "CourseDescription", "InstructorName"], 
                                 available_courses)
                enroll_choice_str = ui.get_input("Enter Course ID to enroll (or 0 to skip)", str, 
                                             allowed_values=[str(c['CourseID']) for c in available_courses] + ['0'])
                if enroll_choice_str == '0': continue
                enroll_choice_id = int(enroll_choice_str)
                if enrollment_manager.enroll_learner(learner_id_portal, enroll_choice_id):
                    ui.display_message("Successfully enrolled!", "success")
                else:
                    ui.display_message("Enrollment failed (perhaps already enrolled or course issue).", "error")
            elif choice == 2: # Access an Enrolled Course
                learner_access_enrolled_course(learner_id_portal, learner_name_portal)
            elif choice == 3: # Back
                break
            if choice != 3: ui.pause_screen()
        except Exception as e:
            ui.display_message(f"Error in Learner Portal: {e}", "error")
            ui.pause_screen()

def learner_access_enrolled_course(learner_id, learner_name): 
    # Get learner's enrolled courses
    enrolled_courses = enrollment_manager.get_enrollments_by_learner(learner_id) 
    if not enrolled_courses:
        ui.display_message(f"{learner_name}, you are not enrolled in any courses to access.", "info"); return

    ui.display_message(f"{learner_name}'s Enrolled Courses:")
    # Display table of enrolled courses
    ui.display_table(["CourseID", "CourseName", "ProgressPercentage"], 
                     [{k: ec[k] for k in ['CourseID', 
                                                        'CourseName', 'ProgressPercentage'] if k in ec}
                                                        for ec in enrolled_courses])
    # Input the CourseID to access
    course_id_to_access = ui.get_input("Enter Course ID to access", int,
                                       allowed_values=[str(ec['CourseID']) for ec in enrolled_courses])
    # Get the selected_course 
    selected_course = next((c for c in enrolled_courses if c['CourseID'] == course_id_to_access), None)
    if not selected_course:
        ui.display_message("Invalid course selection.", "error"); return
    course_name_access = selected_course['CourseName']
    
    while True:
        ui.display_message(f"\nAccessing Course: {course_name_access} (ID: {course_id_to_access}) for {learner_name}")
        # current_enrollment_details = enrollment_manager.get_enrollment_details(learner_id, course_id_to_access)
        # if current_enrollment_details:
        ui.display_message(f"  Current Progress: {selected_course['ProgressPercentage']}% - Status: {selected_course['CompletionStatus']}")
        lectures_with_status = lecture_manager.get_lectures_with_view_status(learner_id, course_id_to_access)
        ui.display_message("Lectures:")
        ui.display_table(["LectureID", "Title", "ViewStatus", "ViewDate"], 
                         [{k : l[k] for k in ['LectureID', 'Title',
                                                                 'ViewStatus', 'ViewDate'] 
                                                                 if k in l} for l in lectures_with_status], 
                         "No lectures in this course.")

        lecture_access_options = ["Back to My Courses List", "View Lecture Content"]
        ui.display_menu("Lecture Options", lecture_access_options)
        lec_choice = ui.get_input("Choice", int, allowed_values=[str(i) for i in range(len(lecture_access_options))])

        if lec_choice == 0: break
        elif lec_choice == 1: # View Content
            if not lectures_with_status: ui.display_message("No lectures to view.", "info"); ui.pause_screen(); continue
            not_viewed_lectures = [l for l in lectures_with_status if l['ViewStatus'] == 'Not Viewed']
            if not not_viewed_lectures:
                ui.display_message("All lectures in this course have been marked as viewed.", "info"); ui.pause_screen(); continue
            ui.display_message("Lectures not yet viewed:")
            ui.display_table(["LectureID", "Title"], [{k:nvl[k] for k in ['LectureID', 'Title'] if k in nvl} for nvl in not_viewed_lectures])
            lec_id_view = ui.get_input("Enter Lecture ID to view content", int, allowed_values=[str(lws['LectureID']) for lws in not_viewed_lectures])
            content = lecture_manager.get_lecture_by_id(lec_id_view)
            if content:
                ui.display_message(f"\n--- Content: {content['Title']} ---")
                print(content.get('Content', "No content available."))
                ui.display_message("--- End of Content ---")
                if enrollment_manager.mark_lecture_viewed(learner_id, lec_id_view):
                    ui.display_message("Lecture marked as viewed. Progress has been updated.", "success")
                else:
                    ui.display_message("Failed to mark lecture (already viewed or enrollment issue).", "error")

            else: ui.display_message("Lecture not found.", "error")
            ui.pause_screen()

# --- Instructor Portal Handlers ---
def handle_instructor_portal():
    ui.display_message("--- Instructor Portal ---")
    instructors = instructor_manager.list_all_instructors()
    if not instructors:
        ui.display_message("No instructors registered in the system. Cannot proceed.", "error"); ui.pause_screen(); return
    ui.display_message("Available Instructors:")
    ui.display_table(["InstructorID", "InstructorName"], 
                     [{k:i[k] for k in ['InstructorID', 'InstructorName'] if k in i}
                     for i in instructors], "NO instructors found.")
    instructor_id_portal = ui.get_input("Enter Instructor ID to access their portal", int, 
                                        allowed_values=[str(i['InstructorID']) for i in instructors])
    selected_instructor = instructor_manager.get_instructor_by_id(instructor_id_portal)
    if not selected_instructor:
        ui.display_message(f"Instructor with ID {instructor_id_portal} not found.", "error"); ui.pause_screen(); return
    instructor_name_portal = selected_instructor['InstructorName']
    ui.display_message(f"Welcome to the Instructor Portal, {instructor_name_portal} (ID: {instructor_id_portal})!", "success")
    ui.pause_screen()
    
    portal_menu_options = ["View My Assigned Courses", "Manage Lectures for an Assigned Course", 
                           "View Enrollment Roster & Progress for My Courses", "Back to Main Menu"]
    while True:
        ui.display_menu(f"Instructor Portal: {instructor_name_portal} (ID: {instructor_id_portal})", portal_menu_options)
        choice = ui.get_input("Choice", int, allowed_values=[str(i) for i in range(len(portal_menu_options))])
        try:
            if choice == 0: # My Assigned Courses
                my_courses = course_manager.get_courses_by_instructor(instructor_id_portal)
                if my_courses:
                    ui.display_table(["CourseID", "CourseName", "CourseDescription"], 
                                     [{k: mc[k] for k in ['CourseID', 
                                                                 'CourseName', "CourseDescription"] if k in mc}
                                                                 for mc in my_courses], 
                                     "You are NOT assigned to any courses.")
                else:
                    ui.display_message("You are not assigned to any courses.", "info")
            elif choice == 1: # Manage Lectures
                my_courses_for_lectures = course_manager.get_courses_by_instructor(instructor_id_portal)
                if not my_courses_for_lectures: 
                    ui.display_message("No courses assigned to manage lectures for.", "info"); ui.pause_screen(); continue
                # Display the courses assigned for instructor
                ui.display_table(["CourseID", "CourseName"], 
                                 [{k : c[k] for k in ['CourseID', 'CourseName'] if k in c}
                                 for c in my_courses_for_lectures])
                # Input for the courseID to manage its lectures 
                course_id_for_lectures = ui.get_input("Enter Course ID to manage its lectures", int,
                                                      allowed_values=[str(c['CourseID']) for c in my_courses_for_lectures])
                admin_handle_lecture_management(course_id_for_lectures) 
            elif choice == 2: # View Roster/Progress
                my_courses_for_roster = course_manager.get_courses_by_instructor(instructor_id_portal)
                if not my_courses_for_roster: 
                    ui.display_message("No courses assigned to view rosters for.", "info"); ui.pause_screen(); continue
                ui.display_table(["CourseID", "CourseName"], [{k : c[k] for k in ['CourseID', 'CourseName'] if k in c}for c in my_courses_for_roster])
                course_id_for_roster = ui.get_input("Enter Course ID to view roster/progress", int,
                                                    allowed_values=[str(c['CourseID']) for c in my_courses_for_roster])
                summary = enrollment_manager.get_course_progress_summary(course_id_for_roster) 
                if summary:
                    ui.display_table(["LearnerName", "EnrollmentDate", "CompletionStatus", "ProgressPercentage"],
                                     [{k : s[k] for k in ['LearnerName', 'EnrollmentDate', 'CompletionStatus', 'ProgressPercentage'] if k in s} for s in summary], 
                                     "NO enrollment data for this course.")
                else:
                    ui.display_message("No enrollment data found for this course.", "info")
            elif choice == 3: # Back
                break
            if choice != 3: ui.pause_screen()
        except Exception as e:
            ui.display_message(f"Error in Instructor Portal: {e}", "error")
            ui.pause_screen()

# --- Administrator Panel Handler ---
def handle_administrator_panel():
    admin_menu_options = [
        "Learner Management", "Instructor Management", "Course Management",
        "Enrollment Management", "Reporting & Statistics", "Back to Main Menu"
    ]
    while True:
        ui.display_menu("Administrator Panel", admin_menu_options)
        choice = ui.get_input("Enter your choice", int, allowed_values=[str(i) for i in range(len(admin_menu_options))])
        try:
            if choice == 0: admin_handle_learner_management()
            elif choice == 1: admin_handle_instructor_management()
            elif choice == 2: admin_handle_course_management()
            elif choice == 3: admin_handle_enrollment_management()
            elif choice == 4: admin_handle_reports()
            elif choice == 5: break # Back
        except Exception as e:
            ui.display_message(f"An unexpected error in Administrator Panel: {e}", "error")
            ui.pause_screen()

# --- Main Application Loop (Role-Based) ---
def main():
    main_menu_options = ["Exit Application", "Learner Portal", "Instructor Portal", "Administrator Panel"]
    while True:
        ui.display_menu("Online Course Management System", main_menu_options)
        choice = ui.get_input("Enter your choice", int, allowed_values=[str(i) for i in range(len(main_menu_options))])
        if choice == 0: print("\nExiting application. Goodbye!"); break
        elif choice == 1: handle_learner_portal()
        elif choice == 2: handle_instructor_portal()
        elif choice == 3: handle_administrator_panel()
        # ui.pause_screen() # Consider if pause is needed after returning from a top-level portal to main menu

if __name__ == "__main__":
    main()