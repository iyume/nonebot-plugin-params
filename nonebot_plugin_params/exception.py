from nonebot.exception import AdapterException


class ValidationError(Exception):
    ...


class NotSupportException(Exception):
    """本插件未支持的适配器，或者适配器不支持对应功能。"""
