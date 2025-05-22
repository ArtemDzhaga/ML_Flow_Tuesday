bucket_name = "mlflowtuesday-artifacts"
region     = "ru-central1"
# s3_key и s3_secret должны задаваться через переменные окружения или secrets
zone       = "ru-central1-a"

labels = {
  environment = "dev"
  project     = "mlflow"
  managed_by  = "terraform"
} 