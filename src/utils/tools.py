import datetime
import importlib
import os
import random

from fastapi import UploadFile
from core.logger import logger


def clac_time_diff(start_date: str, end_date: str = None):
    """
    获取时间差
    :param start_date: %Y-%m-%d %H:%M:%S
    :param end_date: %Y-%m-%d %H:%M:%S
    :return: 秒
    """
    start_time = datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    if not end_date:
        end_time = datetime.datetime.now()
    else:
        end_time = datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    return int((start_time - end_time).total_seconds())


class TimeClac:
    """
    时间计算
    """

    def __init__(self, vtime: str):
        """
        初始化时间
        :param vtime: %Y-%m-%d %H:%M:%S
        """
        self.vtime = vtime
        self.ptime = datetime.datetime.strptime(vtime, "%Y-%m-%d %H:%M:%S")

    def subtraction(self, seconds: int, obj: bool = False):
        """
        减去秒数
        :param seconds: 秒数
        :param obj: 是否返回时间对象
        :return:
        """
        result = self.ptime - datetime.timedelta(seconds=seconds)
        if obj:
            return result
        return result.strftime("%Y-%m-%d %H:%M:%S")


def import_module(modules: list, desc: str, **kwargs):
    for module in modules:
        if not module:
            continue
        try:
            # 动态导入模块
            module_pag = importlib.import_module(module[0:module.rindex(".")])
            getattr(module_pag, module[module.rindex(".") + 1:])(**kwargs)
        except ModuleNotFoundError:
            logger.error(f"AttributeError：导入{desc}失败，未找到该模块：{module}")
        except AttributeError:
            logger.error(f"ModuleNotFoundError：导入{desc}失败，未找到该模块下的方法：{module}")


async def import_module_async(modules: list, desc: str, **kwargs):
    for module in modules:
        if not module:
            continue
        try:
            # 动态导入模块
            module_pag = importlib.import_module(module[0:module.rindex(".")])
            await getattr(module_pag, module[module.rindex(".") + 1:])(**kwargs)
        except ModuleNotFoundError:
            logger.error(f"AttributeError：导入{desc}失败，未找到该模块：{module}")
        except AttributeError:
            logger.error(f"ModuleNotFoundError：导入{desc}失败，未找到该模块下的方法：{module}")


def get_code(length: int = 6, blend: bool = False) -> str:
    """
    随机获取短信验证码
    短信验证码只支持数字，不支持字母及其他符号

    :param length: 验证码长度
    :param blend: 是否 字母+数字 混合
    """
    code = ""  # 创建字符串变量,存储生成的验证码
    for i in range(length):  # 通过for循环控制验证码位数
        num = random.randint(0, 9)  # 生成随机数字0-9
        if blend:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            # 随机选择其中一位
            num = random.choice([num, upper_alpha, lower_alpha])
        code = code + str(num)
    return code


def calculate_time(days=0, hours=0, minutes=0, seconds=0):
    """
    时间计算
    """
    now = datetime.datetime.now()
    target_time = now + datetime.timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )
    return target_time.strftime("%Y-%m-%d %H:%M:%S")
