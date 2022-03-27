from enum import Enum


class Adapter(str, Enum):
    ONEBOT = "OneBot V11"
    FEISHU = "Feishu"
    TELEGRAM = "Telegram"
    QQGUILD = "QQ Guild"


ONEBOT = Adapter.ONEBOT
FEISHU = Adapter.FEISHU
TELEGRAM = Adapter.TELEGRAM
QQGUILD = Adapter.QQGUILD
