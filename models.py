from dataclasses import dataclass


@dataclass()
class Course:
    course_name: str
    description: str
    course_features: str
    price: str
    What_youll_learn: str
    timings: str
    requirements: str
    curriculum: str
    mentor_names: str


@dataclass()
class Category:
    category_name: str
    course: Course
