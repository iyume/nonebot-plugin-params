from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Optional, Type, Union, cast

from nonebot.adapters import Bot, Event, MessageSegment
from nonebot.exception import ApiNotAvailable
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


def _generic_message_segment_class(event: Event) -> Type[MessageSegment]:
    from importlib import import_module

    adapter_package = import_module("..", event.__class__.__module__)
    return adapter_package.__dict__["MessageSegment"]


async def _message_segment_class(
    event: Event, adapter_name: str = AdapterName()
) -> Type[MessageSegment]:
    if adapter_name == ONEBOT:
        from nonebot.adapters.onebot.v11 import MessageSegment

        return MessageSegment

    elif adapter_name == FEISHU:
        from nonebot.adapters.feishu import MessageSegment

        return MessageSegment

    elif adapter_name == TELEGRAM:
        # from nonebot.adapters.telegram import MessageSegment

        return _generic_message_segment_class(event)

    elif adapter_name == QQGUILD:
        from nonebot.adapters.qqguild import MessageSegment

        return MessageSegment

    return _generic_message_segment_class(event)


def MessageSegmentClass() -> Type[MessageSegment]:
    """获取 Adapter 对应的 MessageSegment 类。

    适配: OneBot, Feishu, QQGuild
    实验性适配: Telegram
    """
    return Depends(_message_segment_class)


class _get_image_segment:
    auto_convertion: bool = False
    """如果能够转换，则自动转换图片类型。如 Path 转 str， BytesIO 转 bytes。"""

    def __init__(
        self,
        adapter_name: str = Depends(AdapterName),
        MS: MessageSegment = Depends(MessageSegmentClass),
    ) -> None:
        self.adapter_name = adapter_name
        self._MS = MS

    def __call__(self, file: Union[str, bytes, BytesIO, Path]) -> MessageSegment:
        if self.adapter_name == ONEBOT:
            self._MS = cast("OneBot_MessageSegment", self._MS)

            return self._MS.image(file)

        elif self.adapter_name == FEISHU:
            self._MS = cast("Feishu_MessageSegment", self._MS)

            if isinstance(file, str):
                return self._MS.image(file)
            else:
                raise ValueError(
                    f"{FEISHU!r} not support image type {type(file)}. See: "
                    "https://feishu.adapters.nonebot.dev/docs/api/message#MessageSegment-image"
                )

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


def ImageSegmentMethod() -> Callable[[Union[str, bytes, BytesIO, Path]], MessageSegment]:
    """获取 Image Segment 的构造方法。

    适配: OneBot, Feishu, QQGuild
    实验性适配: Telegram
    """
    return Depends(_get_image_segment)
