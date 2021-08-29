from rest_framework.exceptions import APIException


class QuestionCantContainItems(APIException):
    status_code = 400
    default_detail = "Вопрос не может содержать вариантов ответа (тип вопроса текстовый)"