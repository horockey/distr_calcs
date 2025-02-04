# app.py
from flask import Flask, render_template
import mysql.connector
from config import DATABASE_CONFIG

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(**DATABASE_CONFIG)


@app.route('/page1')
def index1():
    index('/page1')


@app.route('/page2')
def index2():
    index('/page2')


def index(path):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)

        query = """
            SELECT time, src_ip, user_agent
            FROM your_table_name
            WHERE path = ?
            ORDER BY time DESC
        """
        cursor.execute(query, params={'path': path})

        rows = cursor.fetchall()
        cursor.close()
        cnx.close()

        return render_template('index.html', data=rows)

    except mysql.connector.Error as err:
        return f"Error accessing database: {err}", 500


if __name__ == '__main__':
    app.run(debug=True)
