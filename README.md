# nonebot-plugin-params

此插件为插件编写者提供便利的函数用于实现多适配器兼容。

可以避免一长串的 try...except 语句来实现的多适配器兼容代码。

比如说我的插件只需要发送 text 和 at 类型的消息，这是基本所有适配器都实现的功能。为了拿到 MessageSegment 目前只能使用 try...import... 于是此插件提供了一行式的注入函数来拿到当前适配器对应的 MessageSegment。

比如说我只想匹配私聊消息类型，我可以在 handler 使用 try...import 然后再 isinstance，但这无疑很繁琐而且没有任何可读性。但是不用 isinstance 好像又做不成，因为不是所有私聊消息类型都叫 `message.private`，QQ 里有子类型 friend 和 group，飞书里则叫做 `message.p2p`，去阅读这些东西会耗费大量时间。

此插件并没有完全避免上述情况发生，但是提供了一些便捷的方式去访问适配器类型，提供了一些便捷的函数如 `is_private_message` 来适配所有私聊类型。

## 安装 Install

```
pip install nonebot-plugin-params
```

## 注意 Warning

引用本插件前，在 `__init__.py` 头部使用 require 保证插件加载。

```python
from nonebot import require

require("nonebot_plugin_params")

# writing main code
import os

from nonebot_plugin_params import ONEBOT
```

## 插件示例 Example

先来看一个简单的示例程序，这是 [示例插件项目地址](https://github.com/iyume/nonebot-plugin-wordle)，这里只提取了一部分用作示例。

```python
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
```

如果你有 QQ 和 Feishu 两个机器人，可以尝试一下上面这个程序。

下面解释一些代码的作用。

```python
from nonebot_plugin_params import ONEBOT, FEISHU, TELEGRAM, QQGUILD
```

导入适配器名称，可以用于便利的条件判断。

```python
wordle = on_command("wordle", rule=allow_adapters(ONEBOT, FEISHU) & is_private_message)
```

其中 rule 作用是使得当前这个 matcher 仅接受来自 QQ 或者 Feishu 的事件，并且都是私聊事件。

```python
@wordle.handle()
async def _(
    matcher: Matcher,
    adapter_name: str = AdapterName(),
    MS: Type[MessageSegment] = MessageSegmentClass(),
) -> None:
    await matcher.send("欢迎来到 wordle")
```

其中 `MessageSegmentClass()` 获取当前适配器对应的 MessageSegment 类。

## 可用 API

- `ONEBOT`

- `FEISHU`

- `TELEGRAM`

- `QQGUILD`

- `AdapterName`

- `EventName`

- `ImageSegmentMethod`

- `MessageSegmentClass`

- `PRIVATEMESSAGE`

- `allow_adapters`

- `is_private_message`
