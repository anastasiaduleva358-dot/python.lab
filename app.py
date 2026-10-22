from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            rating REAL NOT NULL,
            year INTEGER NOT NULL,
            image TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

#----ДОРАБОТКА----
# список + поиск + сортировка + фильтр
@app.route('/items')
def movies():

    sort = request.args.get('sort') # получает данные из урл
    search = request.args.get('search')
    genre = request.args.get('genre')

    conn = get_db_connection()

    query = 'SELECT * FROM movies WHERE 1=1' # WHERE чтобы потом удобно добавлять условия
    params = []

    # поиск
    if search:
        query += ' AND title LIKE ?'
        params.append(f'%{search}%')

    # фильтр
    if genre:
        query += ' AND genre = ?'
        params.append(genre)

    # сортировка
    if sort == 'rating':
        query += ' ORDER BY rating DESC'
    elif sort == 'year':
        query += ' ORDER BY year DESC'

    movies = conn.execute(query, params).fetchall()

    genres = conn.execute(
        'SELECT DISTINCT genre FROM movies'
    ).fetchall()

    conn.close()

    return render_template(
        'movies.html',
        movies=movies,
        genres=genres
    )

# один фильм
@app.route('/items/<int:id>')
def movie_detail(id):

    conn = get_db_connection()

    movie = conn.execute(
        'SELECT * FROM movies WHERE id = ?',
        (id,)
    ).fetchone()

    conn.close()

    if movie is None:
        return render_template('error.html')

    return render_template(
        'movie_detail.html',
        movie=movie
    )

# добавление
@app.route('/add', methods=['GET', 'POST'])
def add_movie():

    error = ''

    if request.method == 'POST':

        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        year = request.form['year']
        image = request.form['image']

#----ДОРАБОТКА----
        # пустые поля
        if not title or not genre or not rating or not year or not image:
            error = 'Заполните все поля'

        else:
            try:
                rating = float(rating)
                year = int(year)

                # рейтинг
                if rating < 0 or rating > 10:
                    error = 'Рейтинг должен быть от 0 до 10'

                # год
                elif year < 1900 or year > 2026:
                    error = 'Некорректный год'

                # ссылка
                elif not image.startswith('http'):
                    error = 'Введите корректную ссылку'

                else:
                    conn = get_db_connection()

                    conn.execute(
                        '''
                        INSERT INTO movies
                        (title, genre, rating, year, image, created_at)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ''',
                        (
                            title,
                            genre,
                            rating,
                            year,
                            image,
                            datetime.now()
                        )
                    )

                    conn.commit()
                    conn.close()

                    return redirect(url_for('movies'))

            except:
                error = 'Неверный формат данных'

    return render_template(
        'add_movie.html',
        error=error
    )

#----ДОРАБОТКА----
# редактирование
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_movie(id):

    conn = get_db_connection()

    movie = conn.execute(
        'SELECT * FROM movies WHERE id = ?',
        (id,)
    ).fetchone()

    if movie is None:
        conn.close()
        return render_template('error.html')

    error = ''

    if request.method == 'POST':

        title = request.form['title']
        genre = request.form['genre']
        rating = request.form['rating']
        year = request.form['year']
        image = request.form['image']

        if not title or not genre or not rating or not year or not image:
            error = 'Заполните все поля'

        else:
            try:
                rating = float(rating)
                year = int(year)

                conn.execute(
                    '''
                    UPDATE movies
                    SET title = ?,
                        genre = ?,
                        rating = ?,
                        year = ?,
                        image = ?
                    WHERE id = ?
                    ''',
                    (
                        title,
                        genre,
                        rating,
                        year,
                        image,
                        id
                    )
                )

                conn.commit()
                conn.close()

                return redirect(url_for('movies'))

            except:
                error = 'Ошибка данных'

    conn.close()

    return render_template(
        'edit_movie.html',
        movie=movie,
        error=error
    )

# статистика
@app.route('/stats')
def stats():

    conn = get_db_connection()

    total = conn.execute(
        'SELECT COUNT(*) FROM movies'
    ).fetchone()[0]

    avg_rating = int(conn.execute(
        'SELECT AVG(rating) FROM movies'
    ).fetchone()[0])

    by_genre = conn.execute(
        '''
        SELECT genre, COUNT(*) as count
        FROM movies
        GROUP BY genre
        '''
    ).fetchall()

    top_movie = conn.execute(
        '''
        SELECT title, rating
        FROM movies
        ORDER BY rating DESC
        LIMIT 1
        '''
    ).fetchone()

    conn.close()

    return render_template(
        'stats.html',
        total=total,
        avg_rating=avg_rating,
        by_genre=by_genre,
        top_movie=top_movie
    )

# удаление
@app.route('/delete/<int:id>')
def delete_movie(id):

    conn = get_db_connection()

    conn.execute(
        'DELETE FROM movies WHERE id = ?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for('movies'))

if __name__ == '__main__':
    app.run(debug=True)