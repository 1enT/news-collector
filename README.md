# News-collector

Проект создан для удобства поиска новостей на площадках и дальнейшей их отправки в телеграм-канал.
Программа собирает новости с определенных сайтови показывает их диспетчеру, который может отклонять/редактировать/отправлять предложенные новости.
В интерфейсе диспетчера пользователь также может создавать новости сам.

## Структура проекта
Проект состоит из нескольких частей:
- `news aggregator` собирает новости с сайтов tatar-inform.ru, rais.tatarstan.ru, а также с сайтов муниципалитетов и министерств Татарстана. Аггрегатор не только собирает новости, но еще и фильтрует их по ключевым словам.
- `server`. Тут лежат клиентское приложение и его API.
- `telegram bot server` позволяет мониторить забор новостей.
- `reload news script` очищает очередь ожидания новостей. Новости, отобранные аггрегатором попадают в очередь, которая видна пользователю, и в полночь все нерассмотренные новости очищаются.

## Запуск проекта
- ./ `pip install -r requirements.txt` установка зависимостей
- ./news aggregator/ `py main.py` запуск news aggregator

- ./server/react-flask-app/api `python -m venv venv` установка виртуального окружения
- ./server/react-flask-app/api `venv\Scripts\activate && pip install -r requirements.txt` установка зависимостей
- ./server/react-flask-app/api `run.py` запуск API клиента

- ./server/react-flask-app `npm install`
- ./server/react-flask-app `npm start` запуск клиента

Опционально:
- ./telegram bot server `py run.py` запуск тг-бота
- ./reload news script `py run.py` запуск очистителя