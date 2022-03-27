"""提供常用的权限检查。"""
from nonebot.permission import Permission

from .consts import FEISHU as FEISHU_c
from .consts import ONEBOT as ONEBOT_c
from .consts import QQGUILD as QQGUILD_c
from .consts import TELEGRAM as TELEGRAM_c
from .deps import AdapterName, EventName


class PrivateMessage:
    """检查是否为私聊消息事件，不支持的适配会返回 False。

    适配: OneBot, Feishu, Telegram
    不支持: QQGuild
    """

    __slots__ = ()

    async def __call__(
        self, event_name: str = EventName(), adapter_name: str = AdapterName()
    ) -> bool:
        if adapter_name in (ONEBOT_c, TELEGRAM_c):
            return event_name.startswith("message.private")
        elif adapter_name == FEISHU_c:
            return event_name == "message.p2p"
        return False


class _check_adapter_name:
    __slots__ = ("adapter_name",)

    def __init__(self, adapter_name: str) -> None:
        self.adapter_name = adapter_name

    async def __call__(self, adapter_name: str = AdapterName()) -> bool:
        return self.adapter_name == adapter_name


PRIVATEMESSAGE: Permission = Permission(PrivateMessage())

ONEBOT: Permission = Permission(_check_adapter_name(ONEBOT_c))

FEISHU: Permission = Permission(_check_adapter_name(FEISHU_c))

TELEGRAM: Permission = Permission(_check_adapter_name(TELEGRAM_c))

QQGUILD: Permission = Permission(_check_adapter_name(QQGUILD_c))
