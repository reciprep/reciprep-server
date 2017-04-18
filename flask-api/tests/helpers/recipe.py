import json

def req_recipe_details(test_case, recipe_id):
    return test_case.client.get(
        'api/recipe/{}'.format(recipe_id),
        content_type='application/json'
    )
