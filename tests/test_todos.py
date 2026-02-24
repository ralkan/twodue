def _get_and_assert_todo_3(client):
    """ Function to test single todo with id 3
    """
    response = client.get('/todos/3')
    assert response.status_code == 200

    assert 'content' in response.json

    assert response.json['content'] == 'Coffee'
    assert response.json['id'] == 3
    assert response.json['done'] == False


def test_list_todos(client, todos):
    response = client.get('/todos/')
    assert response.status_code == 200

    # Check if there's a "todos" key in the response
    assert 'todos' in response.json

    todos = response.json['todos']

    # Check if there are exactly 3 todo's
    assert len(todos) == 3

    # Check if all todo's have a "content" key
    assert all(['content' in t for t in todos])

    todo_contents = [t['content'] for t in todos]

    # Check if "Cheese" is one of the todos' contents
    assert 'Cheese' in todo_contents


def test_get_todo(client, todos):
    _get_and_assert_todo_3(client)


def test_create_todo(client, todos):
    response = client.get('/todos/')
    assert response.status_code == 200

    todos = response.json['todos']
    assert len(todos) == 3

    post_response = client.post('/todos/', json={'content': 'Bread', 'done': True})
    assert post_response.status_code == 201

    # Check if we get the todo back in the response
    assert 'content' in post_response.json
    # Check if we return the id of the new todo in the response
    assert 'id' in post_response.json
    # Check if the todo content is also correct
    assert post_response.json['content'] == 'Bread'
    # Check if the id has incremented as expected
    # (This might change or be removed when we use uuid's)
    assert post_response.json['id'] == 4

    response = client.get('/todos/')
    assert response.status_code == 200

    todos = response.json['todos']
    # The todo should be saved in the database which means there are 4 todo's now
    assert len(todos) == 4


def test_update_todo_content(client, todos):
    _get_and_assert_todo_3(client)

    # Only update "content"
    response = client.put('/todos/3', json={'content': 'Marshmallows'})
    assert response.status_code == 200

    assert 'content' in response.json

    # Make sure only "content" has been updated and nothing else
    assert response.json['content'] == 'Marshmallows'
    assert response.json['id'] == 3
    assert response.json['done'] == False


def test_update_todo_done(client, todos):
    _get_and_assert_todo_3(client)

    # Only update "done"
    response = client.put('/todos/3', json={'done': True})
    assert response.status_code == 200

    assert 'content' in response.json

    # Make sure only "done" has been updated and nothing else
    assert response.json['content'] == 'Coffee'
    assert response.json['id'] == 3
    assert response.json['done'] == True


# Negative flows

def test_cannot_update_todo_id(client, todos):
    _get_and_assert_todo_3(client)

    # Only update "id"
    response = client.put('/todos/3', json={'id': 888})
    assert response.status_code == 422
    assert 'errors' in response.json

    # Make sure nothing has changed and todo is still the same
    _get_and_assert_todo_3(client)


def test_cannot_update_todo_id_along_with_other_fields(client, todos):
    _get_and_assert_todo_3(client)

    # Try and update "id"
    response = client.put('/todos/3', json={'content': 'Marshmallow', 'id': 888})
    assert response.status_code == 422
    assert 'errors' in response.json

    # Make sure nothing has changed and todo is still the same
    _get_and_assert_todo_3(client)


def test_cannot_update_todo_empty(client, todos):
    _get_and_assert_todo_3(client)

    # Try and update with empty body
    response = client.put('/todos/3', json={})
    assert response.status_code == 422
    assert 'errors' in response.json

    # Make sure nothing has changed and todo is still the same
    _get_and_assert_todo_3(client)
