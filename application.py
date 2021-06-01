from flask import Flask, request
import logging
import json
import boto3

application = Flask(__name__)
app = application

logging.basicConfig(level=logging.DEBUG)

sqs = boto3.resource('sqs', aws_access_key_id='AKIATYQ65N6IQPDTBLDQ',
                     aws_secret_access_key='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', region_name='eu-central-1')

queue_url = 'SQS_QUEUE_URL'


@application.route("/", methods=["POST"])
def main():
    logging.info(request.json)

    response = {
        "version": request.json["version"],
        "session": request.json["session"],
        "response": {
            "end_session": False
        }
    }

    req = request.json
    if req["session"]["new"]:
        response["response"][
            "text"] = "Привет! Меня зовут Алиса, я твой Голосовой помощник для управления страницей браузера.\nЧтобы узнать список моих команд, скажите слово 'Команды'."
    else:
        if req["request"]["original_utterance"].lower() in ["команды", "список команд"]:
            response["response"]["text"] = "Список команд для работы с браузером(можно использовать синонимы):\n" \
                                           "Для навигации по странице: 1)Наверх 2)Выше 3)Чуть выше. По аналогии с перемещением вниз.\n" \
                                           "Для перехода между страницами: 1)Вперед 2)Назад.\n" \
                                           "Для закрытия браузера: 1)Закрыть браузер."
        elif req["request"]["original_utterance"].lower() in ["в начало страницы", "начало", "в самое начало",
                                                              "наверх"]:
            response["response"]["text"] = "func_up_full"
            sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=response["response"]["text"])

        elif req["request"]["original_utterance"].lower() in ["в самый низ", "конец", "в самый конец",
                                                              "вниз"]:
            response["response"]["text"] = "func_down_full"
            sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=response["response"]["text"])

        elif req["request"]["original_utterance"].lower() in ["выше"]:
            response["response"]["text"] = "func_up_normal"
            sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=response["response"]["text"])

        elif req["request"]["original_utterance"].lower() in ["ниже"]:
            response["response"]["text"] = "func_down_normal"
            sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=response["response"]["text"])

        elif req["request"]["original_utterance"].lower() in ["чуть выше", "немного выше"]:
            response["response"]["text"] = "func_up_abit"
            sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=response["response"]["text"])

        elif req["request"]["original_utterance"].lower() in ["чуть ниже", "немного ниже"]:
            response["response"]["text"] = "func_down_abit"
            sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=response["response"]["text"])

        elif req["request"]["original_utterance"].lower() in ["закрыть браузер"]:
            response["response"]["text"] = "func_exit"
            sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=response["response"]["text"])

        elif req["request"]["original_utterance"].lower() in ["вперед"]:
            response["response"]["text"] = "func_forward"
            sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=response["response"]["text"])

        elif req["request"]["original_utterance"].lower() in ["назад"]:
            response["response"]["text"] = "func_back"
            sqs.send_message(QueueUrl=queue_url, DelaySeconds=10, MessageBody=response["response"]["text"])

    return json.dumps(response)
