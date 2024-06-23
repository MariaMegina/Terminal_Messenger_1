# Terminal Messenger

## Постановка решаемой задачи:
Разработка терминального мессенджера с поддержкой множества чатов
ограниченного доступа с сохранием истории и избранных сообщений

## Предпологаемые инструменты решения:
#### shlex
#### asyncio
#### python_cowsay
#### art

## Макет интерфейса:
### При запуске мессенджера доступны команды:
#### show_chatlist
показывает список доступных клиенту чатов
#### open_chat <название чата>
открывает чат с заданным названием
#### create_chat <название чата>
создает новый чат с заданным названием
#### update_chat <название чата> <параметры редактирования>
Редактирует параметры чата с заданным названием
#### add_to_chat <имя пользователя> <название чата>
Добавляет пользователя в чат с заданным названием, если у вас есть на это права
#### quit_chat <название чата>
выход из чата, оставляет чат без доступа у клиента
#### delete_chat <название чата>
удаляет чат
#### info_chat <название чата>
показывает информацию о чате(количество и имена участников)

### При входе в чат доступны команды:
#### send <сообщение>
отправка сообщения 
#### send <сообщение> -m cowsay <имя коровы>
отправка сообщения в стиле заданной коровы
#### send <сообщение> -m art
отправка сообщения в стиле art
#### add_to_favourites <идентификатор сообщения>
добавления сообщения с заданным идентификатором в избранное
#### reply <идентификатор сообщения> <сообщение>
ответ на сообщение с заданным идентификатором 
#### exit
выход из чата
