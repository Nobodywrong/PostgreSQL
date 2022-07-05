#!/bin/bash

for ARGUMENT in "$@"
do
  KEY=$(echo $ARGUMENT | cut -f1 -d=)

  KEY_LENGTH=${#KEY}
  VALUE="${ARGUMENT:$KEY_LENGTH+1}"
  case "$KEY" in
    "H" | "host") host="$VALUE";;
    "U" | "user") user="$VALUE";;
    "P" | "password") password="$VALUE";;
    "PP" | "port") port="$VALUE";;
    "DD" | "database") database="$VALUE";;
    "NEW" | "new_database") new_database="$VALUE";;
  esac
done
#  -z   -  true если длина строки является 0
#  -n   -  true если длина строки НЕ является 0
if [[ -z $new_database ]] && [[ -z $database ]]; then  #Проверка передачи параметров имен БД
  echo "Error: not param"
  exit 255
fi

if [[ -n $new_database ]]; then  #Если передан параметр подключения к новой БД выплнение скрипта очистки + vacuum full
  echo "Connect to NEW database"
  python3 clear_db.py --host "$host" --user "$user" --pwd "$password" --port "$port" --database "$new_database"
  if [[ "$?" != 0 ]]; then   #Проверка статуса выхода последней команды
    echo "Vacuum New Datadase Error"
    exit 255
  fi
  psql postgresql://$user:$password@$host:$port/$new_database -c "vacuum full verbose analyze;"
fi

if [[ $database != "" ]]; then  #Если передан параметр подключения к старой БД выплнение скрипта очистки + vacuum full
  echo "Connect to OLD database"
  python3 clear_db_2.py --host $host --user $user --pwd $password --port $port --database $database
  if [[ "$?" != 0 ]]; then  #Проверка статуса выхода последней команды
    echo "Vacuum Old Datadase Error"
    exit 255
  fi
  psql postgresql://$user:$password@$host:$port/$database -c "vacuum full verbose analyze;"
fi