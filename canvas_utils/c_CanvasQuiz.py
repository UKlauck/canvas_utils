#import configparser as cp
#import os

#from canvasapi import Canvas
#from canvasapi.course import Course
#from canvasapi.util import combine_kwargs, get_institution_url, obj_or_id
#from canvasapi.util import uri_str

from canvasapi.quiz import Quiz

class CanvasQuiz(Quiz):
    def __init__(self, requester, attributes):
        super(Quiz, self).__init__(requester, attributes)
        self.groups = []
        self.questions = []

    def new_quiz_group(self, name='', pick_count=1, points=0):
        """
        Creates a group of questios.

        :param name:        group name
        :param pick_count:  no of questions picked from the group members for each student
        :param points:      no of points used for grading
        :return:            %
        """
        quiz_group = [
            dict(name=name, pick_count=pick_count, question_points=points)
        ]
        self.quiz_group = self.create_question_group(quiz_group)
        self.groups.append(self.quiz_group)

    def new_mc_question(self, title, text, correct, wrong, points=1, image=None, grouped=False):
        """
        Creates a multiple choice question

        :param title:   question title (str)
        :param text:    question text (str)
        :param correct: text for the correct answer (str or list, if list, only the first element is used)
        :param wrong:   list of wrong answers (list of str)
        :param points:  no of points used for grading
        :param grouped: add to group? (bool)
        :return:        %
        """

        answers = []
        if type(correct) == list:
            answers.append({'text': correct[0], 'weight': 100})
        else:
            answers.append({'text': correct, 'weight': 100})
        for w in wrong:
            answers.append({'text': w, 'weight': 0})

        text = self.handle_image(text, image)

        new_question = dict(question_name=title, question_type='multiple_choice_question', question_text=text,
                            points_possible=points, correct_comments='', incorrect_comments='', neutral_comments='',
                            correct_comments_html='', incorrect_comments_html='', neutral_comments_html='',
                            answers=answers)

        if grouped:
            new_question['quiz_group_id'] = self.quiz_group.id

        question = self.create_question(question=new_question)
        self.questions.append(question)

    def new_multi_answer_question(self, title, text, correct, wrong, points=1, image=None, grouped=False):
        """
        Creates a multi answer question. Different correct or wrong answers can be selected.

        :param title:   question title (str)
        :param text:    question text (str)
        :param correct: list of correct answers (list of str)
        :param wrong:   list of wrong answers (list of str)
        :param points:  no of points used for grading
        :param grouped: add to group? (bool)
        :return:        %
        """
        answers = []
        for c in correct:
            answers.append({'text': c, 'weight': 100})
        for w in wrong:
            answers.append({'text': w, 'weight': 0})

        text = self.handle_image(text, image)

        new_question = dict(question_name=title, question_type='multiple_answers_question', question_text=text,
                            points_possible=points, correct_comments='', incorrect_comments='', neutral_comments='',
                            correct_comments_html='', incorrect_comments_html='', neutral_comments_html='',
                            answers=answers)

        if grouped:
            new_question['quiz_group_id'] = self.quiz_group.id

        question = self.create_question(question=new_question)
        self.questions.append(question)

    def new_numerical_question(self, title, text,
                               answer=None, precision=None, errorMargin=None,
                               begin=None, end=None, points=1, image=None, grouped=False):
        """
        Creates a numerical question. Depending on the parameters provided, the answer is an exact answer with
        error margins or an exact answer with a given precision or a range with a given start and end

        :param title:   question title (str)
        :param text:    question text (str)
        :param answer:  correct answer with precision or error margins (numerical, optional)
        :param precision: precision for the given answer (numerical)
        :param errorMargin: error margin for the given answer (numerical)
        :param begin:   start of a range answer (numerical)
        :param end:     end of a range answer (numerical)
        :param points:  no of points used for grading
        :param grouped: add to group? (bool)
        :return:        %
        """

        if answer is not None and precision is not None:
            answer = [
                dict(numerical_answer_type='precision_answer', answer_approximate=answer, answer_precision=precision)
            ]
        elif answer is not None and errorMargin is not None:
            answer = [
                dict(numerical_answer_type='exact_answer', answer_exact=answer, answer_error_margin=errorMargin)
            ]
        elif begin is not None and end is not None:
            answer = [
                dict(numerical_answer_type='range_answer', answer_range_start=begin, answer_range_end=end)
            ]

        text = self.handle_image(text, image)

        new_question = dict(question_name=title, question_type='numerical_question', question_text=text,
                            points_possible=points, correct_comments='', incorrect_comments='', neutral_comments='',
                            correct_comments_html='', incorrect_comments_html='', neutral_comments_html='',
                            answers=answer)

        if grouped:
            new_question['quiz_group_id'] = self.quiz_group.id

        question = self.create_question(question=new_question)
        self.questions.append(question)

    def new_essay_question(self, title, text, points=1, image=None, grouped=False):
        """
        Creates an essay question which provides an editor

        :param title:   question title (str)
        :param text:    question text (str)
        :param points:  no of points used for grading
        :param grouped: add to group? (bool)
        :return:        %
        """

        text = self.handle_image(text, image)

        new_question = dict(question_name=title, question_type='essay_question', question_text=text,
                            points_possible=points, correct_comments='', incorrect_comments='', neutral_comments='',
                            correct_comments_html='', incorrect_comments_html='', neutral_comments_html='', answers=[])

        if grouped:
            new_question['quiz_group_id'] = self.quiz_group.id

        question = self.create_question(question=new_question)
        self.questions.append(question)

    def new_file_upload_question(self, title, text, points=0, image=None, grouped=False):
        """
        Create a file upload question. A file selection field is provided.

        :param title:   question title (str)
        :param text:    question text (str)
        :param points:  no of points used for grading
        :param grouped: add to group? (bool)
        :return:        %
        """

        text = self.handle_image(text, image)

        new_question = dict(question_name=title, question_type='file_upload_question', question_text=text,
                            points_possible=points, correct_comments='', incorrect_comments='', neutral_comments='',
                            correct_comments_html='', incorrect_comments_html='', neutral_comments_html='', answers=[])

        if grouped:
            new_question['quiz_group_id'] = self.quiz_group.id

        question = self.create_question(question=new_question)
        self.questions.append(question)

    def new_short_answer_question(self, title, text, correct, points=1, image=None, grouped=False):
        """

        :param title:   question title (str)
        :param text:    question text (str)
        :param correct: possible correct answers (list of str)
        :param points:  no of points used for grading
        :param grouped: add to group? (bool)
        :return:        %
        """

        answers = []
        for c in correct:
            answers.append({'text': c, 'weight': 100})

        text = self.handle_image(text, image)

        new_question = dict(question_name=title, question_type='short_answer_question', question_text=text,
                            points_possible=points, correct_comments='', incorrect_comments='', neutral_comments='',
                            correct_comments_html='', incorrect_comments_html='', neutral_comments_html='',
                            answers=answers)

        if grouped:
            new_question['quiz_group_id'] = self.quiz_group.id

        question = self.create_question(question=new_question)
        self.questions.append(question)

    def new_true_false_question(self, title, text, correct, wrong, points=1, image=None, grouped=False):
        """
        Create a true_false question

        :param title:   question title (str)
        :param text:    question text (str)
        :param correct: text for the true item (str or list. If list, only the first element is used)
        :param wrong:   text for the false item (str or list. If list, only the first element is used)
        :param points:  no of points used for grading
        :param grouped: add to group? (bool)
        :return:        %
        """
        answers = []
        if type(correct) == list:
            answers.append({'text': correct[0], 'weight': 100})
        else:
            answers.append({'text': correct, 'weight': 100})

        if type(wrong) == list:
            answers.append({'text': wrong[0], 'weight': 0})
        else:
            answers.append({'text': wrong, 'weight': 0})

        text = self.handle_image(text, image)

        new_question = dict(question_name=title, question_type='true_false_question', question_text=text,
                            points_possible=points, correct_comments='', incorrect_comments='', neutral_comments='',
                            correct_comments_html='', incorrect_comments_html='', neutral_comments_html='',
                            answers=answers)

        if grouped:
            new_question['quiz_group_id'] = self.quiz_group.id

        question = self.create_question(question=new_question)
        self.questions.append(question)

    def new_text_only_question(self, title, text, image=None, grouped=False):
        """
        Create a text only question which is not graded. Useful for descriptive text for subsequent questions

        :param title: question title (str)
        :param text:  question text (str)
        :param grouped: add to group? (bool)
        :return: %
        """
        text = self.handle_image(text, image)

        new_question = dict(question_name=title, question_type='text_only_question', question_text=text,
                            points_possible=None, correct_comments='', incorrect_comments='', neutral_comments='',
                            correct_comments_html='', incorrect_comments_html='', neutral_comments_html='', answers=[])
        if grouped:
            new_question['quiz_group_id'] = self.quiz_group.id

        question = self.create_question(question=new_question)
        self.questions.append(question)

    def new_fill_blanks_question(self, title, text, blanks, points=1, image=None, grouped=False):
        """

        :param title:   question title (str)
        :param text:    question text (str). Use [a], [b], ... for blanks
        :param blanks:  list of lists of str. For each blank a list of str is required
        :param points:  no of points used for grading
        :param grouped: add to group? (bool)
        :return:        %
        """
        answers = []
        blank_id = 'a'
        for bb in blanks:
            for b in bb:
                answers.append({
                    'text':b,
                    'weight':100,
                    'blank_id': blank_id
                })
            blank_id = chr(ord(blank_id)+1)

        text = self.handle_image(text, image)

        new_question = dict(question_name=title, question_type='fill_in_multiple_blanks_question', question_text=text,
                            points_possible=points, correct_comments='', incorrect_comments='', neutral_comments='',
                            correct_comments_html='', incorrect_comments_html='', neutral_comments_html='',
                            answers=answers)
        if grouped:
            new_question['quiz_group_id'] = self.quiz_group.id

        question = self.create_question(question=new_question)
        self.questions.append(question)


    def get_question(self, question_id):
        return self.quiz.get_question(question_id)


    def handle_image(self, text, image):
        if image is not None:
            success, res = self.course.upload(image, parent_folder_path='/Images')
            #success, res = self.upload(image, parent_folder_path='/Images')
            if success:
                image_ref = res['preview_url']
                pos = image_ref.find('file_preview')
                if pos != -1:
                    image_ref = '<img src="' + \
                        image_ref[:pos] + \
                        'preview" alt="You should see an image here"  />'
                    kw = '%IMAGE%'
                    pos = text.find(kw)
                    if pos != -1:
                        text = text[:pos] + image_ref + text[pos+len(kw):]
        return text
