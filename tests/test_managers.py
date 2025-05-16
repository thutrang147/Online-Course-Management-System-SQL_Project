from managers.learner_manager import add_learner, get_learner_by_id, update_learner_info, list_all_learners, delete_learner
from managers.instructor_manager import add_instructor, get_instructor_by_id, delete_instructor
from managers.course_manager import add_course, get_course_by_id, delete_course
from managers.lecture_manager import add_lecture, get_lecture_by_id
from managers.enrollment_manager import enroll_learner, get_enrollments_by_learner, mark_lecture_viewed

def run_tests():
    print("Running basic unit tests...")

    # Test Learner Manager
    learner_id = add_learner("Test Learner", "test@example.com", "0901234567")
    print(f"Added learner with ID: {learner_id}")
    learner = get_learner_by_id(learner_id)
    print(f"Retrieved learner: {learner}")
    update_learner_info(learner_id, name="Updated Learner")
    learner = get_learner_by_id(learner_id)
    print(f"Updated learner: {learner}")
    learners = list_all_learners()
    print(f"All learners: {len(learners)} found")
    deleted = delete_learner(learner_id)
    print(f"Deleted learner: {deleted}")
    learner = get_learner_by_id(learner_id)
    print(f"Retrieved learner after deletion: {learner}")

    # Test Instructor Manager
    instructor_id = add_instructor("Test Instructor", "Testing", "instructor@example.com")
    print(f"Added instructor with ID: {instructor_id}")
    instructor = get_instructor_by_id(instructor_id)
    print(f"Retrieved instructor: {instructor}")
    deleted = delete_instructor(instructor_id)
    print(f"Deleted instructor: {deleted}")
    instructor = get_instructor_by_id(instructor_id)
    print(f"Retrieved instructor after deletion: {instructor}")

    # Test Course Manager
    # Re-add instructor for course (since previous one was deleted)
    instructor_id = add_instructor("New Instructor", "Testing", "new.instructor@example.com")
    course_id = add_course("Test Course", "Description", instructor_id)
    print(f"Added course with ID: {course_id}")
    course = get_course_by_id(course_id)
    print(f"Retrieved course: {course}")
    deleted = delete_course(course_id)
    print(f"Deleted course: {deleted}")
    course = get_course_by_id(course_id)
    print(f"Retrieved course after deletion: {course}")

    # Test Lecture Manager
    # Re-add course for lecture (since previous one was deleted)
    course_id = add_course("New Course", "Description", instructor_id)
    lecture_id = add_lecture(course_id, "Test Lecture", "Content")
    print(f"Added lecture with ID: {lecture_id}")
    lecture = get_lecture_by_id(lecture_id)
    print(f"Retrieved lecture: {lecture}")

    # Test Enrollment Manager
    # Re-add learner for enrollment (since previous one was deleted)
    learner_id = add_learner("New Learner", "new.learner@example.com", "0909876543")
    enrolled = enroll_learner(learner_id, course_id)
    print(f"Enrolled learner: {enrolled}")
    enrollments = get_enrollments_by_learner(learner_id)
    print(f"Enrollments: {enrollments}")
    if enrollments:
        enrollment_id = enrollments[0]['EnrollmentID']
        marked = mark_lecture_viewed(enrollment_id, lecture_id)
        print(f"Marked lecture viewed: {marked}")

if __name__ == "__main__":
    run_tests()