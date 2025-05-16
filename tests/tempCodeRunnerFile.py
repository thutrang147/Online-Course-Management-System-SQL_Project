from managers.learner_manager import add_learner, get_learner_by_id, update_learner_info, list_all_learners
from managers.instructor_manager import add_instructor, get_instructor_by_id
from managers.course_manager import add_course, get_course_by_id, list_all_courses
from managers.lecture_manager import add_lecture, get_lectures_by_course
from managers.enrollment_manager import enroll_learner, get_enrollments_by_learner, mark_lecture_viewed, get_learner_progress
import datetime

def run_tests():
    # Test Learner
    learner_id = add_learner("Test Learner", "test@learner.com", "1234567890")
    assert learner_id is not None, "Failed to add learner"
    learner = get_learner_by_id(learner_id)
    assert learner['LearnerName'] == "Test Learner", "Learner name mismatch"
    assert update_learner_info(learner_id, name="Updated Learner"), "Failed to update learner"
    learners = list_all_learners()
    assert any(l['LearnerID'] == learner_id for l in learners), "Learner not in list"

    # Test Instructor
    instructor_id = add_instructor("Test Instructor", "Testing", "instructor@test.com")
    assert instructor_id is not None, "Failed to add instructor"
    instructor = get_instructor_by_id(instructor_id)
    assert instructor['InstructorName'] == "Test Instructor", "Instructor name mismatch"

    # Test Course
    course_id = add_course("Test Course", "Test Description", instructor_id)
    assert course_id is not None, "Failed to add course"
    course = get_course_by_id(course_id)
    assert course['CourseName'] == "Test Course", "Course name mismatch"
    courses = list_all_courses()
    assert any(c['CourseID'] == course_id for c in courses), "Course not in list"

    # Test Lecture
    lecture_id = add_lecture(course_id, "Test Lecture", "Content")
    assert lecture_id is not None, "Failed to add lecture"
    lectures = get_lectures_by_course(course_id)
    assert any(l['LectureID'] == lecture_id for l in lectures), "Lecture not in course"

    # Test Enrollment
    assert enroll_learner(learner_id, course_id), "Failed to enroll learner"
    enrollments = get_enrollments_by_learner(learner_id)
    assert any(e['CourseID'] == course_id for e in enrollments), "Enrollment not found"

    # Test LectureViews and Progress
    assert mark_lecture_viewed(learner_id, lecture_id, datetime.date.today()), "Failed to mark lecture viewed"
    progress = get_learner_progress(learner_id, course_id)
    assert progress is not None, "Failed to get learner progress"
    assert progress == 100.0, "Progress calculation incorrect (should be 100% for 1 lecture viewed out of 1)"

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()