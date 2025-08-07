"""
量化交易策略包

包含多种交易策略的实现，包括：
- 移动平均线交叉策略
- RSI策略
- 布林带策略
- MACD策略
- Buy & Hold策略

以及相关的回测工具和数据分析组件。
"""

from .base_strategy import BaseStrategy
from .moving_average_strategy import MovingAverageCrossStrategy
from .rsi_strategy import RSIStrategy
from .bollinger_bands_strategy import BollingerBandsStrategy
from .macd_strategy import MACDStrategy
from .buy_hold_strategy import BuyHoldStrategy
from .backtest_utils import BacktestUtils
from .data_loader import DataLoader

__all__ = [
    'BaseStrategy',
    'MovingAverageCrossStrategy',
    'RSIStrategy',
    'BollingerBandsStrategy',
    'MACDStrategy',
    'BuyHoldStrategy',
    'BacktestUtils',
    'DataLoader'
]
