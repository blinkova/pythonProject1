import allure  # Импортируем библиотеки
import requests
from requests.exceptions import HTTPError
import pytest
import xml.etree.ElementTree as ElTree
import logging
from allure_commons.types import AttachmentType

# Парсинг mxl
tree = ElTree.parse('in.xml')  # Для парсинга берем файл in.xml
root = tree.getroot()  # Выделяем корневой узел
child = list(root)  # Выводим список из дочерних узлов
place = child[0]  # Берем первый элеиент из списка дочерних узлов
geo = child[1]  # Берем второй элемент из списка дочерних узлов
place_n = [[place[0][0].text, place[0][1].text, place[0][2].text],  # Выводим содержимое тегов узла в виде текста
           [place[1][0].text, place[1][1].text, place[1][2].text],  # Формируем входные данные - список из списков
           [place[2][0].text, place[2][1].text, place[2][2].text],
           [place[3][0].text, place[3][1].text, place[3][2].text],
           [place[4][0].text, place[4][1].text, place[4][2].text],
           [place[5][0].text, place[5][1].text, place[5][2].text],
           [place[6][0].text, place[6][1].text, place[6][2].text]]
geo_n = [[geo[0][0].text, geo[0][1].text, geo[0][2].text],  # Выводим содержимое тегов узла в виде текста
         [geo[1][0].text, geo[1][1].text, geo[1][2].text],  # Формируем массив входных данных - список из списков
         [geo[2][0].text, geo[2][1].text, geo[2][2].text],
         [geo[3][0].text, geo[3][1].text, geo[3][2].text],
         [geo[4][0].text, geo[4][1].text, geo[4][2].text],
         [geo[5][0].text, geo[5][1].text, geo[5][2].text],
         [geo[6][0].text, geo[6][1].text, geo[6][2].text]]


# Простая фикстура, которая только выводит тескт
@pytest.fixture
def fixture_info():  # Создаем фикстуру fixture_info
    with allure.step('Начало теста'):  # Текст до начала теста
        pass
    yield
    with allure.step('Конец теста'):  # Текст после завершения теста
        pass


# Класс отправки запроса и получения ответа
class TestUrl:  # Создаем класс TestUrl
    def __init__(self, search):
        self.search = search  # Задаем параметры поиска

    def status(self):  # Создаем метод status
        try:  # Пробуем отправить запрос с заданными параметрами поиска
            response = requests.get('https://nominatim.openstreetmap.org/' + self.search + '&format=json')
            # Если на запрос получаем ошибку, то выводим ее
        except HTTPError as http_err:  # Для ошибки http выводим ее
            logging.exception(f'Произошла ошибка HTTP: {http_err}')
            raise HTTPError(f'Произошла ошибка HTTP: {http_err}')
        except Exception as err:  # Для другой ошибки выводим ее
            logging.exception(f'Произошла ошибка: {err}')
            raise Exception(f'Произошла ошибка: {err}')
        else:
            logging.info('HTTP-соединение успешно установлено')
            data = response.json()  # Получаем ответ на запрос в формате json, как словарь
            logging.info(f"Получены данные следующего содержания: {data}")
            return data  # Возвращаем полученное значение


# Получение адреса по координатам
@pytest.mark.usefixtures('fixture_info')  # Применяем фикстуру для теста
@allure.story('test_search_by_coordinates')
@pytest.mark.parametrize('param', geo_n)  # В качестве параметров будет перебираться массив входных данных geo_n
def test_search_by_coordinates(param):
    latitude = param[0]  # В качестве широты устанавливаем первый элемент списка
    longitude = param[1]  # В качестве долготы устанавливаем второй элемент списка
    address = param[2]      # В качестве эталонного значения адреса устанавливаем третий элемент списка
    logging.info(f"Получить адрес по координатам: широта - {latitude}  долгота - {longitude}."
                 f" Адрес должен соответствовать -  {address}")
    url = TestUrl('reverse?lat=' + latitude + '&lon=' + longitude)  # Передаем параметры поиска для класса TestUrl
    data = url.status()  # Применяем метод status для класса TestUrl и забираем полученные данные (в виде словаря)
    with allure.step('Получены данные по координатам'):
        allure.attach(str(data), name='data', attachment_type=AttachmentType.TEXT)
        try:  # Пробуем применить поиск по ключу для словаря
            display_name = (data['display_name'])  # В словаре забирем значение для ключа display_name
            logging.info(f"Получен следующий адрес: {display_name}")
        except KeyError:  # В случае отсутсвия данного ключа в словаре, выводим ошибку
            logging.exception(f"Exception occurred: Невозможно получить адрес по координатам")
            raise AttributeError('Невозможно получить адрес по координатам')
        else:  # если данные упешно получены проверяем на равенство полученных и эталонных данных
            assert display_name == address, 'Полученный адрес не соответствует эталонным данным'
            logging.info("Passed: адрес соответствует ожидаемому")


# Получение координат по адресу
@pytest.mark.usefixtures('fixture_info')  # Применяем фикстуру для теста
@allure.story('test_search_by_address')
@pytest.mark.parametrize('param', place_n)  # В качестве параметров будет перебираться массив входных данных place_n
def test_search_by_address(param):
    address = param[0]  # В качестве адреса устанавливаем первый элемент списка
    latitude = param[1]  # В качестве эталонного широты устанавливаем второй элемент списка
    longitude = param[2]  # В качестве эталонного значения долготы устанавливаем третий элемент списка
    logging.info(f"Получить координаты по адресу - {address}. Координаты должны соответствовать: широта - {latitude},"
                 f" долгота -  {longitude}")
    url = TestUrl('search?q=' + address)  # Передаем параметры поиска для класса TestUrl
    data = url.status()  # Применяем метод status для класса TestUrl и забираем данные (в виде списка словарей)
    with allure.step('Получены данные по координатам'):
        allure.attach(str(data), name='data', attachment_type=AttachmentType.TEXT)
    s = 0  # Задаем значение счетчика совпадений по координатам
    for geo_dict in data:  # Вводим переменную geo_dict, которая перебирает словари в списке data
        lat = (geo_dict['lat'])  # В словаре выполняем поиск по ключу lat и записываем результат в переменную lat
        lon = (geo_dict['lon'])  # В словаре выполняем поиск по ключу lon и записываем результат в переменную lon
        logging.info(f"Получены следующие координаты: широта - {lat}, долгота - {lon}")
        if lat == latitude and lon == longitude:  # Проверяем равенство полученных значений эталонным
            s = 1  # Если координаты верны, то увеличиваем счетчик совпадений координат на 1
            logging.info("Найдено совпадение полученных и эталонных координат")
            break  # И выходим из цикла
        else:
            logging.info("Координаты не соответствуют ожидаемым")
    assert s == 1, 'Совпадений не выявлено. Полученные координаты не соответствуют эталонным данным'
    # Проверяем найдено ли совпадение по координатам
    logging.info("Passed: Координаты соответствуют ожидаемым")
