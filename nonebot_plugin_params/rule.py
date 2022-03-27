from typing import Tuple, Union

from nonebot.rule import Rule
from typing_extensions import Literal

from .consts import FEISHU, ONEBOT, QQGUILD, TELEGRAM
from .deps import AdapterName, EventName


class _check_adapter_name:
    __slots__ = ("names",)

    def __init__(self, names: Tuple[str, ...]) -> None:
        self.names = names

    async def __call__(self, adapter_name: str = AdapterName()) -> bool:
        return adapter_name in self.names


def allow_adapters(allows: Tuple[Literal[FEISHU, ONEBOT, QQGUILD, TELEGRAM], ...]) -> Rule:
    return Rule(_check_adapter_name(allows))


async def _is_private_message(
    event_name: str = EventName(), adapter_name: str = AdapterName()
) -> bool:
    if adapter_name in (ONEBOT, TELEGRAM):
        return event_name.startswith("message.private")
    elif adapter_name == FEISHU:
        return event_name == "message.p2p"
    return False


is_private_message: Rule = Rule(_is_private_message)
