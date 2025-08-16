"""
Buy & Hold策略

实现最简单的买入持有策略：
- 在第一个交易日全仓买入
- 持有到回测结束
"""

import backtrader as bt
from .base_strategy import BaseStrategy


class BuyHoldStrategy(BaseStrategy):
    """
    Buy & Hold策略类 - 最简单的买入持有策略
    
    策略逻辑:
    - 在第一个交易日全仓买入
    - 持有到回测结束，不进行任何交易
    
    核心思想：长期投资，相信市场的长期上涨趋势
    通常用作基准策略，用于比较其他策略的表现
    """
    
    params = (
        ('printlog', True),     # 是否打印交易日志
    )
    
    def __init__(self):
        """
        策略初始化函数
        
        初始化内容:
        - order: 订单对象，用于跟踪当前订单状态
        """
        # 订单状态跟踪变量，用于防止重复下单
        self.order = None
    
    def next(self):
        """
        策略核心决策函数
        
        作用：
        1. 在第一个交易日全仓买入
        2. 之后不再进行任何交易
        
        执行时机：每个交易日（每个bar）都会调用一次
        
        策略逻辑：
        - 无持仓时 => 全仓买入（只在第一次）
        - 有持仓时 => 不做任何操作
        """
        # 如果没有持仓，则买入
        if not self.position:
            # 当前现金
            cash = self.broker.getcash()
            # 当前收盘价
            price = self.datas[0].close[0]
            # 计算可买股数（整股）
            size = int(cash // price)  # 使用整除保证是整数
            
            if size > 0:
                self.log(f'Buy & Hold策略：全仓买入 {size} 股')
                self.order = self.buy(size=size)
        
        # 有持仓后，不再进行任何交易
        # 策略将持有到回测结束
