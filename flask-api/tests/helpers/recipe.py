import json

def req_recipe_details(test_case, recipe_id):
    return test_case.client.get(
        'api/recipe/{}'.format(recipe_id),
        content_type='application/json'
    )

def req_search_recipe(test_case, data, query=''):
    if query:
        query = '?query=' + query.replace(' ', '+')

    return test_case.client.get(
        '/api/recipe/search' + query,
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        )
    )
