from math import ceil
from elasticsearch_dsl import (
    DocType, Keyword, Q
)
from apps.rs_es.es_base import EsBase


class EsUser(EsBase, DocType):
    id = Keyword()

    # 搜索返回值最大允许值1000
    MAX_ALLOWED_QUESTION_DATA = 1000

    class Meta:
        index = EsBase.rs_index_name

    @staticmethod
    def es_response_format(dt):
        """
        按这个结构返回es数据
        :param dt:
        :return:
        """
        res = dt['_source']
        res['es_id'] = dt['_id']
        return res

    @classmethod
    def generate_search_query(cls, _query, _type, _key, _val, **kwargs):
        """
        生成ES搜索的query
        :param _query:
        :param _type:
        :param _key:
        :param _val:
        :param kwargs:
        :return:
        """
        if _type == 'match':
            search_string = {
                _key: _val
            }

            q_obj = Q('match', **search_string)
        elif _type == 'filter':
            search_string = {
                "filter": {
                    "term": {_key: _val}
                }
            }

            q_obj = Q('bool', **search_string)
        elif _type == 'rs_keyword':
            search_string = {
                "should": [
                    {
                        "match": {
                            "address": {
                                "query": _val,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "match": {
                            "description": {
                                "query": _val,
                                "operator": "and"
                            }
                        }
                    }
                ]
            }

            q_obj = Q('bool', **search_string)
        elif _type == 'rs_date':
            create_time_dict = {
                "lte": _val['end_time'],
                "format": "epoch_millis"
            }

            if _val['start_time']:
                create_time_dict['gte'] = _val['start_time']

            search_string = {
                "must": {
                    "range": {
                        "create_time": create_time_dict
                    }
                }
            }
            q_obj = Q('bool', **search_string)
        elif _type == 'wildcard':
            search_string = {
                "username": {
                    "value": '*{0}*'.format(_val)
                }
            }
            q_obj = Q('wildcard', **search_string)
        elif _type == 'copy_to':
            search_string = {
                "should": [
                    {
                        "match": {
                            "full_name": {
                                "query": _val,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "match": {
                            "first_name": {
                                "query": _val,
                                "operator": "and"
                            }
                        }
                    },
                    {
                        "match": {
                            "last_name": {
                                "query": _val,
                                "operator": "and"
                            }
                        }
                    }
                ]
            }

            q_obj = Q('bool', **search_string)
        elif _type == 'birthday':
            birth_dict = {
                "lte": _val['end_birth']
            }

            if _val['start_birth']:
                birth_dict['gte'] = _val['start_birth']
            search_string = {
                "must": {
                    "range": {
                        "birthday": birth_dict
                    }
                }
            }

            q_obj = Q('bool', **search_string)
        else:
            raise ('未找到符合的搜索类型')

        if _query:
            _query = _query & q_obj
        else:
            _query = q_obj
        return _query

    @classmethod
    def search_user(cls, **kwargs):
        """
        根据搜索条件搜索
        :param kwargs:
        :return:
        """
        # 可以带的数据
        order = kwargs.get('order')
        order = cls.validate_order(order)

        query_filter = kwargs.get('query_filter')
        page_size = kwargs.get('page_size', 10)

        max_page = int(ceil(cls.MAX_ALLOWED_QUESTION_DATA / page_size))
        page = int(kwargs.get('page', 1))
        if page > max_page:
            page = max_page

        if not query_filter:
            raise ('不存在任何的搜索条件')

        search_obj = cls.search().extra(
            from_=(page - 1) * page_size, size=page_size
        ).sort(order)

        search_obj = search_obj.query(query_filter)

        response = search_obj.execute()
        total = response.hits.total
        sum_total = total
        if total > cls.MAX_ALLOWED_QUESTION_DATA:
            total = cls.MAX_ALLOWED_QUESTION_DATA
        hits = response.hits.hits

        res_list = []
        if len(hits) > 0:
            for dt in hits:
                res = cls.es_response_format(dt)
                res_list.append(res)

        res = {
            'data': res_list,
            'total': sum_total,
            'pages': ceil(total / page_size),
            'current_page': page
        }
        return res

    @classmethod
    def validate_order(cls, order):
        supported_order = [
            'create_time', 'update_time',
            '-create_time', '-update_time',
            'birthday', '-birthday'
        ]

        if order not in supported_order:
            raise (
                'order只支持create_time、update_time、birthday的排序'
            )

        return order
