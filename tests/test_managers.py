from managers.learner_manager import add_learner, get_learner_by_id, update_learner_info, list_all_learners
from managers.instructor_manager import add_instructor, get_instructor_by_id
from managers.course_manager import add_course, get_course_by_id
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

    # Test Instructor Manager
    instructor_id = add_instructor("Test Instructor", "Testing", "instructor@example.com")
    print(f"Added instructor with ID: {instructor_id}")
    instructor = get_instructor_by_id(instructor_id)
    print(f"Retrieved instructor: {instructor}")

    # Test Course Manager
    course_id = add_course("Test Course", "Description", instructor_id)
    print(f"Added course with ID: {course_id}")
    course = get_course_by_id(course_id)
    print(f"Retrieved course: {course}")

    # Test Lecture Manager
    lecture_id = add_lecture(course_id, "Test Lecture", "Content")
    print(f"Added lecture with ID: {lecture_id}")
    lecture = get_lecture_by_id(lecture_id)
    print(f"Retrieved lecture: {lecture}")

    # Test Enrollment Manager
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