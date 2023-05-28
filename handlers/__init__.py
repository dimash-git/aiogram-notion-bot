from .users import trade, size, leverage, common


def setup(bot, dp):
    trade.setup(dp)
    size.setup(bot, dp)
    leverage.setup(bot, dp)
    common.setup(dp)
