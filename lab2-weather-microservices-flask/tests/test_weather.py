def test_weather_no_city(client):
    response = client.get("/weather")
    assert response.status_code == 400