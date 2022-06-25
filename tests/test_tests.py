def test_create_test(auth_user):
    data = {
        'title': 'testtitle'
    }
    response = auth_user.post('/tests/', json=data)
    assert response.status_code == 201
