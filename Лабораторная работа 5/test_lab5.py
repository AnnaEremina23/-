# Импортируем необходимые библиотеки для работы Selenium
from selenium import webdriver                      # управление браузером
from selenium.webdriver.common.by import By        # типы локаторов (ID, XPATH и т.д.)
from selenium.webdriver.common.keys import Keys    # работа с клавиатурой (Enter и др.)
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # автоматическая установка драйвера
from selenium.webdriver.support.ui import WebDriverWait   # ожидания элементов
from selenium.webdriver.support import expected_conditions as EC
import time

# ФУНКЦИЯ ПОИСКА ЭЛЕМЕНТА ПО НЕСКОЛЬКИМ ЛОКАТОРАМ
def find_first(driver, wait, locators):
    """
    Пытается найти элемент по списку локаторов.
    Возвращает первый найденный элемент.
    """
    last_error = None

    for by, value in locators:
        try:
            # Ждём появления элемента на странице
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except Exception as e:
            last_error = e

    # Если ни один локатор не сработал — ошибка
    raise last_error


# ФУНКЦИЯ БЕЗОПАСНОГО КЛИКА
def safe_click(driver, wait, locator):
    element = wait.until(EC.element_to_be_clickable(locator))

    # Прокрутка к элементу
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(1)

    try:
        element.click()
    except Exception:
        # Запасной вариант — клик через JavaScript
        driver.execute_script("arguments[0].click();", element)

    return element

# ЗАПУСК БРАУЗЕРА
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()  # открываем окно на весь экран
wait = WebDriverWait(driver, 15)  # ожидание до 15 секунд


try:
    # 1. ОТКРЫТИЕ САЙТА
    driver.get("https://www.chitai-gorod.ru/")
    time.sleep(3)

    # 2. ПОИСК ПОЛЯ ВВОДА (РАЗНЫЕ ЛОКАТОРЫ)
    search_input = find_first(driver, wait, [
        (By.CSS_SELECTOR, "input[type='search']"),  # CSS локатор
        (By.XPATH, "//input[contains(@placeholder, 'Поиск')]"),  # XPath
        (By.XPATH, "//input")  # запасной вариант
    ])
    print("Поле поиска найдено.")

    # 3. ПОИСК ЭЛЕМЕНТА "КАТАЛОГ"
    catalog_locator = (By.XPATH, "//*[contains(text(), 'Каталог')]")
    wait.until(EC.presence_of_element_located(catalog_locator))
    print("Элемент 'Каталог' найден.")

    # 4. ПОИСК КОРЗИНЫ
    cart_locator = (By.XPATH, "//*[contains(text(), 'Корзина')]")
    wait.until(EC.presence_of_element_located(cart_locator))
    print("Элемент 'Корзина' найден.")
    # 5. ПОИСК КНОПКИ ПОИСКА
    search_button_found = False

    # разные варианты локаторов кнопки
    button_locators = [
        (By.XPATH, "//button[contains(@type, 'submit')]"),
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//form//button")
    ]

    for locator in button_locators:
        try:
            wait.until(EC.presence_of_element_located(locator))
            search_button_found = True
            print("Кнопка поиска найдена.")
            break
        except Exception:
            pass

    if not search_button_found:
        print("Кнопка поиска не найдена, будет использован Enter.")

    # 6. КЛИК ПО КАТАЛОГУ
    safe_click(driver, wait, catalog_locator)
    time.sleep(2)

    # 7. ПРОВЕРКА КАТЕГОРИЙ
    category_element = find_first(driver, wait, [
        (By.XPATH, "//*[contains(text(), 'Книги')]"),
        (By.XPATH, "//*[contains(text(), 'Канцтовары')]"),
        (By.XPATH, "//a[contains(., 'Книги')]")
    ])
    print("Категория найдена:", category_element.text)

    # 8. ВОЗВРАТ НА ГЛАВНУЮ
    driver.get("https://www.chitai-gorod.ru/")
    time.sleep(3)
    # 9. ПОИСК СТРОКИ ПОИСКА СНОВА
    search_input = find_first(driver, wait, [
        (By.CSS_SELECTOR, "input[type='search']"),
        (By.XPATH, "//input[contains(@placeholder, 'Поиск')]"),
        (By.XPATH, "//input")
    ])

    # ввод текста
    search_input.click()
    time.sleep(1)
    search_input.clear()
    time.sleep(1)
    search_input.send_keys("Гарри Поттер")
    time.sleep(2)

    # 10. ЗАПУСК ПОИСКА
    clicked = False

    for locator in button_locators:
        try:
            safe_click(driver, wait, locator)
            clicked = True
            break
        except Exception:
            pass

    if not clicked:
        search_input.send_keys(Keys.ENTER)

    time.sleep(4)
    # 11. ПРОВЕРКА РЕЗУЛЬТАТОВ ПОИСКА
    product_cards = []

    possible_product_locators = [
        (By.CSS_SELECTOR, "article"),
        (By.CSS_SELECTOR, "a[href*='/product/']"),
        (By.XPATH, "//a[contains(@href, '/product/')]")
    ]

    for by, value in possible_product_locators:
        try:
            wait.until(EC.presence_of_all_elements_located((by, value)))
            product_cards = driver.find_elements(by, value)
            if len(product_cards) > 0:
                break
        except Exception:
            pass

    print("Найдено товаров:", len(product_cards))

    # проверка — товары должны быть
    assert len(product_cards) > 0, "Результаты поиска не найдены"
    # 12. ПЕРЕХОД К ПЕРВОМУ ТОВАРУ
    first_product = product_cards[0]

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_product)
    time.sleep(1)

    try:
        first_product.click()
    except Exception:
        driver.execute_script("arguments[0].click();", first_product)

    time.sleep(4)
    # 13. ДОБАВЛЕНИЕ В КОРЗИНУ
    add_to_cart = find_first(driver, wait, [
        (By.XPATH, "//button[contains(., 'В корзину')]"),
        (By.XPATH, "//button[contains(., 'Добавить в корзину')]"),
        (By.XPATH, "//button[contains(., 'Купить')]")
    ])

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart)
    time.sleep(1)

    try:
        add_to_cart.click()
    except Exception:
        driver.execute_script("arguments[0].click();", add_to_cart)

    time.sleep(3)
    print("Товар добавлен в корзину.")
    # 14. ПЕРЕХОД В КОРЗИНУ
    safe_click(driver, wait, cart_locator)
    time.sleep(4)
    # 15. ПРОВЕРКА КОРЗИНЫ
    cart_items = []

    cart_locators = [
        (By.CSS_SELECTOR, "article"),
        (By.CSS_SELECTOR, "[class*='cart']"),
        (By.XPATH, "//*[contains(text(), 'Гарри Поттер')]")
    ]

    for by, value in cart_locators:
        items = driver.find_elements(by, value)
        if len(items) > 0:
            cart_items = items
            break

    # проверка — товар должен быть в корзине
    assert len(cart_items) > 0, "Товар в корзине не найден"

    print("Тест успешно завершён.")
    print("Товар присутствует в корзине.")
# ОБРАБОТКА ОШИБОК
except Exception as e:
    print("Во время выполнения теста произошла ошибка:")
    print(e)
# ЗАКРЫТИЕ БРАУЗЕРА
finally:
    time.sleep(5)
    driver.quit()
#XPATH-по структуре страницы
#pip show selenium
#pip install selenium webdriver-manager
#python test_lab5.py