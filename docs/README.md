# ML Flow Tuesday - Документация проекта

## Содержание
1. [Обзор проекта](#обзор-проекта)
2. [Архитектура](#архитектура)
3. [Установка и настройка](#установка-и-настройка)
4. [Разработка](#разработка)
5. [CI/CD Pipeline](#cicd-pipeline)
6. [ML Pipeline](#ml-pipeline)
7. [Мониторинг и логирование](#мониторинг-и-логирование)
8. [Безопасность](#безопасность)

## Обзор проекта

ML Flow Tuesday - это система для классификации документов с использованием машинного обучения. Проект использует MLflow для отслеживания экспериментов и управления моделями.

### Основные возможности
- Классификация документов по проектам
- Отслеживание версий документов
- Управление проектами и задачами
- REST API для интеграции
- MLflow для управления ML-моделями

## Архитектура

### Компоненты системы
1. **Django Backend**
   - REST API на Django REST Framework
   - PostgreSQL для хранения данных
   - JWT аутентификация

2. **ML Pipeline**
   - MLflow для отслеживания экспериментов
   - Scikit-learn для классификации
   - S3 для хранения артефактов

3. **Infrastructure**
   - Terraform для управления инфраструктурой
   - Yandex Cloud для хостинга
   - Docker для контейнеризации

### Схема развертывания
```
[GitHub Actions] -> [Terraform] -> [Yandex Cloud]
                              -> [S3 Bucket]
                              -> [MLflow Server]
                              -> [PostgreSQL]
```

## Установка и настройка

### Предварительные требования
- Python 3.11+
- Docker и Docker Compose
- Terraform
- Yandex Cloud CLI

### Локальная установка

1. **Клонирование репозитория**
   ```bash
   git clone https://github.com/your-username/ML_Flow_Tuesday.git
   cd ML_Flow_Tuesday
   ```

2. **Настройка переменных окружения**
   ```bash
   cp .env.example .env
   # Отредактируйте .env файл
   ```

3. **Запуск MLflow и PostgreSQL**
   ```bash
   cd deploy/mlflow
   docker-compose up -d
   ```

4. **Установка зависимостей**
   ```bash
   pip install -r requirements.txt
   ```

5. **Миграции базы данных**
   ```bash
   python manage.py migrate
   ```

6. **Генерация тестовых данных**
   ```bash
   python manage.py shell -c "from core.management.commands.generate_test_data import Command; Command().handle()"
   ```

## Разработка

### Структура проекта
```
ML_Flow_Tuesday/
├── core/                 # Основное приложение
├── unidoc/              # Настройки проекта
├── deploy/              # Конфигурации развертывания
├── terraform/           # Terraform манифесты
├── docs/                # Документация
└── tests/               # Тесты
```

### Запуск тестов
```bash
python manage.py test
```

### Локальное обучение модели
```bash
PYTHONPATH=$(pwd) python unidoc/ml/train.py
```

## CI/CD Pipeline

### Этапы пайплайна
1. **Infra**
   - Создание S3 бакета
   - Настройка прав доступа

2. **Deploy**
   - Установка Docker
   - Запуск MLflow и PostgreSQL
   - Проверка доступности сервисов

3. **Test**
   - Установка Python
   - Запуск тестов
   - Проверка качества кода

4. **ML Training**
   - Подготовка данных
   - Обучение модели
   - Сохранение результатов

### Переменные окружения
- `YC_KEY` - Yandex Cloud API ключ
- `YC_S3_KEY` - S3 Access Key
- `YC_S3_SECRET` - S3 Secret Key
- `YC_CLOUD_ID` - Yandex Cloud ID
- `YC_FOLDER_ID` - Yandex Cloud Folder ID

## ML Pipeline

### Компоненты ML Pipeline
1. **Подготовка данных**
   - Загрузка из PostgreSQL
   - Предобработка текста
   - Кэширование данных

2. **Обучение модели**
   - TF-IDF векторизация
   - RandomForest классификатор
   - Валидация модели

3. **MLflow интеграция**
   - Отслеживание экспериментов
   - Логирование метрик
   - Сохранение артефактов

### Использование MLflow
1. **Просмотр экспериментов**
   ```bash
   mlflow ui
   ```

2. **Загрузка модели**
   ```python
   import mlflow
   model = mlflow.sklearn.load_model("runs:/<run_id>/model")
   ```

## Мониторинг и логирование

### Метрики
- Точность классификации
- Время обучения
- Размер модели

### Логирование
- Django logging
- MLflow tracking
- GitHub Actions logs

## Безопасность

### Меры безопасности
1. **Аутентификация**
   - JWT токены
   - Сессии Django

2. **Данные**
   - Шифрование в S3
   - Безопасное хранение секретов

3. **Доступ**
   - RBAC в Yandex Cloud
   - Ограничение доступа к API

### Рекомендации
1. Регулярно обновлять зависимости
2. Использовать секреты для хранения ключей
3. Настроить мониторинг безопасности 