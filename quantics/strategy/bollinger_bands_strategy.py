"""
布林带策略

实现基于布林带的均值回归策略：
- 价格跌破下轨 => 买入信号
- 价格突破上轨 => 卖出信号
"""

import backtrader as bt
from .base_strategy import BaseStrategy


class BollingerBandsStrategy(BaseStrategy):
    """
    简单布林带均值回归策略
    
    策略逻辑:
    - 收盘价 < 下轨 => 全仓买入  
    - 收盘价 > 上轨 => 全部卖出  
    
    核心思想：均值回归，当价格偏离均值过多时进行反向操作
    """
    
    params = (
        ('period', 20),         # 布林带周期，默认20天
        ('devfactor', 2.0),     # 标准差倍数，默认2.0
        ('printlog', True),     # 是否打印交易日志
    )
    
    def __init__(self):
        """
        策略初始化函数
        
        初始化内容:
        - order: 订单对象，用于跟踪当前订单状态
        - boll: 布林带指标对象，包含上轨、中轨、下轨
        """
        self.order = None
        self.boll = bt.indicators.BollingerBands(
            self.datas[0],
            period=self.params.period,
            devfactor=self.params.devfactor
        )
    
    def next(self):
        """
        策略核心决策函数
        
        作用：
        1. 在每个时间点分析布林带指标
        2. 根据价格与布林带的位置关系生成交易信号
        3. 执行买入或卖出操作
        
        执行时机：每个交易日（每个bar）都会调用一次
        
        策略逻辑：
        - 无持仓 + 价格跌破下轨 => 全仓买入
        - 有持仓 + 价格突破上轨 => 卖出全部
        """
        close_price = self.datas[0].close[0]
        top = self.boll.top[0]      # 上轨
        bot = self.boll.bot[0]      # 下轨
        
        self.log(f'收盘价: {close_price:.2f}, 上轨: {top:.2f}, 下轨: {bot:.2f}')
        
        if self.order:
            return
        
        if not self.position:
            # 跌破下轨 => 全仓买入
            if close_price < bot:
                cash = self.broker.getcash()
                size = int(cash // close_price)
                if size > 0:
                    self.log(f'买入信号 (收盘价<下轨), 全仓买入: {size} 股')
                    self.order = self.buy(size=size)
        else:
            # 突破上轨 => 全部卖出
            if close_price > top:
                self.log(f'卖出信号 (收盘价>上轨), 卖出全部: {self.position.size} 股')
                self.order = self.sell(size=self.position.size)
