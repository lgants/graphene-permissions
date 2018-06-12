import pytest
from django.contrib.auth import get_user_model

from tests.utils import load_fixtures


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
    (None, None),
])
@pytest.mark.django_db
def test_mutation_django_model_required_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    mutation = """
    mutation{
        djangoModelAddPet(input: {race:"horse", name:"Alex", owner: "VXNlcjoz"}){
            status,
            pet{
                name,
                race,
            }
        }
    }
    """

    response = client.post(data=mutation, **test_kwargs)
    result = response.json()

    # get_user_model().objects.get(username='paul').user_permissions.add(19)
    if login in ('paul', 'tom'):
        # print(get_user_model().objects.get(username='paul').has_perms(['test_app.add_pet']))
        # print(get_user_model().objects.get(username='paul').user_permissions.all())
        assert result['data'] == {
            'djangoModelAddPet': {
                'pet': {
                    'name': 'Alex',
                    'race': 'horse'
                },
                'status': 201
            }
        }
    else:
        # print(get_user_model().objects.get(username='tom').has_perms(['test_app.add_pet']))
        # print(get_user_model().objects.get(username='tom').user_permissions.all())
        # print(get_user_model().objects.get(username='kate').has_perms(['test_app.add_pet']))
        # print(get_user_model().objects.get(username='kate').user_permissions.all())
        assert result['data'] == {
            'djangoModelAddPet': {
                'pet': None,
                'status': 403
            }
        }


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
    (None, None),
])
@pytest.mark.django_db
def test_mutation_superuser_required_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    mutation = """
    mutation{
        superuserAddPet(input: {race:"horse", name:"Alex", owner: "VXNlcjoz"}){
            status,
            pet{
                name,
                race,
            }
        }
    }
    """

    response = client.post(data=mutation, **test_kwargs)
    result = response.json()

    if login is 'tom':
        assert result['data'] == {
            'superuserAddPet': {
                'pet': {
                    'name': 'Alex',
                    'race': 'horse'
                },
                'status': 201
            }
        }
    else:
        assert result['data'] == {
            'superuserAddPet': {
                'pet': None,
                'status': 403
            }
        }


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
    (None, None),
])
@pytest.mark.django_db
def test_mutation_staff_required_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    mutation = """
    mutation{
        staffAddPet(input: {race:"horse", name:"Alex", owner: "VXNlcjoz"}){
            status,
            pet{
                name,
                race,
            }
        }
    }
    """

    response = client.post(data=mutation, **test_kwargs)
    result = response.json()

    if login is 'tom':
        assert result['data'] == {
            'staffAddPet': {
                'pet': {
                    'name': 'Alex',
                    'race': 'horse'
                },
                'status': 201
            }
        }
    else:
        assert result['data'] == {
            'staffAddPet': {
                'pet': None,
                'status': 403
            }
        }


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
    (None, None),
])
@pytest.mark.django_db
def test_mutation_allow_authenticated_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    mutation = """
    mutation{
        authenticatedAddPet(input: {race:"horse", name:"Alex", owner: "VXNlcjoz"}){
            status,
            pet{
                name,
                race,
            }
        }
    }
    """

    response = client.post(data=mutation, **test_kwargs)
    result = response.json()

    if login in ('tom', 'kate', 'paul'):
        assert result['data'] == {
            'authenticatedAddPet': {
                'pet': {
                    'name': 'Alex',
                    'race': 'horse'
                },
                'status': 201
            }
        }
    else:
        assert result['data'] == {
            'authenticatedAddPet': {
                'pet': None,
                'status': 403
            }
        }


@load_fixtures('tests/fixtures/test_fixture.yaml')
@pytest.mark.parametrize('login, password', [
    ('tom', 'testpassword'),
    ('kate', 'testpassword'),
    ('paul', 'testpassword'),
    (None, None),
])
@pytest.mark.django_db
def test_mutation_allow_any_permission(client, test_kwargs, login, password):
    client.login(username=login, password=password)

    mutation = """
    mutation{
        addPet(input: {race:"horse", name:"Alex", owner: "VXNlcjoz"}){
            status,
            pet{
                name,
                race,
            }
        }
    }
    """

    response = client.post(data=mutation, **test_kwargs)
    result = response.json()

    assert result['data'] == {
        'addPet': {
            'pet': {
                'name': 'Alex',
                'race': 'horse'
            },
            'status': 201
        }
    }
