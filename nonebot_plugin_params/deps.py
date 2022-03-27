from functools import lru_cache
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Awaitable, Callable, Optional, Type, Union, cast

from nonebot.adapters import Bot, Event, MessageSegment
from nonebot.params import Depends

from .consts import FEISHU, ONEBOT, QQGUILD, TELEGRAM
from .exception import NotSupportException

if TYPE_CHECKING:
    from nonebot.adapters.feishu import MessageSegment as Feishu_MessageSegment
    from nonebot.adapters.onebot.v11 import MessageSegment as OneBot_MessageSegment
    from nonebot.adapters.qqguild import MessageSegment as QQGuild_MessageSegment


async def _event_name(event: Event) -> str:
    return event.get_event_name()


def EventName() -> str:
    return Depends(_event_name)


async def _adapter_name(bot: Bot) -> str:
    return bot.adapter.get_name()


def AdapterName() -> str:
    """获取 Adapter 名字。"""
    return Depends(_adapter_name)


def _generic_message_segment_class(bot: Bot, _fake_key: int) -> Type[MessageSegment]:
    """This is implicit, so only use if adapter not support.

    `_fake_key` prevent this function to be a dependency.
    """
    from importlib import import_module

    adapter_package = import_module("..", bot.__class__.__module__)
    return adapter_package.__dict__["MessageSegment"]


@lru_cache(maxsize=10)
def __message_segment_class(adapter_name: str) -> Optional[Type[MessageSegment]]:
    if adapter_name == ONEBOT:
        from nonebot.adapters.onebot.v11 import MessageSegment

        return MessageSegment

    elif adapter_name == FEISHU:
        from nonebot.adapters.feishu import MessageSegment

        return MessageSegment

    elif adapter_name == QQGUILD:
        from nonebot.adapters.qqguild import MessageSegment

        return MessageSegment


async def _message_segment_class(
    bot: Bot, adapter_name: str = AdapterName()
) -> Type[MessageSegment]:
    ms = __message_segment_class(adapter_name)
    if ms is None:
        return _generic_message_segment_class(bot, 0)
    return ms


def MessageSegmentClass() -> Type[MessageSegment]:
    """获取 Adapter 对应的 MessageSegment 类。

    适配: OneBot, Feishu, QQGuild
    实验性适配: Telegram
    """
    return Depends(_message_segment_class)


class _get_image_segment:
    auto_convertion: bool = True
    """如果能够转换，则自动转换图片类型。如 Path 转 str， BytesIO 转 bytes。"""

    def __init__(
        self,
        bot: Bot,
        adapter_name: str = AdapterName(),
        MS: Type[MessageSegment] = MessageSegmentClass(),
    ) -> None:
        self.bot = bot
        self.adapter_name = adapter_name
        self._MS = MS

    async def __call__(self, file: Union[str, bytes, BytesIO, Path]) -> MessageSegment:
        if self.adapter_name == ONEBOT:
            self._MS = cast("OneBot_MessageSegment", self._MS)
            return self._MS.image(file)

        elif self.adapter_name == FEISHU:
            # experimental code
            self._MS = cast("Feishu_MessageSegment", self._MS)
            if isinstance(file, (str, Path)):
                with open(file, "rb") as f:
                    file = f.read()
            elif isinstance(file, BytesIO):
                file = file.getvalue()
            response = await self.bot.call_api(
                "im/v1/images", image_type="message", image=file
            )
            image_key = response["image_key"]
            return self._MS.image(image_key)

        elif self.adapter_name == TELEGRAM:
            # experimental code
            from nonebot.adapters.telegram.message import File  # type: ignore

            if isinstance(file, BytesIO):
                file = file.getvalue()
            elif isinstance(file, Path):
                file = str(file)

            return File.photo(file)

        elif self.adapter_name == QQGUILD:
            self._MS = cast("QQGuild_MessageSegment", self._MS)

            if isinstance(file, str):
                return self._MS.image(file)
            else:
                raise ValueError(
                    f"{QQGUILD!r} not support image type {type(file)}. See: "
                    "https://github.com/nonebot/adapter-qqguild/blob/master/nonebot/adapters/qqguild/message.py"
                )

        if hasattr(self._MS, "image"):
            return self._MS.image(file)  # type: ignore

        raise NotSupportException


def ImageSegmentMethod() -> Callable[
    [Union[str, bytes, BytesIO, Path]], Awaitable[MessageSegment]
]:
    """获取 Image Segment 的构造方法。

    适配: OneBot, QQGuild
    实验性适配: Feishu, Telegram
    """
    return Depends(_get_image_segment)
