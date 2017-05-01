import json

def req_recipe_details(test_case, recipe_id):
    return test_case.client.get(
        'api/recipe/{}'.format(recipe_id),
        content_type='application/json'
    )

def req_search_recipe(test_case, data, query='', filter_=False):
    querystring = ''
    if query:
        querystring = '?terms=' + query.replace(' ', '+')

    if filter_:
        querystring += '&filter=true' if query else '?filter=true'

    return test_case.client.get(
        '/api/recipe/search' + querystring,
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        )
    )

def req_create_recipe(test_case, data, recipe_obj):
    return test_case.client.post(
        '/api/recipe',
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        ),
        data=json.dumps(recipe_obj),
        content_type='application/json'
    )

def req_prepare_recipe(test_case, data, recipe):
    return test_case.client.put(
        '/api/recipe/{}/prepare'.format(recipe.id),
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        ),
        content_length=0
    )

def req_rate_recipe(test_case, data, recipe, value):
    return test_case.client.put(
        '/api/recipe/{}/rate'.format(recipe.id),
        headers=dict(
            Authorization='Bearer ' + data['auth_token']
        ),
        data=json.dumps({'value': value}),
        content_type='application/json'
    )
