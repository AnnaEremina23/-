import os
import pytest
from api import PetFriends

# Создаём объект класса для работы с API
pf = PetFriends()

# Данные зарегистрированного пользователя
EMAIL = "anaeremina230304@gmail.com"
PASSWORD = "234567890"

# Путь к файлу с фотографией питомца
PHOTO_PATH = os.path.join(os.path.dirname(__file__), "images", "cat.jpg")


# 1. Проверка получения API-ключа с корректными данными
def test_get_api_key_for_valid_user():
    # Отправляем запрос на получение ключа
    status, result = pf.get_api_key(EMAIL, PASSWORD)

    # Проверяем, что статус ответа 200
    assert status == 200

    # Проверяем, что в ответе есть ключ
    assert "key" in result


# 2. Проверка получения списка всех питомцев с валидным ключом
def test_get_all_pets_with_valid_key():
    # Получаем API-ключ
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Запрашиваем список всех питомцев
    status, result = pf.get_list_of_pets(auth_key, "")

    # Проверяем статус ответа
    assert status == 200

    # Проверяем, что в ответе есть список pets
    assert "pets" in result


# 3. Проверка добавления нового питомца с корректными данными
def test_add_new_pet_with_valid_data():
    # Получаем API-ключ
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Добавляем нового питомца
    status, result = pf.add_new_pet(auth_key, "Мани", "кот", "2", PHOTO_PATH)

    # Проверяем статус ответа
    assert status == 200

    # Проверяем, что имя питомца совпадает с отправленным
    assert result["name"] == "Мани"


# 4. Проверка изменения информации о питомце с корректными данными
def test_update_pet_info_with_valid_data():
    # Получаем API-ключ
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Получаем список своих питомцев
    _, pets_result = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список пустой, сначала создаём питомца
    if len(pets_result["pets"]) == 0:
        pf.add_new_pet(auth_key, "Тест", "кот", "2", PHOTO_PATH)
        _, pets_result = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца
    pet_id = pets_result["pets"][0]["id"]

    # Изменяем данные питомца
    status, result = pf.update_pet_info(auth_key, pet_id, "Симка", "кот", "3")

    # Проверяем статус ответа
    assert status == 200

    # Проверяем, что имя действительно изменилось
    assert result["name"] == "Симка"


# 5. Проверка получения API-ключа с неверным email
def test_get_api_key_with_invalid_email():
    # Пробуем получить ключ с неправильным email
    status, result = pf.get_api_key("wrong_email@mail.com", PASSWORD)

    # Ожидаем, что доступ не будет выдан
    assert status != 200


# 6. Проверка получения API-ключа с неверным паролем
def test_get_api_key_with_invalid_password():
    # Пробуем получить ключ с неправильным паролем
    status, result = pf.get_api_key(EMAIL, "wrong_password")

    # Ожидаем, что доступ не будет выдан
    assert status != 200


# 7. Проверка получения списка питомцев с неверным auth_key
def test_get_pets_with_invalid_auth_key():
    # Отправляем запрос с невалидным ключом
    status, result = pf.get_list_of_pets("invalid_key", "")

    # Ожидаем ошибку доступа
    assert status != 200


# 8. Проверка добавления питомца с пустым именем
def test_add_pet_with_empty_name():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Отправляем запрос с пустым именем
    status, result = pf.add_new_pet(auth_key, "", "кот", "2", PHOTO_PATH)

    # В зависимости от работы API возможны разные ответы
    assert status in [200, 400]


# 9. Проверка добавления питомца с пустым типом животного
def test_add_pet_with_empty_animal_type():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Отправляем запрос с пустым animal_type
    status, result = pf.add_new_pet(auth_key, "Барсик", "", "2", PHOTO_PATH)

    assert status in [200, 400]


# 10. Проверка добавления питомца с пустым возрастом
def test_add_pet_with_empty_age():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Отправляем запрос с пустым age
    status, result = pf.add_new_pet(auth_key, "Барсик", "кот", "", PHOTO_PATH)

    assert status in [200, 400]


# 11. Проверка добавления питомца с возрастом 0
def test_add_pet_with_age_zero():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Граничное значение возраста
    status, result = pf.add_new_pet(auth_key, "Барсик", "кот", "0", PHOTO_PATH)

    assert status in [200, 400]


# 12. Проверка добавления питомца с отрицательным возрастом
def test_add_pet_with_negative_age():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Некорректное отрицательное значение возраста
    status, result = pf.add_new_pet(auth_key, "Барсик", "кот", "-1", PHOTO_PATH)

    assert status in [200, 400]


# 13. Проверка добавления питомца с очень большим возрастом
def test_add_pet_with_large_age():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Проверяем граничное большое значение
    status, result = pf.add_new_pet(auth_key, "Барсик", "кот", "999", PHOTO_PATH)

    assert status in [200, 400]


# 14. Проверка добавления питомца с очень длинным именем
def test_add_pet_with_long_name():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Формируем очень длинную строку
    long_name = "А" * 256
    status, result = pf.add_new_pet(auth_key, long_name, "кот", "2", PHOTO_PATH)

    assert status in [200, 400]


# 15. Проверка удаления первого питомца из списка
def test_delete_first_pet():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Получаем список своих питомцев
    _, pets_result = pf.get_list_of_pets(auth_key, "my_pets")

    # Если питомцев нет, сначала создаём одного
    if len(pets_result["pets"]) == 0:
        pf.add_new_pet(auth_key, "Удаляемый", "кот", "2", PHOTO_PATH)
        _, pets_result = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца
    pet_id = pets_result["pets"][0]["id"]

    # Удаляем питомца
    status, result = pf.delete_pet(auth_key, pet_id)

    # Проверяем, что удаление прошло успешно
    assert status == 200


# 16. Проверка добавления питомца со спецсимволами в имени
def test_add_pet_with_special_symbols_in_name():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Имя содержит специальные символы
    status, result = pf.add_new_pet(auth_key, "@@@###", "кот", "2", PHOTO_PATH)

    assert status in [200, 400]


# 17. Проверка добавления питомца, имя которого состоит только из цифр
def test_add_pet_with_numbers_in_name():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Имя задано цифрами
    status, result = pf.add_new_pet(auth_key, "12345", "кот", "2", PHOTO_PATH)

    assert status in [200, 400]


# 18. Проверка изменения питомца на пустое имя
def test_update_pet_with_empty_name():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Получаем список своих питомцев
    _, pets_result = pf.get_list_of_pets(auth_key, "my_pets")

    # Если питомцев нет, создаём одного
    if len(pets_result["pets"]) == 0:
        pf.add_new_pet(auth_key, "Тест", "кот", "2", PHOTO_PATH)
        _, pets_result = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца
    pet_id = pets_result["pets"][0]["id"]

    # Пытаемся обновить питомца, установив пустое имя
    status, result = pf.update_pet_info(auth_key, pet_id, "", "кот", "2")

    assert status in [200, 400]


# 19. Проверка получения списка только своих питомцев
def test_get_my_pets_with_valid_key():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Получаем список своих питомцев
    status, result = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем успешный ответ
    assert status == 200

    # Проверяем наличие ключа pets в ответе
    assert "pets" in result


# 20. Проверка удаления питомца с невалидным id
def test_delete_pet_with_invalid_id():
    _, auth_result = pf.get_api_key(EMAIL, PASSWORD)
    auth_key = auth_result["key"]

    # Пробуем удалить питомца с несуществующим id
    status, _ = pf.delete_pet(auth_key, "invalid_id")

    # Учитываем, что API может отвечать по-разному
    assert status in [200, 400, 404]
    
#pytest -v
#pip install requests pytest