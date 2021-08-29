from rest_framework.exceptions import APIException


class PollDoesNotHaveThisQuestion(APIException):
    status_code = 400
    default_detail = "У данного опроса нет этого вопроса"


class AnswerByThisQuestionMustHaveItem(APIException):
    status_code = 400
    default_detail = "Ответ на данный вопрос должен быть выбран из вариантов"


class AnswerByThisQuestionMustHaveText(APIException):
    status_code = 400
    default_detail = "Ответ на данный вопрос должен содержать текстовый ответ"


class AnswerOnThisQuestionAlreadyExists(APIException):
    status_code = 400
    default_detail = "Ответ на данный вопрос сессии опроса уже существует"


class AnswerItemOnThisMultiQuestionAlreadyExists(APIException):
    status_code = 400
    default_detail = "Вариант ответа на данный вопрос сессии опроса уже существует"


class AnswerOnFinishedPollSession(APIException):
    status_code = 400
    default_detail = "Попытка ответить на вопрос сессии опроса, которая завершена"


