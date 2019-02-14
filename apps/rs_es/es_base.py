import json
import re
import logging

from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk
from apps.rs_es.es_settings import (
    ELASTIC_HOST,
    ELASTIC_AUTH,
    RS_INDEX_NAME
)

logger = logging.getLogger('rs_es')

# server connect
connections = connections.create_connection(
    hosts=ELASTIC_HOST,
    http_auth=ELASTIC_AUTH
)


class EsBase(object):
    """
    es可以共用的函数
    """

    time_zone = "Asia/Shanghai"
    rs_index_name = RS_INDEX_NAME

    @classmethod
    def get_connections(cls):
        return connections

    @staticmethod
    def snake_case(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @classmethod
    def debug_output(cls, string):
        """
        输出测试
        :param string: search object
        :return:
        """
        print(string)
        print('*' * 30)

    @classmethod
    def debug_es(cls, search_obj):
        """
        输出es测试
        :param search_obj:
        :return:
        """
        es_sql = json.dumps(search_obj.to_dict())
        cls.debug_output(es_sql)

    @classmethod
    def save_data(cls, data, es_id=None):
        """
        保存数据
        :param data:
        :return:
        """
        es = connections.get_connection()
        params = {
            'index': cls.rs_index_name,
            'doc_type': cls.snake_case(cls.__name__),
            'refresh': True
        }

        if es_id:
            params['id'] = es_id
            params['body'] = {"doc": data}
            es.update(**params)
        else:
            params['body'] = data
            es.index(**params)

    @classmethod
    def bulk_op_data(cls, user_data_list, op=None):
        """
        支持批量插入用户数据到ES库
        :param user_data_list: user ES结构列表
        :return:
        """
        ACCEPT_OP = ['update']
        # 如果存在op但是op不在可选项里面，则报错
        if op and op not in ACCEPT_OP:
            raise ValueError('op的取值有误')

        if not isinstance(user_data_list, (list,)):
            raise ValueError('user_data_list数据结构为列表')

        # es配置信息
        es = connections.get_connection()
        index_name = cls._doc_type.index
        doc_type_name = cls.snake_case(cls.__name__)

        def gen_user_data():
            for dt in user_data_list:
                user_id = dt.get('id')
                if not user_id:
                    continue

                # es基础信息
                json_dt = {
                    '_index': index_name,
                    '_type': doc_type_name,
                    '_id': user_id
                }

                # 不存在op，就是插入新数据
                if not op:
                    json_dt['_source'] = dt
                # 存在op，则更新数据
                else:
                    json_dt['_op_type'] = op

                    # 只更新除了user_id之外的所有数据
                    dt.pop('user_id')
                    json_dt['doc'] = dt

                yield json_dt

        try:
            res = bulk(es, gen_user_data())
            logger.info(res)
        except Exception as e:
            logger.error(e)
