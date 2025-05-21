# UniDoc + MLflow: Интеллектуальная платформа документооборота

## Структура проекта

```
.
├── core/                # Основное Django-приложение
│   ├── models.py        # Модели данных
│   ├── views.py         # API, включая ML endpoint
│   ├── urls.py          # Маршруты
│   └── ...
├── unidoc/              # Django настройки
├── deploy/mlflow/       # MLflow + Postgres (Docker Compose)
│   ├── docker-compose.yml
│   └── Dockerfile
├── terraform/           # Инфраструктура Yandex Cloud (S3)
│   ├── modules/bucket/  # Модуль для создания S3 бакета
│   └── envs/dev/        # Конфигурация для dev окружения
├── unidoc/ml/           # ML-эксперименты (train.py)
├── requirements.txt     # Python-зависимости
└── .github/workflows/   # CI/CD pipeline
```

## Требования

- Python 3.11+
- Docker и Docker Compose
- Terraform 1.0+
- Yandex Cloud CLI (опционально)

## Настройка окружения

1. **Создайте `.env` файл в корне проекта:**
   ```env
   DB_NAME=mlflow
   DB_USER=mlflow
   DB_PASSWORD=changeme
   DB_HOST=localhost
   DB_PORT=5432
   AWS_ACCESS_KEY_ID=YOUR_YC_S3_KEY
   AWS_SECRET_ACCESS_KEY=YOUR_YC_S3_SECRET
   ```

2. **Настройте GitHub Secrets для CI/CD:**
   - `YC_KEY`: Yandex Cloud API ключ
   - `YC_S3_KEY`: Access key для Yandex Object Storage
   - `YC_S3_SECRET`: Secret key для Yandex Object Storage

## Развертывание инфраструктуры

1. **Инициализация Terraform:**
   ```bash
   cd terraform/envs/dev
   terraform init
   ```

2. **Применение конфигурации:**
   ```bash
   terraform apply
   ```

## Запуск MLflow

1. **Запуск MLflow и Postgres:**
   ```bash
   cd deploy/mlflow
   docker-compose up -d --build
   ```
   MLflow будет доступен на http://localhost:5001

## Разработка

1. **Установка зависимостей:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Миграции базы данных:**
   ```bash
   python manage.py migrate
   ```

3. **Генерация тестовых данных:**
   ```bash
   python manage.py shell -c "from core.management.commands.generate_test_data import Command; Command().handle()"
   ```

4. **Запуск обучения ML-модели:**
   ```bash
   PYTHONPATH=$(pwd) python unidoc/ml/train.py
   ```

## CI/CD Pipeline

Pipeline состоит из трех этапов:

1. **Infra**: Создание S3 бакета в Yandex Cloud
2. **Deploy**: Развертывание MLflow и Postgres
3. **Test ML**: Обучение и тестирование ML-модели

## MLflow в проекте

MLflow используется для:
- Отслеживания экспериментов с ML моделями
- Сохранения метрик и параметров моделей
- Хранения артефактов (моделей) в S3
- Предоставления UI для анализа результатов

## API Endpoints

- Swagger UI: `/api/`
- ReDoc: `/api/redoc/`
- ML Prediction: POST `/api/predict-document-class/`

## Безопасность

- Все секреты хранятся в GitHub Secrets
- Локальные секреты в `.env` (не коммитятся в git)
- Используется HTTPS в production
- JWT аутентификация для API

## Мониторинг и логирование

- MLflow UI для мониторинга ML экспериментов
- Django logging для приложения
- Terraform state в Yandex Cloud

## Дальнейшие улучшения

1. Добавление мониторинга через Prometheus/Grafana
2. Интеграция с BERT/transformers для улучшения классификации
3. Автоматическое масштабирование MLflow
4. Добавление тестов для ML компонентов

---
**Вопросы, доработки, интеграция с BERT/transformers — пишите!**

