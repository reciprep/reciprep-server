import json

def req_user_register(test_case, email, username, password):
    return test_case.client.post(
        '/api/auth/register',
        data=json.dumps(dict(
            email=email,
            username=username,
            password=password
        )),
        content_type='application/json'
    )

def req_user_login(test_case, username, password):
    return test_case.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json'
    )

def req_user_status(test_case, data):
    return test_case.client.get(
        '/api/auth/status',
        headers=dict(
            Authorization='Bearer ' + json.loads(data.decode())['auth_token']
        )
    )
