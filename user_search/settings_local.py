import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings = {
    "SITE_URL": "http://192.168.33.11:8888",
    "secret_key": "ZGGA#Mp4yL4w5CDu",
    "db": {
        "host": "192.168.33.11",
        "user": "root",
        "password": "123456",
        "database": "student_com",
        "port": 3306,
        "charset": "utf8"
    },
    "redis": {
        "host": "192.168.33.11"
    },
    "CELERY_SETTINGS": {
        'namespace': 'user_search',
        'broker_url': 'redis://192.168.33.11:6379/0',
        'result_backend': 'redis://192.168.33.11:6379/1'
    }
}
