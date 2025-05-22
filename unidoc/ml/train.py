import os
import mlflow
import joblib
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from core.models import DocumentVersion
from joblib import Parallel, delayed
import torch
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm

# Создаем директорию для кэша
CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

def load_pretrained_model():
    """Загружает предобученную модель BERT"""
    model_name = "cointegrated/rubert-tiny2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return model, tokenizer

def get_bert_embeddings(texts, model, tokenizer, batch_size=32):
    """Получает эмбеддинги текстов с помощью BERT"""
    embeddings = []
    for i in tqdm(range(0, len(texts), batch_size)):
        batch = texts[i:i + batch_size]
        encoded = tokenizer(batch, padding=True, truncation=True, return_tensors='pt')
        with torch.no_grad():
            outputs = model(**encoded)
            embeddings.append(outputs.last_hidden_state.mean(dim=1).numpy())
    return np.vstack(embeddings)

def train_model_parallel(X, y, n_jobs=-1):
    """Параллельное обучение нескольких моделей"""
    def train_single_model(X_train, X_test, y_train, y_test, n_estimators):
        model = RandomForestClassifier(n_estimators=n_estimators, random_state=42, n_jobs=1)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        return model, accuracy

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Параллельное обучение моделей с разным количеством деревьев
    n_estimators_list = [50, 100, 200, 300]
    results = Parallel(n_jobs=n_jobs)(
        delayed(train_single_model)(X_train, X_test, y_train, y_test, n_est)
        for n_est in n_estimators_list
    )
    
    # Выбираем лучшую модель
    best_model, best_accuracy = max(results, key=lambda x: x[1])
    return best_model, best_accuracy

def load_data():
    """Загружает данные из DocumentVersion и формирует признаки и метки"""
    cache_file = CACHE_DIR / "data_cache.joblib"
    
    if cache_file.exists():
        print("Loading data from cache...")
        return joblib.load(cache_file)
    
    print("Loading data from database...")
    versions = DocumentVersion.objects.select_related('document').all()
    if not versions.exists():
        print("В базе нет версий документов. Сгенерируйте тестовые данные!")
        return None, None
    
    texts = []
    labels = []
    for v in versions:
        texts.append(v.content)
        labels.append(v.document.project.id if v.document and v.document.project else 0)
    
    # Получаем BERT эмбеддинги
    print("Loading pretrained BERT model...")
    model, tokenizer = load_pretrained_model()
    print("Getting BERT embeddings...")
    X = get_bert_embeddings(texts, model, tokenizer)
    y = np.array(labels)
    
    data = (X, y)
    joblib.dump(data, cache_file)
    return data

if __name__ == "__main__":
    # Настройка MLflow
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5001"))
    mlflow.set_experiment("unidoc-document-tfidf-classification")

    # Загрузка данных
    X, y = load_data()
    if X is None or y is None:
        print("Нет данных для обучения. Завершение работы.")
        exit(1)

    # Тренировка модели и логирование в MLflow
    with mlflow.start_run():
        model, accuracy = train_model_parallel(X, y)
        mlflow.log_param("model_type", "RandomForest")
        mlflow.log_param("feature_type", "BERT")
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(model, "model")
        print(f"Точность модели: {accuracy:.3f}")
        print("Эксперимент успешно залогирован в MLflow!") 