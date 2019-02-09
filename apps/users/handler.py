import json
import time
from user_search.handler import BaseHandler
from apps.users.forms import (
    RegisterForm,
)

from apps.users.models import User
from apps.rs_es.user.es_model import EsUser
from playhouse.shortcuts import model_to_dict
from apps.core.utils import format_arguments
from apps.rs_es.tasks import insert_user_es


class RegisterHandler(BaseHandler):
    async def post(self, *args, **kwargs):
        req_data = self.request.body.decode("utf-8")
        req_data = json.loads(req_data)
        regester_form = RegisterForm.from_json(req_data)
        res_data = {}
        if regester_form.validate():
            username = regester_form.username.data
            first_name = regester_form.first_name.data
            last_name = regester_form.last_name.data
            address = regester_form.address.data
            description = regester_form.description.data
            birthday = regester_form.birthday.data
            try:
                await self.application.objects.get(
                    User, username=username
                )
                self.set_status(400)
                res_data["content"] = "用于已存在"
            except User.DoesNotExist:
                user_obj = await self.application.objects.create(
                    User, username=username,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    birthday=birthday,
                    description=description
                )
                res_data["id"] = user_obj.id
                res_data["content"] = "创建用户成功"
                user_dict = model_to_dict(user_obj)
                user_dict["birthday"] = str(birthday)
                insert_user_es.delay(user_dict)
        else:
            res_data["content"] = regester_form.errors
        self.finish(res_data)


class EsUserSearchHandler(BaseHandler):
    """
    GET:
    通过ES读取用户数据
    Demo Params:
    search?keyword=上海&full_name=bb aa
    """
    search_fields = [
        ('page', '分页数'),
        ('per_page', '每页展示数'),
        ('keyword', '关键字搜索，（地址，个人描述）'),
        ('id', '用户ID'),
        ('username', '用户名'),
        ('first_name', '名子'),
        ('last_name', '姓氏'),
        ('full_name', '全名'),
        ('order', 'LIST结构，支持birthday和create_time的排序'),
        ('start_time', '用户创建的开始时间'),
        ('end_time', '用户创建结束时间'),
        ('start_birth', 'birth起始时间'),
        ('end_birth', 'birth结束时间'),
    ]

    def get(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        page_size = self.get_argument('per_page', 10)
        page = self.get_argument('page', 1)
        order = self.get_argument('order', '-update_time')
        req_data = self.request.arguments
        req_data = format_arguments(req_data)
        query_filter = self.generate_query_filter(req_data)
        res_data = EsUser.search_user(
            query_filter=query_filter,
            order=order,
            page_size=page_size,
            page=page
        )
        self.write(res_data)

    @classmethod
    def generate_query_filter(cls, req_data):
        query_filter = None

        # 日期过滤条件
        rs_date_filter = {
            'start_time': None,
            'end_time': int(time.time()) * 1000
        }

        birth_filter = {
            'start_birth': None,
            'end_birth': None
        }

        for doc_field in cls.search_fields:
            filed = doc_field[0]
            field_val = req_data.get(filed)

            # 如果存在field的值
            if field_val or field_val == 0:
                # 正常字段
                if filed in ['id']:
                    query_filter = EsUser.generate_search_query(
                        query_filter, 'filter', filed, field_val
                    )
                # 关键字搜索，要搜索address, description
                elif filed in ['keyword']:
                    query_filter = EsUser.generate_search_query(
                        query_filter, 'rs_keyword', filed, field_val
                    )
                elif filed in ['start_time', 'end_time']:
                    rs_date_filter[filed] = field_val
                elif filed in ['username']:
                    query_filter = EsUser.generate_search_query(
                        query_filter, 'wildcard', filed, field_val
                    )
                elif filed in ['first_name', 'last_name', 'full_name']:
                    query_filter = EsUser.generate_search_query(
                        query_filter, 'copy_to', filed, field_val
                    )
                elif filed in ['start_birth', 'end_birth']:
                    default_birth = req_data.get('start_birth') \
                                    or req_data.get('end_birth')
                    birth_filter['start_birth'] = default_birth
                    birth_filter['end_birth'] = default_birth
                    birth_filter[filed] = field_val
                    query_filter = EsUser.generate_search_query(
                        query_filter, 'birthday', filed, birth_filter
                    )

        # 日期过滤条件
        query_filter = EsUser.generate_search_query(
            query_filter, 'rs_date', 'create_time', rs_date_filter
        )
        return query_filter
