import os

def get_config():
    return {
        "service_name": os.getenv("SERVICE_NAME", "undefined-service"),
        "environment": os.getenv("ENVIRONMENT", "dev"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "log_format": os.getenv("LOG_FORMAT", "json")
    }
