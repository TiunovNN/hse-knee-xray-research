# hse-knee-xray-research

Годовой проект студентов по ВШЭ по специальности "Машинное обучение высоконагруженных систем"

## Описание данных:

Набор данных состоит из 1655 цифровых рентгеновских изображений коленного сустава. Исходные изображения представляют собой 8-битные изображения в оттенках серого. Каждое рентгенологическое рентгеновское изображение коленного сустава вручную классифицировано в соответствии со специальными медицинскими оценками двумя экспертами на 5 классов. 

Эксперт I:

0- Normal (515 шт.)

1- Doubtful (478 шт.)

2- Mild (233 шт.)

3- Moderate (222 шт.)

4- Severe (207 шт.)


Эксперт II:

0- Normal (504 шт.) 

1- Doubtful (489 шт.)

2- Mild (233 шт.)

3- Moderate (222 шт.)

4- Severe (207 шт.)

Ссылка на данные: https://tnn-hse-medtech.storage.yandexcloud.net

## Модели

* ML-модель на основе HOG [ссылка](models/ML_hog)
* ML-модель на основе Autoencoder [ссылка](models/ML_autoencoder)


## Запуск работы проекта

Для начала необходимо прописать environments в [docker-compose.yaml](docker-compose.yaml): API_S3_ACCESS_KEY_ID, API_S3_BUCKET, API_S3_SECRET_ACCESS_KEY, BOT_TOKEN.

После чего для запуска проекта можно прописать `docker-compose -f ./docker-compose.yaml up`

## Иллюстрация работы

![](https://github.com/TiunovNN/hse-knee-xray-research/blob/master/Illustration_of_the_work.gif)
