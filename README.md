<h1 align="center">Проект на FastAPI с использованием PostgreSQL в качестве базы данных</h1> 
<p align="center">
<img src="https://img.shields.io/badge/python-3.10-blue?logo=python">
<img src="https://img.shields.io/badge/fastapi-v0.100.0-green?logo=fastapi">
<img src="https://img.shields.io/badge/PostgreSQL-blue?logo=PostgreSQL&logoColor=white">
</p>

***
В проекте реализован REST API по работе с меню ресторана.<br>
Даны 3 сущности: Меню, Подменю, Блюдо.

### Запуск приложения
Клонировать репозиторий:
```commandline
gh repo clone https://github.com/amoglock/Menu_management
```
Для запуска приложения в командной строке ввести:
```commandline
docker compose up
```
После запуска, документация Swagger доступна по адресу: http://0.0.0.0:8000/docs#/
![](https://github.com/amoglock/images/blob/main/menu_management_swagger.png?raw=true)
***
#### Зависимости
* У меню есть подменю, которые к ней привязаны.
* У подменю есть блюда.


#### Условия
* Блюдо не может быть привязано напрямую к меню, минуя подменю.
* Блюдо не может находиться в 2-х подменю одновременно.
* Подменю не может находиться в 2-х меню одновременно.
* Если удалить меню, удаляются все подменю и блюда этого меню.
* Если удалить подменю, удадяются все блюда этого подменю.
* Цены блюд выводятся с округлением до 2 знаков после запятой.
* Во время выдачи списка меню, для каждого меню добавляется кол-во подменю и блюд в этом меню.
* Во время выдачи списка подменю, для каждого подменю добавляется кол-во блюд в этом подменю.
