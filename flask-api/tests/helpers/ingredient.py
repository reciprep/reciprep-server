import json

def req_add_ingredient_to_pantry(test_case, ingredient_to_value, data):

    '''
    Accepts paramaters:
        - test_case class
        - ingredient_to_value - list of JSON objects with ingredient names and values
        - data - contains user auth token

    Returns JSON containing header and ingredient data

    '''
    return test_case.client.patch(
        '/api/user/pantry',
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        ),
        data=json.dumps(dict(
            ingredients=[{'ingredient_name': i, 'value': ingredient_to_value[i]} for i in ingredient_to_value]
        )),
        content_type='application/json'
    )

def get_ingredients_from_pantry(test_case, data):

    '''
    Accepts parameters:
        - test_case class
        - data - contains user auth token

    Returnds JSON containing header 
    '''

    return test_case.client.get(
        '/api/user/pantry',
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        ),
        content_type='application/json'
    )
