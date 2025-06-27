from rich.console import Console  # для вывода в консоль
from rich.table import Table      # для создания таблиц
from datetime import datetime     # для обработки времени в логах

console = Console()


def print_films(films):
    """
    Выводит список фильмов в виде таблицы с помощью библиотеки Rich.

    Аргументы:
    films (list): список словарей с полями 'title', 'release_year', 'description'

    Возвращает:
    None
    """
    if not films:
        console.print("[bold red]❌ Nothing found.[/bold red]")
        return

    table = Table(title="🎬 Film Results", show_lines=True)

    table.add_column("Title", style="cyan", no_wrap=True)
    table.add_column("Year", justify="center", style="magenta")
    table.add_column("Description", style="white")

    for film in films:
        title = film.get("title", "—")
        year = str(film.get("release_year", "—"))
        description = film.get("description", "—")
        table.add_row(title, year, description)

    console.print(table)


def print_top_keywords(keywords):
    """
    Выводит таблицу с самыми популярными ключевыми словами.

    Аргументы:
    keywords (list): список кортежей ('слово', количество)

    Возвращает:
    None
    """
    if not keywords:
        console.print("[bold yellow]⚠️ No data.[/bold yellow]")
        return

    table = Table(title="📊 Top Keywords", show_lines=True)

    table.add_column("Keyword", style="green")
    table.add_column("Count", justify="center", style="blue")

    for word, count in keywords:
        table.add_row(str(word), str(count))

    console.print(table)


def print_last_queries(queries):
    """
    Показывает последние поисковые запросы из MongoDB.

    Аргументы:
    queries (list): список словарей с полями 'timestamp', 'search_type', 'params', 'results_count'

    Возвращает:
    None
    """
    if not queries:
        console.print("[bold yellow]⚠️ No recent queries found.[/bold yellow]")
        return

    table = Table(title="📜 Last Search Queries", show_lines=True)

    table.add_column("Time", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Parameters", style="white")
    table.add_column("Results", justify="center", style="magenta")

    for q in queries:
        time = q.get("timestamp", "")
        if isinstance(time, datetime):
            time = time.strftime("%Y-%m-%d %H:%M:%S")

        stype = q.get("search_type", "")
        params = str(q.get("params", ""))
        results = str(q.get("results_count", 0))
        table.add_row(time, stype, params, results)

    console.print(table)
