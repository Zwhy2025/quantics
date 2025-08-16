"""
移动平均线交叉策略

实现基于移动平均线交叉的交易策略：
- 短期均线上穿长期均线 => 买入信号
- 短期均线下穿长期均线 => 卖出信号
"""

import backtrader as bt
from .base_strategy import BaseStrategy


class MovingAverageCrossStrategy(BaseStrategy):
    """
    移动平均线交叉策略
    
    策略逻辑：
    - 短期均线(SMA_Fast)上穿长期均线(SMA_Slow) => 全仓买入  
    - 短期均线下穿长期均线 => 卖出全部
    
    核心思想：趋势跟踪，在趋势形成时买入，趋势反转时卖出
    """
    
    params = (
        ('fast_period', 20),    # 短期均线周期，默认20天
        ('slow_period', 50),    # 长期均线周期，默认50天
        ('printlog', True),     # 是否打印交易日志
    )
    
    def __init__(self):
        """
        策略初始化函数
        
        作用：
        1. 初始化策略变量和状态
        2. 创建技术指标（移动平均线、交叉信号）
        3. 设置策略参数
        
        执行时机：策略开始前，只执行一次
        """
        # 订单状态跟踪变量，用于防止重复下单
        self.order = None
        
        # 创建短期移动平均线指标
        self.fast_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.fast_period
        )
        
        # 创建长期移动平均线指标
        self.slow_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.slow_period
        )
        
        # 创建交叉信号指标
        # >0: 快线上穿慢线（买入信号）
        # <0: 快线下穿慢线（卖出信号）
        # =0: 无交叉
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)
    
    def next(self):
        """
        策略核心决策函数
        
        作用：
        1. 在每个时间点分析市场数据
        2. 根据技术指标生成交易信号
        3. 执行买入或卖出操作
        
        执行时机：每个交易日（每个bar）都会调用一次
        
        策略逻辑：
        - 无持仓 + 快线上穿慢线 => 全仓买入
        - 有持仓 + 快线下穿慢线 => 卖出全部
        """
        # 如果有未完成的订单，等待订单执行完成
        if self.order:
            return
        
        # 当前无持仓，检查买入信号
        if not self.position:
            # 快线上穿慢线，产生买入信号
            if self.crossover > 0:
                # 获取当前可用现金
                cash = self.broker.getcash()
                # 获取当前收盘价
                price = self.datas[0].close[0]
                # 计算可买入的股数（整股）
                size = int(cash // price)
                
                # 确保有足够的资金买入至少1股
                if size > 0:
                    self.log(f'买入信号 (fast_ma>slow_ma), 全仓买入: {size} 股')
                    # 创建买入订单
                    self.order = self.buy(size=size)
        else:
            # 当前有持仓，检查卖出信号
            # 快线下穿慢线，产生卖出信号
            if self.crossover < 0:
                self.log(f'卖出信号 (fast_ma<slow_ma), 卖出全部: {self.position.size} 股')
                # 创建卖出订单，卖出全部持仓
                self.order = self.sell(size=self.position.size)
