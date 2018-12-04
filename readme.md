# Сайт харьковского областного союза ЕХБ

Сайт работает под CMS Django.
https://ecb.kh.ua/

### Подготовка к работе:

1. Загрузить и установить Python 3.6.6: https://www.python.org/downloads/release/python-366/
2. Загрузить [файл get-pip.py](https://bootstrap.pypa.io/get-pip.py)
3. В папке с get-pip.py запустить команду: python get-pip.py
4. Необходимо форкнуть проект и загрузить себе на локальную машину: git clone git@github.com:[login]/[project_name].git [dir_to_clone]
5. В папке проекта запустить команду: pip install pipenv npm (pipenv - утилита для создания виртуального окружения и управления .py пакетами; npm - для управления .js пакетами)
6. Затем: pipenv shell --three (создает виртуальное окружение)
7. Установить все зависимые .py пакеты: pipenv install
8. Установить все зависимые .js пакеты: npm install

### Для запуска проекта:

1. Сначала инициализируем виртуальное окружение: pipenv shell
2. В папке с manage.py запускаем команду: fab runserver
3. Для работы с css и js в отдельной консоли нужно инициализировать gulp командой: gulp
