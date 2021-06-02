from flask import Flask, request
import logging
import json
import boto3


def sqs_func(name):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='BrasQueueA.fifo')
    queue.send_message(MessageBody=name, MessageGroupId='gr1')


application = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@application.route("/", methods=["POST"])
def main():
    logging.info('Request: %r', request.json)

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
            "text"] = "Привет! Меня зовут Алиса, я твой Голосовой помощник для управления страницей браузера.\n" \
                      "Чтобы узнать список моих команд, скажите слово 'Команды'."
    else:
        if req["request"]["original_utterance"].lower() in ["команды", "список команд"]:
            response["response"]["text"] = "Список команд для работы с браузером(можно использовать синонимы):\n" \
                                           "Для навигации по странице: 1)Наверх 2)Выше 3)Чуть выше. По аналогии с перемещением вниз.\n" \
                                           "Для перехода между страницами: 1)Вперед 2)Назад.\n" \
                                           "Для закрытия браузера: 1)Закрыть браузер."
        elif req["request"]["original_utterance"].lower() in ["в начало страницы", "начало", "в самое начало",
                                                              "наверх"]:
            response["response"]["text"] = "func_up_full"

        elif req["request"]["original_utterance"].lower() in ["в самый низ", "конец", "в самый конец",
                                                              "вниз"]:
            response["response"]["text"] = "func_down_full"

        elif req["request"]["original_utterance"].lower() in ["выше"]:
            response["response"]["text"] = "func_up_normal"
            sqs_func('func_up_normal')

        elif req["request"]["original_utterance"].lower() in ["ниже"]:
            response["response"]["text"] = "func_down_normal"

        elif req["request"]["original_utterance"].lower() in ["чуть выше", "немного выше"]:
            response["response"]["text"] = "func_up_abit"

        elif req["request"]["original_utterance"].lower() in ["чуть ниже", "немного ниже"]:
            response["response"]["text"] = "func_down_abit"

        elif req["request"]["original_utterance"].lower() in ["закрыть браузер"]:
            response["response"]["text"] = "func_exit"

        elif req["request"]["original_utterance"].lower() in ["вперед"]:
            response["response"]["text"] = "func_forward"

        elif req["request"]["original_utterance"].lower() in ["назад"]:
            response["response"]["text"] = "func_back"

    return json.dumps(response), sqs_func(response["response"]["text"])
