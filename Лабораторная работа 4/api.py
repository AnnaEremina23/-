import requests


class PetFriends:
    # Конструктор класса: задаём базовый URL сервиса
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru"


    # 1. Получение API-ключа пользователя
    def get_api_key(self, email: str, password: str):
        # Передаём email и пароль в заголовках запроса
        headers = {
            "email": email,
            "password": password
        }

        # Отправляем GET-запрос
        res = requests.get(f"{self.base_url}/api/key", headers=headers)

        # Получаем статус ответа
        status = res.status_code

        # Пытаемся преобразовать ответ в JSON
        try:
            result = res.json()
        except Exception:
            result = res.text

        # Возвращаем статус и результат
        return status, result


    # 2. Получение списка питомцев
    def get_list_of_pets(self, auth_key: str, filter_value: str = ""):
        # В заголовках передаём ключ авторизации
        headers = {
            "auth_key": auth_key
        }

        # Параметр filter:
        # "" — все питомцы
        # "my_pets" — только свои
        params = {
            "filter": filter_value
        }

        # Отправляем GET-запрос
        res = requests.get(f"{self.base_url}/api/pets", headers=headers, params=params)

        status = res.status_code

        try:
            result = res.json()
        except Exception:
            result = res.text

        return status, result


    # 3. Добавление нового питомца с фотографией
    def add_new_pet(self, auth_key: str, name: str, animal_type: str, age: str, pet_photo: str):
        # Заголовок с ключом авторизации
        headers = {
            "auth_key": auth_key
        }

        # Данные питомца 
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age
        }

        # Открываем файл изображения в бинарном режиме
        with open(pet_photo, "rb") as photo:
            files = {
                "pet_photo": photo
            }

            # Отправляем POST-запрос
            res = requests.post(
                f"{self.base_url}/api/pets",
                headers=headers,
                data=data,
                files=files
            )

        status = res.status_code

        try:
            result = res.json()
        except Exception:
            result = res.text

        return status, result


    # 4. Обновление информации о питомце
    def update_pet_info(self, auth_key: str, pet_id: str, name: str, animal_type: str, age: str):
        # Заголовок с ключом авторизации
        headers = {
            "auth_key": auth_key
        }

        # Новые данные питомца
        data = {
            "name": name,
            "animal_type": animal_type,
            "age": age
        }

        # Отправляем PUT-запрос (изменение данных)
        res = requests.put(
            f"{self.base_url}/api/pets/{pet_id}",
            headers=headers,
            data=data
        )

        status = res.status_code

        try:
            result = res.json()
        except Exception:
            result = res.text

        return status, result


    # 5. Удаление питомца
    def delete_pet(self, auth_key: str, pet_id: str):
        # Заголовок с ключом авторизации
        headers = {
            "auth_key": auth_key
        }

        # Отправляем DELETE-запрос
        res = requests.delete(
            f"{self.base_url}/api/pets/{pet_id}",
            headers=headers
        )

        status = res.status_code

        try:
            result = res.json()
        except Exception:
            result = res.text

        return status, result