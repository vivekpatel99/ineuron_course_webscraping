import time

import fake_useragent
import selenium_stealth  # avoid detection from website that selenium is used
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager  # to avoid installation of the driver manually

import constants
from models import Course

"""
TODO: setup headless
"""


class CourseInfo(webdriver.Chrome):
    def __init__(self, driver_path=ChromeDriverManager().install(), teardown: bool = False):
        self.driver_path = driver_path
        self.teardown = teardown
        options = Options()
        user_agent = fake_useragent.UserAgent
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(f'user-agent={user_agent}')

        # options.headless = True
        # options.add_argument('--disable-gpu')  # applicable to windows os only
        super(CourseInfo, self).__init__(executable_path=self.driver_path,
                                         chrome_options=options)  # initializing init of webdriver
        self.implicitly_wait(15)
        # self.maximize_window()

    def __enter__(self):
        super(CourseInfo, self).__enter__()
        selenium_stealth.stealth(self,
                                 languages=["en-US", "en"],
                                 vendor="Google Inc.",
                                 platform="Win32",
                                 webgl_vendor="Intel Inc.",
                                 renderer="Intel Iris OpenGL Engine",
                                 fix_hairline=True, )
        return self

    def first_page(self, url: str = constants.BASE_URL) -> None:
        self.get(url)

    def scroll_down(self):
        SCROLL_PAUSE_TIME_SEC = 2  # to copy human behaviour
        # get scroll height
        last_height = self.execute_script("return document.body.scrollHeight")
        # print(last_height)
        while True:
            # scroll down to bottom
            time.sleep(SCROLL_PAUSE_TIME_SEC)
            self.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # wait to load page
            time.sleep(SCROLL_PAUSE_TIME_SEC)

            # calculate new scroll height and compare with last scroll height
            new_height = self.execute_script("return document.body.scrollHeight")
            print(new_height)
            if new_height == 4331:  # last_height:
                break
            last_height = new_height

    def fetch_courses(self) -> list[str]:
        # finding course tab and hover over it to get list of field
        courses_elem = self.find_element(by=By.ID, value='course-dropdown')
        hover = ActionChains(self).move_to_element(courses_elem)
        hover.perform()

        # find data science filed
        data_science_filed_elem = self.find_element(by=By.ID, value='603fa55d8c5e6f4b0ce22d50')
        data_science_filed_elem.click()

        # scroll down until end of the page
        self.scroll_down()

        # get list of courses links on the page
        course_links = WebDriverWait(self, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.Course_right-area__1XUfi a[href]')))
        links_list = []
        for links in course_links:
            # print(links.get_attribute('href'))
            links_list.append(links.get_attribute('href'))

        return links_list

    def get_all_info_from_page(self) -> Course:
        course_name = self.find_element(by=By.CSS_SELECTOR, value='.Hero_course-title__1a-Hg').text
        print(course_name)

        course_description = self.find_element(by=By.CSS_SELECTOR, value='.Hero_course-desc__26_LL').text
        print(course_description)

        course_price = self.find_element(by=By.CSS_SELECTOR, value='.CoursePrice_dis-price__3xw3G span').text
        print(course_price)

        course_features = self.find_elements(by=By.CSS_SELECTOR,
                                             value='div.CoursePrice_course-features__2qcJp ul li')
        features_list = []
        for feature in course_features:
            features_list.append(feature.text)
        print(features_list)

        what_youll_learn = self.find_elements(by=By.CSS_SELECTOR,
                                              value='div.CourseLearning_card__WxYAo ul li')
        topics_list = []
        for topics in what_youll_learn:
            topics_list.append(topics.text)
        print(topics_list)

        course_features = self.find_elements(by=By.CSS_SELECTOR,
                                             value='div.CoursePrice_course-features__2qcJp ul li')
        for feature in course_features:
            features_list.append(feature.text)
        print(features_list)

        try:
            class_list = {}
            timings = self.find_elements(by=By.CSS_SELECTOR,
                                         value='div div.CoursePrice_time__1I6dT')
            if timings:
                if len(timings) == 2:
                    class_list = {'class time': timings[0].text}
                    class_list = {'doubt session': timings[1].text}
                elif len(timings) == 1:
                    class_list = {'class time': timings[0].text}
            print(class_list)

        except Exception as e:
            print(e)

        requirements = self.find_elements(by=By.CSS_SELECTOR,
                                          value="div.CourseRequirement_card__3g7zR ul li")
        requirements_list = []
        for requirement in requirements:
            requirements_list.append(requirement.text)
        print(requirements_list)

        # find view more button and click in course curriculum
        view_more_button = self.find_element(by=By.CSS_SELECTOR,
                                             value='span.CurriculumAndProjects_view-more-btn__3ggZL')
        view_more_button.click()

        course_curriculum = self.find_elements(by=By.CSS_SELECTOR,
                                               value='div.CurriculumAndProjects_course-curriculum__Rlhvu')

        if course_curriculum[0].find_elements(By.CSS_SELECTOR, 'h4')[0].text == 'Course Curriculum':
            # print('[ERROR] urse Curriculum not found')
            print(course_curriculum)
            course_curriculum_dict = {}

        # for requirement in course_curriculum:
        #     requirements_list.append(requirement.text)
        # print(requirements_list)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            super(CourseInfo, self).__exit__()
            self.quit()
