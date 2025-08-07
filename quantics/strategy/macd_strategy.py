"""
MACD策略

实现基于MACD指标的趋势跟踪策略：
- MACD线上穿信号线 => 买入信号
- MACD线下穿信号线 => 卖出信号
"""

import backtrader as bt
from .base_strategy import BaseStrategy


class MACDStrategy(BaseStrategy):
    """
    MACD策略类 - 基于MACD指标的趋势跟踪策略
    
    策略逻辑:
    - 当 MACD 线上穿信号线 => 全仓买入 (趋势向上，买入信号)
    - 当 MACD 线下穿信号线 => 卖出全部 (趋势向下，卖出信号)
    
    核心思路：利用MACD指标的趋势变化来捕捉价格趋势的转折点
    MACD = 快线EMA - 慢线EMA，信号线是MACD的移动平均线
    
    参数说明:
    - fastperiod: 快线EMA周期，默认12天
    - slowperiod: 慢线EMA周期，默认26天  
    - signalperiod: 信号线EMA周期，默认9天
    - printlog: 是否打印日志，默认True
    """
    
    params = (
        ('fastperiod', 12),      # MACD 快线 EMA 周期 (短期指数移动平均线)
        ('slowperiod', 26),      # MACD 慢线 EMA 周期 (长期指数移动平均线)
        ('signalperiod', 9),     # 信号线 EMA 周期 (MACD的移动平均线)
        ('printlog', True),      # 是否打印交易日志
    )
    
    def __init__(self):
        """
        策略初始化函数
        
        初始化内容:
        - order: 订单对象，用于跟踪当前订单状态
        - macd_ind: MACD指标对象，包含MACD线、信号线和柱状图
        - macd_crossover: 交叉信号指标，用于检测MACD线与信号线的交叉
        
        执行时机：策略开始前，只执行一次
        """
        # 订单状态跟踪变量，用于防止重复下单
        self.order = None
        
        # 创建MACD指标对象
        # MACD指标包含三条线：
        # 1. MACD线 = 快线EMA - 慢线EMA (反映价格趋势)
        # 2. 信号线 = MACD线的移动平均线 (平滑MACD线)
        # 3. 柱状图 = MACD线 - 信号线 (反映趋势强度)
        self.macd_ind = bt.indicators.MACD(
            self.datas[0].close,           # 使用收盘价计算
            period_me1=self.p.fastperiod,  # 快线周期 (12天)
            period_me2=self.p.slowperiod,  # 慢线周期 (26天)
            period_signal=self.p.signalperiod  # 信号线周期 (9天)
        )
        
        # 创建交叉信号指标
        # 用于检测MACD线与信号线的交叉情况：
        # >0: MACD线上穿信号线（买入信号，趋势向上）
        # <0: MACD线下穿信号线（卖出信号，趋势向下）
        # =0: 无交叉
        self.macd_crossover = bt.indicators.CrossOver(self.macd_ind.macd, self.macd_ind.signal)
    
    def next(self):
        """
        策略核心决策函数
        
        作用：
        1. 在每个时间点分析MACD指标
        2. 根据MACD线与信号线的交叉生成交易信号
        3. 执行买入或卖出操作
        
        执行时机：每个交易日（每个bar）都会调用一次
        
        策略逻辑：
        - 无持仓 + MACD线上穿信号线 => 全仓买入
        - 有持仓 + MACD线下穿信号线 => 卖出全部
        """
        # 如果有未完成的订单，等待订单执行完成
        if self.order:
            return
        
        # 当前无持仓，检查买入信号
        if not self.position:
            # MACD线上穿信号线，产生买入信号
            if self.macd_crossover > 0:
                # 获取当前可用现金
                cash = self.broker.getcash()
                # 获取当前收盘价
                price = self.datas[0].close[0]
                # 计算可买入的股数（整股）
                size = int(cash // price)
                
                # 确保有足够的资金买入至少1股
                if size > 0:
                    self.log(f'买入信号 (MACD>Signal), 全仓买入: {size} 股, 当前收盘价: {price:.2f}')
                    # 创建买入订单
                    self.order = self.buy(size=size)
        else:
            # 当前有持仓，检查卖出信号
            # MACD线下穿信号线，产生卖出信号
            if self.macd_crossover < 0:
                self.log(f'卖出信号 (MACD<Signal), 卖出全部: {self.position.size} 股')
                # 创建卖出订单，卖出全部持仓
                self.order = self.sell(size=self.position.size)
