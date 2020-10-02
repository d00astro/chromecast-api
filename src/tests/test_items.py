import json


def test_create_summary(test_app, monkeypatch):
    def mock_generate_summary(summary_id, url):
        return None

    title = "my little item"
    description = "a very nice item"

    response = test_app.post(
        "/items/", data=json.dumps({"title": title, "description": description})
    )

    assert response.status_code == 200
    assert response.json()["title"] == title
    assert response.json()["description"] == description
