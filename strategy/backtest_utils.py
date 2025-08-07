"""
回测工具

提供统一的回测功能，包括：
- 策略回测运行
- 性能指标计算
- 结果分析和可视化
"""

import backtrader as bt
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


class BacktestUtils:
    """
    回测工具类
    
    提供统一的回测功能：
    - 策略回测运行
    - 性能指标计算
    - 结果分析和可视化
    - 参数优化
    """
    
    def __init__(self, initial_cash=100000.0, commission=0.001):
        """
        初始化回测工具
        
        参数：
        - initial_cash: 初始资金，默认100000.0
        - commission: 佣金率，默认0.001 (0.1%)
        """
        self.initial_cash = initial_cash
        self.commission = commission
    
    def run_backtest(self, strategy_class, data_feed, **strategy_params):
        """
        运行回测
        
        参数：
        - strategy_class: 策略类
        - data_feed: 数据源
        - **strategy_params: 策略参数
        
        返回：
        - tuple: (cerebro, strategy, results)
        """
        # 创建Cerebro引擎
        cerebro = bt.Cerebro()
        
        # 添加数据
        cerebro.adddata(data_feed)
        
        # 添加策略
        cerebro.addstrategy(strategy_class, **strategy_params)
        
        # 设置初始资金和佣金
        cerebro.broker.setcash(self.initial_cash)
        cerebro.broker.setcommission(commission=self.commission)
        
        # 添加分析器
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', riskfreerate=0.0)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        
        # 运行策略
        initial_value = cerebro.broker.getvalue()
        print(f'初始资金: ${initial_value:.2f}')
        
        results = cerebro.run()
        strategy = results[0]
        
        # 获取最终资金
        final_value = cerebro.broker.getvalue()
        print(f'最终资金: ${final_value:.2f}')
        print(f'盈亏: ${final_value - initial_value:.2f} ({(final_value / initial_value - 1) * 100:.2f}%)')
        
        # 分析结果
        self._print_performance_metrics(strategy)
        
        return cerebro, strategy, results
    
    def _print_performance_metrics(self, strategy):
        """
        打印性能指标
        
        参数：
        - strategy: 策略对象
        """
        print('\n--- 性能指标 ---')
        
        # 夏普比率
        sharpe_analysis = strategy.analyzers.sharpe.get_analysis()
        sharpe_ratio = sharpe_analysis.get('sharperatio', None)
        print(f'夏普比率: {sharpe_ratio:.4f}' if sharpe_ratio is not None else '夏普比率: N/A')
        
        # 最大回撤
        drawdown_analysis = strategy.analyzers.drawdown.get_analysis()
        max_drawdown = drawdown_analysis.get('max', {}).get('drawdown', None)
        print(f'最大回撤: {max_drawdown:.2f}%' if max_drawdown is not None else '最大回撤: N/A')
        
        # 年化收益率
        returns_analysis = strategy.analyzers.returns.get_analysis()
        annual_return = returns_analysis.get('rnorm100', None)
        print(f'年化收益率: {annual_return:.2f}%' if annual_return is not None else '年化收益率: N/A')
        
        # 交易统计
        trade_analysis = strategy.analyzers.trades.get_analysis()
        if 'total' in trade_analysis and 'closed' in trade_analysis['total']:
            total_trades = trade_analysis['total']['closed']
            won_trades = trade_analysis.get('won', {}).get('total', 0)
            lost_trades = trade_analysis.get('lost', {}).get('total', 0)
            
            print(f'总交易次数: {total_trades}')
            if total_trades > 0:
                win_rate = won_trades / total_trades * 100
                print(f'胜率: {win_rate:.1f}% ({won_trades}/{total_trades})')
    
    def run_strategy_and_get_metrics(self, strategy_class, data_feed, **strategy_params):
        """
        运行策略并获取性能指标
        
        参数：
        - strategy_class: 策略类
        - data_feed: 数据源
        - **strategy_params: 策略参数
        
        返回：
        - dict: 性能指标字典
        """
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(self.initial_cash)
        cerebro.broker.setcommission(commission=self.commission)
        cerebro.adddata(data_feed)
        cerebro.addstrategy(strategy_class, **strategy_params)
        
        # 添加分析器
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns', tann=252)
        
        results = cerebro.run()
        strat = results[0]
        
        # 获取指标
        sharpe = strat.analyzers.sharpe.get_analysis().get('sharperatio', None)
        drawdown = strat.analyzers.drawdown.get_analysis().get('max', {}).get('drawdown', None)
        annual_return = strat.analyzers.returns.get_analysis().get('rnorm100', None)
        final_value = cerebro.broker.getvalue()
        
        metrics = {
            'Sharpe Ratio': sharpe,
            'Max Drawdown (%)': drawdown,
            'Annual Return (%)': annual_return,
            'Final Value': final_value,
            'Total Return (%)': (final_value / self.initial_cash - 1) * 100
        }
        
        return metrics
    
    def compare_strategies(self, strategy_configs, data_feed):
        """
        比较多个策略的性能
        
        参数：
        - strategy_configs: 策略配置列表，格式[(name, strategy_class, params), ...]
        - data_feed: 数据源
        
        返回：
        - pandas.DataFrame: 性能比较结果
        """
        results_dict = {}
        
        for name, strat_class, params in strategy_configs:
            print(f"\n正在测试策略: {name}")
            metrics = self.run_strategy_and_get_metrics(strat_class, data_feed, **params)
            results_dict[name] = metrics
        
        performance_df = pd.DataFrame.from_dict(results_dict, orient='index')
        performance_df = performance_df.sort_values('Annual Return (%)', ascending=False)
        
        print("\n策略绩效对比：")
        print(performance_df)
        
        return performance_df
    
    def optimize_parameters(self, strategy_class, data_feed, param_ranges, metric='Sharpe Ratio'):
        """
        参数优化
        
        参数：
        - strategy_class: 策略类
        - data_feed: 数据源
        - param_ranges: 参数范围字典，格式{'param_name': [values]}
        - metric: 优化指标，默认'Sharpe Ratio'
        
        返回：
        - pandas.DataFrame: 优化结果
        """
        import itertools
        
        # 生成所有参数组合
        param_names = list(param_ranges.keys())
        param_values = list(param_ranges.values())
        param_combinations = list(itertools.product(*param_values))
        
        optimization_results = []
        
        print(f"开始参数优化，总共{len(param_combinations)}个参数组合...")
        
        for i, combination in enumerate(param_combinations):
            # 构建参数字典
            params = dict(zip(param_names, combination))
            
            try:
                metrics = self.run_strategy_and_get_metrics(strategy_class, data_feed, **params)
                
                # 添加参数信息
                result = {**params, **metrics}
                optimization_results.append(result)
                
                print(f"[{i+1}/{len(param_combinations)}] 参数: {params}")
                print(f"    夏普比率: {metrics['Sharpe Ratio']:.4f}")
                print(f"    年化收益率: {metrics['Annual Return (%)']:.2f}%")
                print(f"    最大回撤: {metrics['Max Drawdown (%)']:.2f}%")
                
            except Exception as e:
                print(f"[{i+1}/{len(param_combinations)}] 参数 {params} 运行失败: {str(e)}")
        
        # 转换为DataFrame并排序
        optimization_df = pd.DataFrame(optimization_results)
        if len(optimization_df) > 0:
            optimization_df = optimization_df.sort_values(metric, ascending=False)
            
            print(f"\n=== 按{metric}排序的最佳参数组合 ===")
            print(optimization_df.head(10))
        
        return optimization_df
    
    def plot_results(self, cerebro, style='candlestick', **plot_kwargs):
        """
        绘制回测结果
        
        参数：
        - cerebro: Cerebro引擎
        - style: 绘图样式
        - **plot_kwargs: 其他绘图参数
        """
        try:
            cerebro.plot(style=style, **plot_kwargs)
        except Exception as e:
            print(f"绘图失败: {str(e)}")
            print("请检查matplotlib配置")
    
    def create_equity_analyzer(self):
        """
        创建资金曲线分析器
        
        返回：
        - bt.Analyzer: 资金曲线分析器
        """
        class EquityCurveAnalyzer(bt.Analyzer):
            def start(self):
                self.equity = []
                self.dates = []
            
            def next(self):
                # 每个bar记录一次资金量
                self.equity.append(self.strategy.broker.getvalue())
                # 将 datetime 转换为日期对象
                dt = self.strategy.datas[0].datetime.date(0)
                self.dates.append(dt)
            
            def get_analysis(self):
                return {'dates': self.dates, 'equity': self.equity}
        
        return EquityCurveAnalyzer
