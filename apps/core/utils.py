import time


def get_current_timestamp():
    """
    获取当前时间戳
    :return:
    """
    return int(time.time() * 1000)


def get_int_or_none(val):
    try:
        return int(val)
    except Exception:
        return None


def format_arguments(arguments):
    """
    以request.body_arguments 或者 request.arguments传参时
    将二进制转化utf-8编码
    :param arguments:
    :return:
    """

    data = {
        k: list(
            map(
                lambda val: str(val, encoding="utf-8"),
                v
            )
        )[0]
        for k, v in arguments.items()
    }
    return data
