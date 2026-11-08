import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    db_path = tmp_path / "test.db"

    app = create_app({
        "TESTING": True,
        "DATABASE": str(db_path)
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_homepage(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Task Manager" in response.data


def test_add_task(client):
    response = client.post("/add", data={
        "title": "Learn Docker"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Learn Docker" in response.data


def test_complete_task(client):
    client.post("/add", data={
        "title": "Learn CI/CD"
    })

    response = client.post(
        "/complete/1",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"completed" in response.data


def test_delete_task(client):
    client.post("/add", data={
        "title": "Temporary task"
    })

    response = client.post(
        "/delete/1",
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"Temporary task" not in response.data


def test_empty_task_is_not_added(client):
    response = client.post(
        "/add",
        data={"title": "   "},
        follow_redirects=True
    )

    assert response.status_code == 200
    assert b"No tasks yet" in response.data