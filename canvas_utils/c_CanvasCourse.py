#import configparser as cp
#import os

#from canvasapi import Canvas
from canvasapi.course import Course
from canvasapi.util import combine_kwargs     #, get_institution_url, obj_or_id

from .c_CanvasQuiz import CanvasQuiz


class CanvasCourse(Course):
    def __init__(self, requester, attributes):
        super(Course, self).__init__(requester, attributes)


    def create_module_2(self, module, **kwargs):
        """
        Create a new module.

        :calls: `POST /api/v1/courses/:course_id/modules \
        <https://canvas.instructure.com/doc/api/modules.html#method.context_modules_api.create>`_

        :param module: The attributes for the module.
        :type module: dict
        :returns: The created module.
        :rtype: :class:`canvasapi.module.Module`
        """
        from canvasapi.module import Module

        if isinstance(module, dict) and "name" in module:
            kwargs["module"] = module
        else:
            raise RequiredFieldMissing("Dictionary with key 'name' is required.")

        response = self._requester.request(
            "POST",
            "courses/{}/modules".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        module_json = response.json()
        module_json.update({"course_id": self.id})

        return Module(self._requester, module_json)

    def create_quiz(self,
                    title='Quiz',
                    description='',
                    quiz_type='practice_quiz',
                    assignment_group_id=None,
                    time_limit=None,
                    shuffle_answers=True,
                    hide_results='always',
                    show_correct_answers=False,
                    show_correct_answers_last_attempt=False,
                    show_correct_answers_at=None,
                    hide_correct_answers_at=None,
                    allowed_attempts=1,
                    scoring_policy='keep_latest',
                    one_question_at_a_time=False,
                    cant_go_back=False,
                    access_code=None,
                    ip_filter=None,
                    due_at=None,
                    lock_at=None,
                    unlock_at=None,
                    published=False,
                    one_time_results=False,
                    only_visible_to_overrides=False,
                    **kwargs):

        quiz = dict(title=title, description=description, quiz_type=quiz_type,
                    assignment_group_id=assignment_group_id, time_limit=time_limit, shuffle_answers=shuffle_answers,
                    hide_results=hide_results, show_correct_answers=show_correct_answers,
                    show_correct_answers_last_attempt=show_correct_answers_last_attempt,
                    show_correct_answers_at=show_correct_answers_at,
                    hide_correct_answers_at=hide_correct_answers_at, allowed_attempts=allowed_attempts,
                    scoring_policy=scoring_policy, one_question_at_a_time=one_question_at_a_time,
                    cant_go_back=cant_go_back, access_code=access_code, ip_filter=ip_filter, due_at=due_at,
                    lock_at=lock_at, unlock_at=unlock_at, published=published, one_time_results=one_time_results,
                    only_visible_to_overrides=only_visible_to_overrides)

        kwargs["quiz"] = quiz

        response = self._requester.request(
            "POST",
            "courses/{}/quizzes".format(self.id),
            _kwargs=combine_kwargs(**kwargs),
        )
        quiz_json = response.json()
        quiz_json.update({"course_id": self.id})

        my_quiz = CanvasQuiz(self._requester, quiz_json)
        my_quiz.course = self

        return my_quiz


    def list_quizzes(self):
        quizzes = self.get_quizzes()
        for q in quizzes:
            print(q.__str__())


    def delete_all_quizzes(self):
        quizzes = self.get_quizzes()
        for q in quizzes:
            q.delete()


    def delete_folders(self):
        folders = self.course.get_folders()
        for folder in folders:
            if folder.full_name != 'course files':
                folder.delete()
        return folder


    def get_course_folder(self):
        folders = self.get_folders()
        for folder in folders:
            if folder.full_name == 'course files':
                return folder
        return None


    def create_folders(self, folders):
        root = self.get_course_folder()
        if type(folders) is list:
            for f in folders:
                root.create_folder(f)
        else:
            root.create_folder(folders)


    def delete_all_files(self):
        files = self.get_files()
        for f in files:
            f.delete()


    def delete_all_modules(self):
        modules = self.get_modules()
        for mod in modules:
            mod.delete()


    def list_student_enrollments(self):
        el = self.get_enrollments(type=['StudentEnrollment'])
        s = self.name+' ('+str(self.id)+')'
        print('%s\n%s\n'%(s, '-'*len(s)))

        for l in el:
            print('%s   (%s)'%(l.user['sortable_name'], str(l.user['id'])))
        print('')


    def list_users(self, enrollment_type=['student']):
        users = self.get_users(enrollment_type=enrollment_type)
        user_list = list(users)
        print(f'{len(user_list):d} Einschreibungen\n')

        for u in users:
            print('%s%s%s'%(u.sortable_name, ' '*(40-len(u.sortable_name)), u.created_at))

        print('\n\n')

