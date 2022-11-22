# Бот для уведомлений о проверка работ на [DVMN](https://dvmn.org/)
 Это бот, который взаимодействует с API DVMN](https://dvmn.org/) и отправляет вам сообщение о проверенных работах.
 
 ## Как установить 
 Во-первых, вам неоходимо скачать этот репозиторий. Для этого нажмите зелёную кнопку ```Code``` в правом верхнем углу и выберите удобный для вас метод скачивания.
 
 
![222](https://user-images.githubusercontent.com/83189636/203256004-5cc0e83e-36e8-4e0d-b6e7-86a8b81aef39.gif)

Во-вторых, создайте ```.env``` файл в папке проекта, в него нужно записать следующее:
**DVMN_AUTHORIZATION_TOKEN**. Для получения токена необходимо перейти на сайт [DVMN](https://dvmn.org/) и зарегистрироваться, далее нужно перейти в [документацию к API](https://dvmn.org/api/docs/), там же вы и увидите необходимый токен для авторизации. Записать его в ```.env``` файл необходимо в следующем формате.
```python
DVMN_AUTHORIZATION_TOKEN = 'Ваш токен авторизации'
```

**TG_BOT_API_KEY**. Далее необходимо создать телеграм бота в [BotFather](https://telegram.me/BotFather) и получать API-ключ бота. Для этого папаше ботов нужно прописать команду ```/newbot ``` и придумать боту название и логин, заканчивающийся на bot. Записать его в ```.env``` аналогичным образом.
```python
TG_BOT_API_KEY = 'Ваш API-ключ'
```

**CHAT_ID**. Для получения вашего chat id нужно перейти [@userinfobot](https://telegram.me/userinfobot), достатоточно просто запустить его и он сразу же отправит вам всё необходимое. Его нужно также записать в ```.env``` файл.
```python
CHAT_ID = 'Ваш chat id'
```
В проекте используется пакет [environs](https://pypi.org/project/environs/). Он позволяет загружать переменные окружения из файла ```.env``` в корневом каталоге приложения.
Этот ```.env``` файл можно использовать для всех переменных конфигурации.
Ну и естественно Python3 должен быть уже установлен. Затем используйте pip (или pip3,если есть конфликт с Python2) для установки зависимостей:
```python
pip install -r requirements.txt
```

## Как пользоваться 
Достаточно просто запустить бота. Когда преподаватель проверит работу, то вам прийдёт уведомление о том принял ли он работу, или же нет.

## Пример работы
                                      
