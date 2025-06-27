# Импортируем нужные функции из других файлов
from mysql_connector import (
    search_by_keyword,
    get_genres,
    get_year_range,
    search_by_filters
)

from log_writer import log_search
from log_stats import get_last_queries, get_top_keywords
from formatter import print_films, print_top_keywords, print_last_queries


def search_keyword_flow():
    """
    Осуществляет поиск фильмов по ключевому слову с постраничным выводом.

    Пользователь вводит слово, поиск осуществляется по названию фильма.
    Выводится по 10 фильмов за раз с возможностью показа следующей страницы.
    """
    keyword = input("🔍 Enter a keyword to search for films: ")
    offset = 0
    total_shown = 0

    while True:
        results = search_by_keyword(keyword, limit=10, offset=offset)

        if not results and offset == 0:
            print("❌ Nothing found.")
            return

        print_films(results)
        total_shown += len(results)
        log_search("keyword", {"keyword": keyword}, total_shown)

        if len(results) < 10:
            print("✅ No more results.")
            break

        next_page = input("Show next 10? (y/n): ").strip().lower()
        if next_page != 'y':
            break

        offset += 10


def search_genre_year_flow():
    """
    Осуществляет поиск фильмов по жанру и/или диапазону годов.

    Пользователь может ввести только жанр, только годы, либо оба параметра.
    Поддерживается постраничный вывод по 10 результатов.
    """
    genres = get_genres()
    print("\n🎬 Genres:", ", ".join(genres))

    min_year, max_year = get_year_range()
    print(f"📆 Available year range: {min_year} to {max_year}")

    genre = input("Enter genre (optional): ").strip() or None

    try:
        year_from_input = input("Enter start year (optional): ").strip()
        year_from = int(year_from_input) if year_from_input else None

        year_to_input = input("Enter end year (optional): ").strip()
        year_to = int(year_to_input) if year_to_input else None
    except ValueError:
        print("❗ Invalid year entered.")
        return

    offset = 0
    total_shown = 0

    while True:
        results = search_by_filters(genre=genre, year_from=year_from, year_to=year_to, limit=10, offset=offset)

        if not results and offset == 0:
            print("❌ Nothing found.")
            return

        print_films(results)
        total_shown += len(results)
        log_search("genre_year", {"genre": genre, "from": year_from, "to": year_to}, total_shown)

        if len(results) < 10:
            print("✅ No more results.")
            break

        next_page = input("Show next 10? (y/n): ").strip().lower()
        if next_page != 'y':
            break

        offset += 10


def main_menu():
    """
    Отображает главное меню программы и обрабатывает выбор пользователя.

    Предлагаются 5 вариантов: поиск по ключевому слову, поиск по жанру и году,
    просмотр истории, популярных слов, или выход.
    """
    while True:
        print("\n📽️ Movie Search — Menu")
        print("1. Search by keyword")
        print("2. Search by genre and year range")
        print("3. Show recent searches")
        print("4. Show popular keywords")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == '1':
            search_keyword_flow()
        elif choice == '2':
            search_genre_year_flow()
        elif choice == '3':
            print_last_queries(get_last_queries())
        elif choice == '4':
            print_top_keywords(get_top_keywords())
        elif choice == '0':
            print("👋 Goodbye!")
            break
        else:
            print("❗ Invalid choice, try again.")


if __name__ == "__main__":
    """
    Точка входа в приложение.
    Запускает главное меню.
    """
    main_menu()
