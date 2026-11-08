import sqlite3

from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    redirect,
    url_for
)

main = Blueprint("main", __name__)


def get_db():
    connection = sqlite3.connect(
        current_app.config["DATABASE"]
    )
    connection.row_factory = sqlite3.Row
    return connection


@main.route("/")
def index():
    connection = get_db()

    tasks = connection.execute(
        "SELECT * FROM tasks ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return render_template("index.html", tasks=tasks)


@main.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()

    if title:
        connection = get_db()
        connection.execute(
            "INSERT INTO tasks (title) VALUES (?)",
            (title,)
        )
        connection.commit()
        connection.close()

    return redirect(url_for("main.index"))


@main.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    connection = get_db()

    connection.execute(
        """
        UPDATE tasks
        SET completed = CASE completed
            WHEN 0 THEN 1
            ELSE 0
        END
        WHERE id = ?
        """,
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("main.index"))


@main.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    connection = get_db()

    connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("main.index"))