import os
operation = input("")
if operation == 'Вакансии':
    os.system('table.py')
elif operation == 'Статистика':
    os.system('statistics.py')
else:
    print("Неверная команда, доступные команды 'Вакансии' и 'Статистика'")
