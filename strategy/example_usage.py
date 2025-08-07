"""
策略使用示例

展示如何使用拆分后的策略进行回测和比较
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strategy import (
    MovingAverageCrossStrategy,
    RSIStrategy,
    BollingerBandsStrategy,
    MACDStrategy,
    BuyHoldStrategy,
    DataLoader,
    BacktestUtils
)

import matplotlib.pyplot as plt
import pandas as pd


def main():
    """
    主函数：演示策略的使用方法
    """
    print("=== 量化交易策略演示 ===")
    
    # 1. 数据加载
    print("\n1. 加载数据...")
    data_loader = DataLoader()
    
    # 定义回测参数
    ticker_symbol = '002745.SZ'
    start_date = '2022-03-02'
    end_date = '2025-03-02'
    
    # 加载股票数据
    stock_data = data_loader.load_stock_data(ticker_symbol, start_date, end_date)
    
    # 创建Backtrader数据源
    data_feed = data_loader.create_bt_data_feed(stock_data)
    
    # 2. 初始化回测工具
    print("\n2. 初始化回测工具...")
    backtest_utils = BacktestUtils(initial_cash=100000.0, commission=0.001)
    
    # 3. 运行单个策略回测
    print("\n3. 运行移动平均线策略回测...")
    cerebro, strategy, results = backtest_utils.run_backtest(
        MovingAverageCrossStrategy,
        data_feed,
        fast_period=20,
        slow_period=50,
        printlog=True
    )
    
    # 4. 策略比较
    print("\n4. 比较多个策略...")
    strategy_configs = [
        ('MA Cross', MovingAverageCrossStrategy, dict(fast_period=20, slow_period=50)),
        ('RSI', RSIStrategy, dict(rsi_period=14, rsi_low=30, rsi_high=70)),
        ('Bollinger Bands', BollingerBandsStrategy, dict(period=20, devfactor=2.0)),
        ('MACD', MACDStrategy, dict(fastperiod=12, slowperiod=26, signalperiod=9)),
        ('Buy & Hold', BuyHoldStrategy, dict()),
    ]
    
    performance_df = backtest_utils.compare_strategies(strategy_configs, data_feed)
    
    # 5. 参数优化示例
    print("\n5. 移动平均线策略参数优化...")
    param_ranges = {
        'fast_period': [10, 15, 20, 25],
        'slow_period': [40, 50, 60, 70]
    }
    
    optimization_df = backtest_utils.optimize_parameters(
        MovingAverageCrossStrategy,
        data_feed,
        param_ranges,
        metric='Sharpe Ratio'
    )
    
    # 6. 使用最佳参数运行回测
    if len(optimization_df) > 0:
        print("\n6. 使用最佳参数运行回测...")
        best_params = optimization_df.iloc[0]
        
        cerebro_best, strategy_best, results_best = backtest_utils.run_backtest(
            MovingAverageCrossStrategy,
            data_feed,
            fast_period=int(best_params['fast_period']),
            slow_period=int(best_params['slow_period']),
            printlog=True
        )
        
        # 绘制结果
        print("\n7. 绘制回测结果...")
        backtest_utils.plot_results(cerebro_best, style='candlestick')
    
    print("\n=== 演示完成 ===")


def quick_test():
    """
    快速测试函数：运行单个策略
    """
    print("=== 快速测试 ===")
    
    # 数据加载
    data_loader = DataLoader()
    stock_data = data_loader.load_stock_data('002745.SZ', '2022-03-02', '2025-03-02')
    data_feed = data_loader.create_bt_data_feed(stock_data)
    
    # 运行RSI策略
    backtest_utils = BacktestUtils()
    cerebro, strategy, results = backtest_utils.run_backtest(
        RSIStrategy,
        data_feed,
        rsi_period=14,
        rsi_low=30,
        rsi_high=70,
        printlog=False  # 关闭日志以简化输出
    )
    
    print("快速测试完成")


if __name__ == "__main__":
    # 运行完整演示
    main()
    
    # 或者运行快速测试
    # quick_test()
