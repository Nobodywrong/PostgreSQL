# Install ODBC_PostgreSQL on Ubuntu 20.04 for ZABBIX

## Установка пакетов, необходимых для компиляции и создания двоичных файлов
```
sudo apt install build-essential
```

Загрузка последней стабильной версии ODBC

Последнюю версию берем отсюда http://www.unixodbc.org/download.html
```
wget ftp://ftp.unixodbc.org/pub/unixODBC/unixODBC-'version'.tar.gz
```

Распаковываем архив
```
tar xvzf unixODBC-2.3.9.tar.gz
```

Переход в созданную папку
```
cd unixODBC-'version'/
```

И оттуда начинаем настройку пакетов
```
./configure --prefix=/usr/local/unixODBC
```

Компилируем
```
make
```

После установки его в ситсему, запускаем
```
sudo make install
```

Проверяем установку
```
cd /usr/local/unixODBC/bin
ls
```

## Устанавливаем драйвер
```
apt-get install odbc-postgresql
```

Проверяем размещение файлов
``` 
odbcinst -j
```

odbcinst.ini используется для перечисления установленных драйверов баз данных ODBC

odbc.ini используется для определения источников данных
```
[TEST_PSQL]
Description = PostgreSQL database 
Driver  = /usr/lib/x86_64-linux-gnu/odbc/psqlodbca.so
Setup   = /usr/lib/x86_64-linux-gnu/odbc/libodbcpsqlS.so
Username = 
Password = 
Servername = 
Database = 
Port = 
Protocol = 7.4
```

Тест проверки соединения
```
isql TEST_PSQL

+---------------------------------------+
| Connected!                            |
|                                       |
| sql-statement                         |
| help [tablename]                      |
| quit                                  |
|                                       |
+---------------------------------------+
SQL>
```




