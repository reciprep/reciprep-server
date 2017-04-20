import json


def req_add_ingredient_to_pantry(test_case, ingredient_to_value, data):
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
    return test_case.client.get(
        '/api/user/pantry',
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        ),
        content_type='application/json'
    )

# def req_search_recipe(test_case, data, query=''):
#     if query:
#         query = '?query=' + query.replace(' ', '+')

#     return test_case.client.get(
#         '/api/recipe/search' + query,
#         headers=dict(
#             Authorization='Bearer ' + data['auth_token']
#         )
#     )