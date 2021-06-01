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

sessionStorage = {}

name = ''


@application.route('/post', methods=['POST'])
def main():
    ## Создаем ответ
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    ## Заполняем необходимую информацию
    handle_dialog(response, request.json)
    return json.dumps(response)


def handle_dialog(res, req):
    if req["session"]["new"]:
        res["response"][
            "text"] = "Привет! Меня зовут Алиса, я твой Голосовой помощник для управления страницей браузера.\nЧтобы узнать список моих команд, скажите слово 'Команды'."
    else:
        if req["request"]["original_utterance"].lower() in ["команды", "список команд"]:
            res["response"]["text"] = "Список команд для работы с браузером(можно использовать синонимы):\n" \
                                      "Для навигации по странице: 1)Наверх 2)Выше 3)Чуть выше. По аналогии с перемещением вниз.\n" \
                                      "Для перехода между страницами: 1)Вперед 2)Назад.\n" \
                                      "Для закрытия браузера: 1)Закрыть браузер."
        elif req["request"]["original_utterance"].lower() in ["в начало страницы", "начало", "в самое начало",
                                                              "наверх"]:
            res["response"]["text"] = "func_up_full"

        elif req["request"]["original_utterance"].lower() in ["в самый низ", "конец", "в самый конец",
                                                              "вниз"]:
            res["response"]["text"] = "func_down_full"

        elif req["request"]["original_utterance"].lower() in ["выше"]:
            res["response"]["text"] = "func_up_normal"
            sqs_func('func_up_normal')

        elif req["request"]["original_utterance"].lower() in ["ниже"]:
            res["response"]["text"] = "func_down_normal"

        elif req["request"]["original_utterance"].lower() in ["чуть выше", "немного выше"]:
            res["response"]["text"] = "func_up_abit"

        elif req["request"]["original_utterance"].lower() in ["чуть ниже", "немного ниже"]:
            res["response"]["text"] = "func_down_abit"

        elif req["request"]["original_utterance"].lower() in ["закрыть браузер"]:
            res["response"]["text"] = "func_exit"

        elif req["request"]["original_utterance"].lower() in ["вперед"]:
            res["response"]["text"] = "func_forward"

        elif req["request"]["original_utterance"].lower() in ["назад"]:
            res["response"]["text"] = "func_back"


if __name__ == '__main__':
    application.run()
