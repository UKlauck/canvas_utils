import configparser as cp
import os

from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.util import combine_kwargs, get_institution_url, obj_or_id

from .c_CanvasCourse import CanvasCourse
#from c_CanvasQuiz import CanvasQuiz


class Canvas(Canvas):

    def __init__(self, url=None, token=None, config_section=None):
        if url is None or token is None:
            config = cp.ConfigParser()
            _ = config.read(os.getenv('HOME') + '/.canvasctl/canvas.conf')
            if config_section is None:
                config_section = 'Default'
            url = config[config_section]['URL']
            if url[0] == '"':
                url = url[1:-1]
            token = config[config_section]['Token']
            if token[0] == '"':
                token = token[1:-1]
        super(Canvas,self).__init__(url, token)


    def list_courses(self):
        """
        Prints a list of all courses belonging to the user account

        :return: %
        """
        courses = self.get_courses()
        try:
            for c in courses:
                print(c.__str__())
        except:
            print(f'*** Problem printing info for course {c.id}')

    def get_course(self, course, use_sis_id=False, **kwargs):
        if use_sis_id:
            course_id = course
            uri_str = "courses/sis_course_id:{}"
        else:
            course_id = obj_or_id(course, "course", (Course,))
            uri_str = "courses/{}"

        response = self.__requester.request(
            "GET", uri_str.format(course_id), _kwargs=combine_kwargs(**kwargs)
        )
        return CanvasCourse(self.__requester, response.json())


if __name__ == "__main__":
    canvas = Canvas(config_section='Sites.GC')
    canvas.list_courses()

    # Test folders
    course = canvas.get_course(525)
    cf = course.get_course_folder()
    print(cf.full_name)

    folders = course.get_folders()
    for f in folders:
        print(f)

    # Test enrollments listing
    course.list_users()
    course.list_student_enrollments()

    # Test modules
    course.delete_all_modules()

    myModule = course.create_module(dict(name='Machine Learning I'))
    myModule.create_module_item(dict(title='Lecture Notes', type='SubHeader'))
    myModule.create_module_item(dict(title='Examples', type='SubHeader'))
    myModule.create_module_item(dict(title='Exercises', type='SubHeader'))
    myModule.create_module_item(dict(title='Datasets', type='SubHeader'))

    modules = course.get_modules()
    for mod in modules:
        print(mod)

    # Test quizzes
    course.delete_all_quizzes()
    q = course.create_quiz('New quiz')
    q.new_true_false_question('title', 'text', 'correct', 'wrong', points=1, image=None, grouped=False)

    course.list_quizzes()

