[app]
# Название вашего приложения
title = Calculator

# Имя главного файла (обратите внимание, мы указываем путь внутрь папки)
# Если сборщик всё равно не найдет файл, лучше переименуйте calculator.py в main.py
# Но если хотите оставить как есть, укажите так:
source.dir = calc
source.include_exts = py,png,jpg,kv,atlas

# Требования для работы вашей БД
requirements = python3,kivy,sqlite3

# Ориентация экрана
orientation = portrait

# Иконка (если она лежит в calc/pics/icon.png)
icon.filename = %(source.dir)s/pics/icon.png
