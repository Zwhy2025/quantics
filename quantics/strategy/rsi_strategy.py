"""
RSI策略

实现基于相对强弱指数(RSI)的交易策略：
- RSI < 30 => 超卖信号，买入
- RSI > 70 => 超买信号，卖出
"""

import backtrader as bt
from .base_strategy import BaseStrategy


class RSIStrategy(BaseStrategy):
    """
    RSI策略类 - 基于相对强弱指数(RSI)的量化交易策略
    
    策略逻辑:
    - 当 RSI < 30 => 全仓买入 (超卖信号)
    - 当 RSI > 70 => 卖出全部 (超买信号)
    
    参数说明:
    - rsi_period: RSI计算周期，默认14天
    - rsi_low: RSI超卖阈值，默认30
    - rsi_high: RSI超买阈值，默认70
    - printlog: 是否打印日志，默认True
    """
    
    params = (
        ('rsi_period', 14),
        ('rsi_low', 30),
        ('rsi_high', 70),
        ('printlog', True),
    )
    
    def __init__(self):
        """
        策略初始化函数
        
        初始化内容:
        - order: 订单对象，用于跟踪当前订单状态
        - rsi: RSI指标对象，基于SMA计算的相对强弱指数
        """
        self.order = None
        self.rsi = bt.indicators.RSI_SMA(self.datas[0], period=self.params.rsi_period)
    
    def next(self):
        """
        策略核心逻辑函数
        
        在每个交易周期被调用，实现主要的交易决策逻辑:
        1. 获取当前价格和RSI值
        2. 检查是否有待处理订单
        3. 根据持仓状态和RSI值决定买入或卖出
        """
        price = self.datas[0].close[0]
        rsi_value = self.rsi[0]
        self.log(f'收盘价: {price:.2f}, RSI: {rsi_value:.2f}')
        
        if self.order:
            return
        
        # 若无持仓，且 RSI < 30 => 全仓买入
        if not self.position:
            if rsi_value < self.params.rsi_low:
                cash = self.broker.getcash()
                size = int(cash // price)
                if size > 0:
                    self.log(f'买入信号 (RSI<{self.params.rsi_low}), 全仓买入: {size} 股')
                    self.order = self.buy(size=size)
        else:
            # 有持仓时，若 RSI > 70 => 卖出全部
            if rsi_value > self.params.rsi_high:
                self.log(f'卖出信号 (RSI>{self.params.rsi_high}), 卖出全部: {self.position.size} 股')
                self.order = self.sell(size=self.position.size)
