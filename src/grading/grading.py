import json

import models


class Grader:

    def __init__(self):
        pass

    def grade_automatic_questions(self, response_id):
        task_response = models.TaskResponse.query.filter_by(id=response_id).first()
        if task_response.graded_response:
            return
        response = json.loads(task_response.response)
        task = task_response.task
        task_questions = json.loads(task.questions)
        correct_responses = 0
        total_responses = 0
        for question in response['automatic_questions']:
            for task_question in task_questions:
                if task_question['questionID'] == question['questionID']:
                    correctOption = task_question['correctOption']
                    correct = (question['selectedOption'] == correctOption)
                    question['correctOption'] = correctOption
                    question['correct'] = correct
                    question['correctOptionText'] = task_question['correctOptionText']
                    total_responses += 1
                    correct_responses += 1 if correct else 0
        task_response.graded_response = json.dumps(response)
        task_response.correctness_grade = int(float(100 * correct_responses) / total_responses)
        models.db.session.commit()
        return response['automatic_questions']