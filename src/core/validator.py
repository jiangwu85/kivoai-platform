"""
doc：https://pydantic-docs.helpmanual.io/usage/validators/#reuse-validators
"""

import re


def vali_telephone(value: str) -> str:
    if not value or len(value) != 11 or not value.isdigit():
        raise ValueError("Please enter your phone number!")
    regex = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'
    if not re.match(regex, value):
        raise ValueError("Please enter a correct phone number!")

    return value


def vali_email(value: str) -> str:
    if not value:
        raise ValueError("Please enter your email address!")

    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(regex, value):
        raise ValueError("Value error, please enter a correct email address!")

    return value




