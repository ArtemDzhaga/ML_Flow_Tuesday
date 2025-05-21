import os
# Инициализация Django для standalone-скрипта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unidoc.settings")
import django
django.setup()

import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from core.models import DocumentVersion


def load_data():
    """
    Загружает данные из DocumentVersion и формирует признаки и метки.
    Признак: длина текста версии.
    Метка: 0 — короткий текст, 1 — длинный (порог — медиана).
    """
    versions = DocumentVersion.objects.all()
    if not versions.exists():
        print("В базе нет версий документов. Сгенерируйте тестовые данные!")
        return None, None
    X = []  # Признаки
    y = []  # Метки
    lengths = [len(v.content) for v in versions]
    median_len = np.median(lengths)
    for v in versions:
        X.append([len(v.content)])
        y.append(1 if len(v.content) > median_len else 0)
    return np.array(X), np.array(y)

def train_model(X, y):
    """
    Тренирует модель классификации и возвращает её и accuracy на тесте.
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, accuracy

if __name__ == "__main__":
    # Настройка MLflow
    mlflow.set_tracking_uri("http://localhost:5001")
    mlflow.set_experiment("unidoc-document-classification")

    # Загрузка данных
    X, y = load_data()
    if X is None or y is None:
        print("Нет данных для обучения. Завершение работы.")
        exit(1)

    # Тренировка модели и логирование в MLflow
    with mlflow.start_run():
        model, accuracy = train_model(X, y)
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")
        print(f"Точность модели: {accuracy:.3f}")
        print("Эксперимент успешно залогирован в MLflow!") 