from rest_framework.exceptions import APIException


class NotAllQuestionsAnswered(APIException):
    status_code = 400
    default_detail = "Не на все вопросы опроса даны ответы"

