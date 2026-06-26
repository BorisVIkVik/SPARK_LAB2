# Викторов Борис Лабораторная 6.

Работа посвящена pyspark и HDFS.

## Данные: OpenFoodFacts
https://huggingface.co/datasets/openfoodfacts/product-database

## Модель: KMeans

## Database/FileSystem: HDFS
Был взят как копия ветки docker репозитория https://github.com/apache/hadoop/tree/docker-hadoop-3

## Структура
```
.
├── config
├── data
├── hadoop
│   └── test.sh
└── src

```
Папки:

    config: Хранится yaml файл с конфигурацией pyspark.
    data: Хранится parquet с данными.
    src: Папка для кода модели.
    hadoop: Папка для кода hdfs с docker.
## Запуск
Вариант 1:

HDFS:

    docker compose -f ./hadoop/docker-compose.yaml --project-directory ./hadoop up -d
Когда HDFS загружен запускаем код для загрузки данных:

    python src/load.py
После запускаем Python скрипт:

    python src/main.py
    
Варинат 2:

    ./runapp.sh
