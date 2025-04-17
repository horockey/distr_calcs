from flask import Flask, render_template, request
import clickhouse_connect
import os
import datetime

app = Flask(__name__)


def get_db_connection():
    try:
        conn = clickhouse_connect.get_client(
            host=os.getenv("CLICKHOUSE_HOST"), password="default")
    except Exception as e:
        print(e)
        raise e
    return conn


@app.route('/page1')
def index1():
    try:
        return index('/page1')
    except Exception as err:
        print(f"Error serving endpoint: {err}")
        return err, 500


@app.route('/page2')
def index2():
    try:
        return index('/page2')
    except Exception as err:
        print(f"Error serving endpoint: {err}")
        return err, 500


def index(path):
    try:
        cnx = get_db_connection()

        cnx.command("CREATE DATABASE IF NOT EXISTS site_visits")
        cnx.command(
            """CREATE TABLE IF NOT EXISTS site_visits.journal (
                time DateTime,
                path String,
                src_ip String,
                user_agent String,
            ) engine = MergeTree() order by time;""")
        cnx.command(
            """INSERT INTO site_visits.journal
                    (
                        time,
                        path,
                        src_ip,
                        user_agent,
                    )
                    VALUES
                    (
                        %(time)s,
                        %(path)s,
                        %(src_ip)s,
                        '%(user_agent)s'
                    )
        """, parameters={
                "time": datetime.datetime.now(),
                "path": path,
                "src_ip": request.remote_addr,
                "user_agent": request.user_agent,
            },
        )
        res = cnx.query("""
            SELECT time, src_ip, user_agent
            FROM site_visits.journal
            WHERE path = %(path)s
            ORDER BY time DESC
        """, parameters={"path": path})
        data = []
        for row in res.result_rows:
            data.append(
                {"time": row[0], "src_ip": row[1], "user_agent": row[2]}
            )
        render = render_template('index.html', data=data)

    except Exception as e:
        print(e)
        raise e
    return render


if __name__ == '__main__':
    app.run(debug=True)
