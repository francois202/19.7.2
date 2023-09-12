import pytest
import os
import random
import string
from api import PetFriends
from settings import valid_email, valid_password


pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/0.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "СуперКот", "кот", "3", "images/0.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


'''8 tests'''


def test_successful_add_new_pet_simple(name='Мурзик_2', animal_type='Котэ_2', age=10):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_successful_add_photo_of_pet(pet_photo='images/0.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "СуперКот", "кот", "3", "images/0.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)

    assert status == 200


def test_invalid_user_get_api_key(filter=''):
    status, result = \
        pf.get_list_of_pets({'key': 'uoefhiuwheufhuiwehfhuew'},
                                         filter)

    assert status == 403


def test_invalid_auth_key_get_all_pets(email='123@gmail.com', password='123321'):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_add_new_pet_noname(animal_type='двортерьер',
                            age='4', pet_photo='images/0.jpg'):
    '''По документации непонятно, какой у нас должен быть фактический р-тат:
    Может ли создаваться питомец с пустым именем или нет'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, None, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == ''


def test_add_new_pet_long_name(animal_type='двортерьер', age='4', pet_photo='images/0.jpg'):
    '''По документации непонятно, какой у нас должен быть фактический р-тат:
    Может ли создаваться питомец с именем длиной >= 10000 символов'''

    name = ''.join(random.choices(string.ascii_letters + string.digits, k=10000))

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200


def test_get_all_pets_with_invalid_filter(filter='wefwef'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 500


def test_delete_nonexistent_pet_id():

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, _ = pf.delete_pet(auth_key, '3ceb67a8-faf0-4202-8f75-e06fa5b26832')

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
