"""提供常用的权限检查。"""
from nonebot.permission import Permission

from .consts import FEISHU, ONEBOT, TELEGRAM
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
        if adapter_name in (ONEBOT, TELEGRAM):
            return event_name.startswith("message.private")
        elif adapter_name == FEISHU:
            return event_name == "message.p2p"
        return False


PRIVATEMESSAGE: Permission = Permission(PrivateMessage())
