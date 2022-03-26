"""
一些多适配器通用的规则。
"""
from nonebot.adapters import Event
from nonebot.rule import Rule

from .consts import FEISHU, ONEBOT, QQGUILD, TELEGRAM
from .deps import AdapterName
from .exception import NotSupportException


async def _only_private_message(event: Event, adapter_name: str = AdapterName()) -> bool:
    if adapter_name == ONEBOT:
        from nonebot.adapters.onebot.v11 import PrivateMessageEvent

        # EventName == "message.private"
        return isinstance(event, PrivateMessageEvent)

    elif adapter_name == FEISHU:
        from nonebot.adapters.feishu import PrivateMessageEvent

        # EventName == "message.p2p"
        return isinstance(event, PrivateMessageEvent)

    elif adapter_name == TELEGRAM:
        # experimental code
        from nonebot.adapters.telegram import PrivateMessageEvent  # type: ignore

        # EventName == "message.private"
        return isinstance(event, PrivateMessageEvent)

    elif adapter_name == QQGUILD:
        raise NotSupportException(f"{QQGUILD!r} not support PrivateMessageEvent.")

    # add logger
    return False


def only_private_message() -> Rule:
    """匹配私聊消息。

    适配: OneBot, Feishu
    实验性适配: Telegram
    不支持: QQGuild。
    """
    return Rule(_only_private_message)
