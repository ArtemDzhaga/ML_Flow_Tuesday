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
│   ├── modules/bucket/
│   └── envs/dev/
├── unidoc/ml/           # ML-эксперименты (train.py)
├── requirements.txt     # Python-зависимости
└── .github/workflows/   # CI/CD pipeline
```

## Быстрый старт

1. **Создайте .env в корне:**
   ```
   DB_NAME=mlflow
   DB_USER=mlflow
   DB_PASSWORD=changeme
   DB_HOST=localhost
   DB_PORT=5432
   AWS_ACCESS_KEY_ID=... # ключ из Yandex Cloud
   AWS_SECRET_ACCESS_KEY=... # секрет из Yandex Cloud
   ```
2. **Запустите MLflow и Postgres:**
   ```bash
   cd deploy/mlflow
   docker-compose up -d --build
   ```
   MLflow будет доступен на http://localhost:5001
3. **Выполните миграции и сгенерируйте тестовые данные:**
   ```bash
   python manage.py migrate
   python manage.py shell -c "from core.management.commands.generate_test_data import Command; Command().handle()"
   ```
4. **Запустите обучение ML-модуля:**
   ```bash
   PYTHONPATH=$(pwd) python unidoc/ml/train.py
   ```
5. **Проверьте результаты в MLflow UI:**
   - http://localhost:5001
   - Эксперименты, параметры, метрики, модели

## Безопасность
- **Никогда не коммитьте ключи доступа в git!**
- Используйте `.env` и GitHub Secrets для хранения ключей.
- Если ключи были скомпрометированы — немедленно удалите их в Yandex Cloud и создайте новые.
- Очищайте историю git от секретов с помощью BFG Repo-Cleaner.

## MLflow: зачем он нужен?
- **Контроль версий экспериментов:** все параметры, метрики, модели и артефакты логируются автоматически.
- **Воспроизводимость:** любой эксперимент можно воспроизвести по сохранённым параметрам и данным.
- **Централизованное хранилище:** все модели и артефакты хранятся в S3, доступны для CI/CD и продакшн.
- **Интеграция с CI/CD:** при каждом пуше пайплайн автоматически запускает обучение и логирование в MLflow.
- **Удобный UI:** можно сравнивать эксперименты, отслеживать метрики, скачивать модели.

## ML/AI возможности
- Классификация документов по содержимому (TF-IDF, RandomForest)
- Логирование экспериментов, моделей и метрик в MLflow
- API для предсказаний: POST `/predict-document-class/` с полем `text`

## Пример запроса к API
```bash
curl -X POST http://localhost:8000/predict-document-class/ \
     -H 'Content-Type: application/json' \
     -d '{"text": "Пример текста документа для классификации"}'
```

## CI/CD
- Автоматически применяет Terraform (создаёт S3 в Yandex Cloud)
- Разворачивает MLflow + Postgres
- Запускает обучение ML-модуля

---
**Вопросы, доработки, интеграция с BERT/transformers — пишите!**

