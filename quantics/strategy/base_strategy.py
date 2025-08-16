"""
基础策略类

提供所有策略共用的基础功能，包括：
- 日志记录
- 订单管理
- 基础回测功能
"""

import backtrader as bt
from datetime import datetime


class BaseStrategy(bt.Strategy):
    """
    基础策略类
    
    提供所有策略共用的基础功能：
    - 统一的日志记录格式
    - 订单状态管理
    - 基础的回测功能
    """
    
    params = (
        ('printlog', True),  # 是否打印日志
    )
    
    def log(self, txt, dt=None):
        """
        统一的日志记录函数
        
        参数：
        - txt: 要记录的文本信息
        - dt: 日期时间，如果为None则使用当前数据的时间
        
        作用：统一管理策略运行过程中的日志输出
        """
        if self.params.printlog:
            dt = dt or self.datas[0].datetime.date(0)
            print(f'{dt.isoformat()}, {txt}')
            print(f'当前资金: {self.broker.getvalue():.2f}')
    
    def notify_order(self, order):
        # 订单提交或接受状态，等待执行
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        # 检查订单是否已完成
        if order.status == order.Completed:
            if order.isbuy():
                self.log(f'买单执行, 价格: {order.executed.price:.2f}, 股数: {order.executed.size}')
            else:
                self.log(f'卖单执行, 价格: {order.executed.price:.2f}, 股数: {order.executed.size}')
            self.order = None  # 重置订单状态
        
        # 处理订单被拒绝或取消的情况
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            status_str = {
                order.Canceled: '已取消',
                order.Margin: '保证金不足',
                order.Rejected: '已拒绝'
            }
            self.log(f'订单{status_str[order.status]}')
            if order.status == order.Margin:
                self.log(f'可用资金: {self.broker.getcash():.2f}')
            self.order = None  # 重置订单状态
    
    def stop(self):
        """
        策略结束函数
        
        作用：
        1. 策略运行结束时的清理工作
        2. 输出最终结果和统计信息
        3. 记录策略表现
        
        执行时机：策略运行结束时，只执行一次
        """
        self.log(f'策略结束，期末资金: {self.broker.getvalue():.2f}')
    
    def next(self):
        """
        策略核心决策函数
        
        子类必须重写此方法来实现具体的交易逻辑
        
        作用：
        1. 在每个时间点分析市场数据
        2. 根据技术指标生成交易信号
        3. 执行买入或卖出操作
        
        执行时机：每个交易日（每个bar）都会调用一次
        """
        raise NotImplementedError("子类必须实现next方法")
