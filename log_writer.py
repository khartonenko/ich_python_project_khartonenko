from pymongo import MongoClient
from datetime import datetime, timezone, timedelta

# Подключение к MongoDB
MONGO_URI = (
    "mongodb://ich_editor:verystrongpassword@mongo.itcareerhub.de/"
    "?readPreference=primary&ssl=false&authMechanism=DEFAULT&authSource=ich_edit"
)

# Создаём клиент MongoDB и выбираем базу данных
client = MongoClient(MONGO_URI)
db = client["ich_edit"]

# Название коллекции
collection_name = "final_project_100125_khartonenko"
log_collection = db[collection_name]


def log_search(search_type, params, results_count):
    """
    Сохраняет один поисковый запрос в MongoDB.

    Аргументы:
    search_type (str): тип запроса ('keyword', 'genre_year')
    params (dict): параметры запроса (например, {'keyword': 'love'})
    results_count (int): количество результатов

    Возвращает:
    None
    """
    # Время
    timestamp = datetime.now(timezone(timedelta(hours=2)))

    log_entry = {
        "timestamp": timestamp,  # сохраняем как объект datetime
        "search_type": search_type,
        "params": params,
        "results_count": results_count
    }

    log_collection.insert_one(log_entry)
