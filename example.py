from typing import TYPE_CHECKING, Type, cast

from nonebot import on_command
from nonebot.adapters import Event, MessageSegment
from nonebot.matcher import Matcher

from nonebot_plugin_params import (
    FEISHU,
    ONEBOT,
    AdapterName,
    MessageSegmentClass,
    allow_adapters,
    is_private_message,
)

if TYPE_CHECKING:
    from nonebot.adapters.feishu import MessageSegment as Feishu_MessageSegment
    from nonebot.adapters.onebot.v11 import MessageSegment as Onebot_MessageSegment


wordle = on_command("wordle", rule=allow_adapters(ONEBOT, FEISHU) & is_private_message)


@wordle.handle()
async def _(
    matcher: Matcher,
    event: Event,
    adapter_name: str = AdapterName(),
    MS: Type[MessageSegment] = MessageSegmentClass(),
) -> None:
    await matcher.send("欢迎来到 wordle")
    if adapter_name == ONEBOT:
        MS = cast("Type[Onebot_MessageSegment]", MS)  # only for type hint
        await matcher.send(MS.at(event.get_user_id()) + MS.text("mua~"))
        # user id like "1748272409"

    elif adapter_name == FEISHU:
        MS = cast("Type[Feishu_MessageSegment]", MS)  # only for type hint
        await matcher.send(MS.at(event.get_user_id()) + MS.text("mua~"))
        # user id like "3e3cf96b"
