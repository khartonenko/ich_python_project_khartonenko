from pymongo import MongoClient
from collections import Counter  # нужен для подсчёта самых популярных слов

# Подключение к MongoDB
MONGO_URI = (
    "mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/"
    "?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"
)

# Создаём клиента Mongo и подключаемся к базе и коллекции
client = MongoClient(MONGO_URI)
db = client["ich_edit"]
collection = db["final_project_100125_khartonenko"]


def get_last_queries(limit=5):
    """
    Возвращает последние N поисковых запросов.

    Аргументы:
    limit (int): сколько запросов вернуть (по умолчанию 5)

    Возвращает:
    list: список последних документов из MongoDB
    """
    # Сортируем по времени в обратном порядке и берём нужное количество
    return list(collection.find().sort("timestamp", -1).limit(limit))


def get_top_keywords(limit=5):
    """
    Возвращает самые частые ключевые слова из запросов по типу 'keyword'.

    Аргументы:
    limit (int): сколько самых популярных слов показать (по умолчанию 5)

    Возвращает:
    list: список кортежей ('слово', количество)
    """
    keywords = []  # сюда собираем все ключевые слова

    # Перебираем все запросы с типом 'keyword'
    for log in collection.find({"search_type": "keyword"}):
        if "params" in log and "keyword" in log["params"]:
            kw = log["params"]["keyword"]
            keywords.append(kw.lower())  # добавляем слово в нижнем регистре

    # Считаем сколько раз встречается каждое слово
    top = Counter(keywords).most_common(limit)
    return top
