from user_search.celery import app as celery_app
from apps.rs_es.user.es_model import EsUser


@celery_app.task(bind=True)
def insert_user_es(self, user_dict):
    """
    使用异步任务执行ES插入
    :param user_dict:
    :return:
    """
    EsUser.save_data(user_dict)
