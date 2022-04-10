import time

from course_info import CourseInfo
from excel import Excel
from models import Category, Course


def main():
    # safely close after use of browser
    with CourseInfo() as course_info:
        excel = Excel()
        course_info.goto_page()
        courses_categories_dict = course_info.fetch_courses_links_list_with_category()
        for category_name in courses_categories_dict:
            courses_links = course_info.get_courses_links_from_category_link(
                course_link=courses_categories_dict[category_name])

            for course_link in courses_links:
                course_info.goto_page(course_link)
                course = course_info.get_all_info_from_page()
                category = Category(category_name=category_name, course=course)

                excel.write_excel_file_by_row(category_obj=category)
                time.sleep(3)


if __name__ == '__main__':
    main()
