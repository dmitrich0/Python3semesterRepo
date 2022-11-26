import os
operation = input("")
if operation == 'Вакансии':
    os.system('table.py')
elif operation == 'Статистика':
    os.system('2.1.3.py')
else:
    print("Неверная команда, доступные команды 'Вакансии' и 'Статистика'")
