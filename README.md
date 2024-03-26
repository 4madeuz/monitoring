# monitoring
скрипт мониторинга процесса, который запускает заданный процесс (команда запуска должна передаваться в параметрах командной строки)

# Описание

Предположим, есть скрипт на Python с названием script.py.

python monitor_process.py "python my_script.py arg1 arg2" output.log --restart --timeout 60

Эта команда запустит процесс python my_script.py arg1 arg2, и его вывод будет записываться в файл output.log. Скрипт будет перезапускать процесс в случае его падения, и он также автоматически завершится через 60 секунд.

Альтернативно:

./monitor_process.sh "python my_script.py arg1 arg2" output.log --restart --timeout 60
