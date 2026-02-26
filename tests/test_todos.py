# TODO: Test search functionality
# TODO: Test pagination
# TODO: Test sort/ordering

API_PREFIX = '/api/v2'


def _get_and_assert_todo_3(client):
    """ Function to test single todo with id 3
    """
    response = client.get(f'{API_PREFIX}/todos/3')
    assert response.status_code == 200

    assert 'content' in response.json

    assert response.json['content'] == 'Coffee'
    assert response.json['id'] == 3
    assert response.json['done'] == False


def test_list_todos(auth_client, user, todos):
    response = auth_client.get(f'{API_PREFIX}/todos/')
    assert response.status_code == 200

    # Check if there's a "todos" key in the response
    assert 'todos' in response.json
    assert 'total_records' in response.json
    assert 'total_pages' in response.json

    todos = response.json['todos']

    # Check if there are exactly 3 todo's
    assert response.json['total_records'] == 3

    # Check if all todo's have a "content" key
    assert all(['content' in t for t in todos])

    todo_contents = [t['content'] for t in todos]

    # Check if "Cheese" is one of the todos' contents
    assert 'Cheese' in todo_contents


def test_get_todo(auth_client, todos):
    _get_and_assert_todo_3(auth_client)


def test_create_todo(auth_client, todos):
    response = auth_client.get(f'{API_PREFIX}/todos/')
    assert response.status_code == 200

    todos_count = response.json['total_records']
    assert todos_count == 3

    post_response = auth_client.post(f'{API_PREFIX}/todos/', json={'content': 'Bread', 'done': True})
    assert post_response.status_code == 201

    # Check if we get the todo back in the response
    assert 'content' in post_response.json
    # Check if we return the id of the new todo in the response
    assert 'id' in post_response.json
    # Check if the todo content is also correct
    assert post_response.json['content'] == 'Bread'
    # Check if the id has incremented as expected
    # (This might change or be removed when we use uuid's)
    assert post_response.json['id'] == 5

    response = auth_client.get(f'{API_PREFIX}/todos/')
    assert response.status_code == 200

    todos_count = response.json['total_records']
    # The todo should be saved in the database which means there are 4 todo's now
    assert todos_count == 4


def test_update_todo_content(auth_client, todos):
    _get_and_assert_todo_3(auth_client)

    # Only update "content"
    response = auth_client.put(f'{API_PREFIX}/todos/3', json={'content': 'Marshmallows'})
    assert response.status_code == 200

    assert 'content' in response.json

    # Make sure only "content" has been updated and nothing else
    assert response.json['content'] == 'Marshmallows'
    assert response.json['id'] == 3
    assert response.json['done'] == False


def test_update_todo_done(auth_client, todos):
    _get_and_assert_todo_3(auth_client)

    # Only update "done"
    response = auth_client.put(f'{API_PREFIX}/todos/3', json={'done': True})
    assert response.status_code == 200

    assert 'content' in response.json

    # Make sure only "done" has been updated and nothing else
    assert response.json['content'] == 'Coffee'
    assert response.json['id'] == 3
    assert response.json['done'] == True


# Negative flows

def test_unauthorized_list_todos(client, todos):
    response = client.get(f'{API_PREFIX}/todos/')
    assert response.status_code == 401
    # Make sure we have a message in the json
    assert 'message' in response.json
    # Make sure we yap about the token to the user
    assert 'token' in response.json['message'].lower()


def test_unauthorized_create_todo(client, todos):
    response = client.post(f'{API_PREFIX}/todos/', json={'content': 'Bread', 'done': True})
    assert response.status_code == 401
    # Make sure we have a message in the json
    assert 'message' in response.json
    # Make sure we yap about the token to the user
    assert 'token' in response.json['message'].lower()


def test_unauthorized_show_todo(client, todos):
    response = client.get(f'{API_PREFIX}/todos/3')
    assert response.status_code == 401
    # Make sure we have a message in the json
    assert 'message' in response.json
    # Make sure we yap about the token to the user
    assert 'token' in response.json['message'].lower()


def test_cannot_update_todo_id(auth_client, todos):
    _get_and_assert_todo_3(auth_client)

    # Only update "id"
    response = auth_client.put(f'{API_PREFIX}/todos/3', json={'id': 888})
    assert response.status_code == 422
    assert 'errors' in response.json

    # Make sure nothing has changed and todo is still the same
    _get_and_assert_todo_3(auth_client)


def test_cannot_update_todo_id_along_with_other_fields(auth_client, todos):
    _get_and_assert_todo_3(auth_client)

    # Try and update "id"
    response = auth_client.put(f'{API_PREFIX}/todos/3', json={'content': 'Marshmallow', 'id': 888})
    assert response.status_code == 422
    assert 'errors' in response.json

    # Make sure nothing has changed and todo is still the same
    _get_and_assert_todo_3(auth_client)


def test_cannot_update_todo_empty(auth_client, todos):
    _get_and_assert_todo_3(auth_client)

    # Try and update with empty body
    response = auth_client.put(f'{API_PREFIX}/todos/3', json={})
    assert response.status_code == 422
    assert 'errors' in response.json

    # Make sure nothing has changed and todo is still the same
    _get_and_assert_todo_3(auth_client)
