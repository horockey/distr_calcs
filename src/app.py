from flask import Flask, render_template
import mysql.connector
from config import DATABASE_CONFIG

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(**DATABASE_CONFIG)


@app.route('/page1')
def index1():
    try:
        index('/page1')
    except Exception as err:
        return f"Error accessing database: {err}", 500


@app.route('/page2')
def index2():
    try:
        index('/page2')
    except Exception as err:
        return f"Error accessing database: {err}", 500


def index(path):
    cnx = get_db_connection()

    cnx.cmd_init_db('site_visits')
    cnx.cmd_query(
        """CREATE TABLE IF NOT EXISTS journal (
            time,
            path,
            src_ip,
            user_agent,
            primary key (time, path, src_ip)
        );""")
    cursor = cnx.cursor(dictionary=True)

    query = """
        SELECT time, src_ip, user_agent
        FROM site_visits.journal
        WHERE path = ?
        ORDER BY time DESC
    """
    cursor.execute(query, params={'path': path})

    rows = cursor.fetchall()
    cursor.close()
    cnx.close()

    return render_template('index.html', data=rows)


if __name__ == '__main__':
    app.run(debug=True)
