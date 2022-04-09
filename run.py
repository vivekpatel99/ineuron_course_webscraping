import time

from course_info import CourseInfo


def main():
    # safely close after use of browser
    with CourseInfo() as course_info:
        course_info.first_page(url='https://courses.ineuron.ai/Full-Stack-Data-Science-Bootcamp')
        print(course_info.get_all_info_from_page())
        # course_info.fetch_courses()
        time.sleep(3)


if __name__ == '__main__':
    main()
