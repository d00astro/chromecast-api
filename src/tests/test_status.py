def test_status(test_app):
    # Given
    # test_app

    # When
    response = test_app.get("/status")

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "environment": "dev",
        "status": "running",
        "testing": True,
    }
