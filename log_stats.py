from pymongo import MongoClient
from collections import Counter

MONGO_URI = (
    "mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/"
    "?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"
)

client = MongoClient(MONGO_URI)
db = client["ich_edit"]
collection = db["final_project_100125_khartonenko"]


def get_last_queries(limit=5):
    """
    Возвращает последние 5 поисковых запросов.
    """
    # Сортирует по времени в обратном порядке и берёт нужное количество
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
            keywords.append(kw.lower())

    # Считает сколько раз встречается каждое слово
    top = Counter(keywords).most_common(limit)
    return top
