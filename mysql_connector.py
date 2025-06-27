import pymysql

MYSQL = {
    'host': 'ich-db.edu.itcareerhub.de',
    'user': 'ich1',
    'password': 'password',
    'database': 'sakila'
}


def get_connection():
    """
    Создаёт и возвращает подключение к MySQL.
    """
    return pymysql.connect(**MYSQL, cursorclass=pymysql.cursors.DictCursor)


def search_by_keyword(keyword, limit=10, offset=0):
    """
    Поиск фильмов по ключевому слову в названии.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = """
        SELECT title, release_year, description
        FROM film
        WHERE title LIKE %s
        LIMIT %s OFFSET %s
        """
        cursor.execute(sql, (f"%{keyword}%", limit, offset))
        result = cursor.fetchall()
    conn.close()
    return result


def get_genres():
    """
    Получает список всех жанров.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT name FROM category")
        genres = [row["name"] for row in cursor.fetchall()]
    conn.close()
    return genres


def get_year_range():
    """
    Получает минимальный и максимальный год.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT MIN(release_year) AS min_year, MAX(release_year) AS max_year FROM film")
        result = cursor.fetchone()
    conn.close()
    return result["min_year"], result["max_year"]


def search_by_filters(genre=None, year_from=None, year_to=None, limit=10, offset=0):
    """
    Поиск фильмов по фильтрам: жанр и/или год.
    Любой из фильтров может быть пропущен.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = """
        SELECT f.title, f.release_year, f.description
        FROM film f
        LEFT JOIN film_category fc ON f.film_id = fc.film_id
        LEFT JOIN category c ON fc.category_id = c.category_id
        WHERE 1=1
        """
        params = []

        if genre:
            sql += " AND c.name = %s"
            params.append(genre)

        if year_from is not None and year_to is not None:
            sql += " AND f.release_year BETWEEN %s AND %s"
            params.extend([year_from, year_to])
        elif year_from is not None:
            sql += " AND f.release_year >= %s"
            params.append(year_from)
        elif year_to is not None:
            sql += " AND f.release_year <= %s"
            params.append(year_to)

        sql += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

        cursor.execute(sql, tuple(params))
        result = cursor.fetchall()
    conn.close()
    return result
