from flask import Flask, request
import logging
import json
import boto3
import os

sqs = boto3.resource('sqs', aws_access_key_id=os.environ['ACCESS_KEY'],
                     aws_secret_access_key=os.environ['SECRET_KEY'], region_name='eu-central-1')
queue = sqs.get_queue_by_name(QueueName='BrasQueueA.fifo')

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
            queue.send_message(MessageBody=response["response"]["text"], MessageGroupId='gr1')

        elif req["request"]["original_utterance"].lower() in ["в самый низ", "конец", "в самый конец",
                                                              "вниз"]:
            response["response"]["text"] = "func_down_full"
            queue.send_message(MessageBody=response["response"]["text"], MessageGroupId='gr1')

        elif req["request"]["original_utterance"].lower() in ["выше"]:
            response["response"]["text"] = "func_up_normal"
            queue.send_message(MessageBody=response["response"]["text"], MessageGroupId='gr1')

        elif req["request"]["original_utterance"].lower() in ["ниже"]:
            response["response"]["text"] = "func_down_normal"
            queue.send_message(MessageBody=response["response"]["text"], MessageGroupId='gr1')

        elif req["request"]["original_utterance"].lower() in ["чуть выше", "немного выше"]:
            response["response"]["text"] = "func_up_abit"
            queue.send_message(MessageBody=response["response"]["text"], MessageGroupId='gr1')

        elif req["request"]["original_utterance"].lower() in ["чуть ниже", "немного ниже"]:
            response["response"]["text"] = "func_down_abit"
            queue.send_message(MessageBody=response["response"]["text"], MessageGroupId='gr1')

        elif req["request"]["original_utterance"].lower() in ["закрыть браузер"]:
            response["response"]["text"] = "func_exit"
            queue.send_message(MessageBody=response["response"]["text"], MessageGroupId='gr1')

        elif req["request"]["original_utterance"].lower() in ["вперед"]:
            response["response"]["text"] = "func_forward"
            queue.send_message(MessageBody=response["response"]["text"], MessageGroupId='gr1')

        elif req["request"]["original_utterance"].lower() in ["назад"]:
            response["response"]["text"] = "func_back"
            queue.send_message(MessageBody=response["response"]["text"], MessageGroupId='gr1')

    return json.dumps(response)
