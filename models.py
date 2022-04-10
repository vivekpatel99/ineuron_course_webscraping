from dataclasses import dataclass


@dataclass()
class Course:
    course_name: str
    description: str
    course_features: list[str]
    price: str
    what_youll_learn: list[str]
    timings: list[str]
    requirements: list[str]
    curriculum: list[str, list[str]]
    mentor_names: list[str]


@dataclass()
class Category:
    category_name: str
    course: Course
