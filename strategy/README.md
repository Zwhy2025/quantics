# 量化交易策略包

这个包包含了多种量化交易策略的实现，以及相关的回测工具和数据分析组件。

## 策略列表

### 1. 移动平均线交叉策略 (MovingAverageCrossStrategy)
- **策略逻辑**: 短期均线上穿长期均线买入，下穿卖出
- **参数**: 
  - `fast_period`: 短期均线周期，默认20天
  - `slow_period`: 长期均线周期，默认50天
- **适用场景**: 趋势跟踪，适合有明显趋势的市场

### 2. RSI策略 (RSIStrategy)
- **策略逻辑**: RSI < 30买入，RSI > 70卖出
- **参数**:
  - `rsi_period`: RSI计算周期，默认14天
  - `rsi_low`: 超卖阈值，默认30
  - `rsi_high`: 超买阈值，默认70
- **适用场景**: 均值回归，适合震荡市场

### 3. 布林带策略 (BollingerBandsStrategy)
- **策略逻辑**: 价格跌破下轨买入，突破上轨卖出
- **参数**:
  - `period`: 布林带周期，默认20天
  - `devfactor`: 标准差倍数，默认2.0
- **适用场景**: 均值回归，适合波动率稳定的市场

### 4. MACD策略 (MACDStrategy)
- **策略逻辑**: MACD线上穿信号线买入，下穿卖出
- **参数**:
  - `fastperiod`: 快线周期，默认12天
  - `slowperiod`: 慢线周期，默认26天
  - `signalperiod`: 信号线周期，默认9天
- **适用场景**: 趋势跟踪，适合捕捉趋势转折点

### 5. Buy & Hold策略 (BuyHoldStrategy)
- **策略逻辑**: 在第一个交易日全仓买入，持有到结束
- **参数**: 无
- **适用场景**: 基准策略，用于比较其他策略表现

## 工具类

### DataLoader
数据加载工具，提供：
- 从yfinance获取历史数据
- 本地缓存管理
- 数据格式标准化
- 数据验证和修复

### BacktestUtils
回测工具，提供：
- 策略回测运行
- 性能指标计算
- 策略比较
- 参数优化
- 结果可视化

## 使用示例

### 基本使用

```python
from strategy import MovingAverageCrossStrategy, DataLoader, BacktestUtils

# 1. 加载数据
data_loader = DataLoader()
stock_data = data_loader.load_stock_data('002745.SZ', '2022-03-02', '2025-03-02')
data_feed = data_loader.create_bt_data_feed(stock_data)

# 2. 运行回测
backtest_utils = BacktestUtils()
cerebro, strategy, results = backtest_utils.run_backtest(
    MovingAverageCrossStrategy,
    data_feed,
    fast_period=20,
    slow_period=50
)
```

### 策略比较

```python
from strategy import *

# 定义策略配置
strategy_configs = [
    ('MA Cross', MovingAverageCrossStrategy, dict(fast_period=20, slow_period=50)),
    ('RSI', RSIStrategy, dict(rsi_period=14, rsi_low=30, rsi_high=70)),
    ('Bollinger Bands', BollingerBandsStrategy, dict(period=20, devfactor=2.0)),
    ('MACD', MACDStrategy, dict(fastperiod=12, slowperiod=26, signalperiod=9)),
    ('Buy & Hold', BuyHoldStrategy, dict()),
]

# 比较策略性能
backtest_utils = BacktestUtils()
performance_df = backtest_utils.compare_strategies(strategy_configs, data_feed)
```

### 参数优化

```python
# 定义参数范围
param_ranges = {
    'fast_period': [10, 15, 20, 25],
    'slow_period': [40, 50, 60, 70]
}

# 运行参数优化
optimization_df = backtest_utils.optimize_parameters(
    MovingAverageCrossStrategy,
    data_feed,
    param_ranges,
    metric='Sharpe Ratio'
)
```

## 性能指标

每个策略都会计算以下性能指标：
- **夏普比率**: 风险调整后收益
- **最大回撤**: 最大亏损幅度
- **年化收益率**: 年化总收益
- **总交易次数**: 完成的交易数量
- **胜率**: 盈利交易占比

## 文件结构

```
strategy/
├── __init__.py                 # 包初始化文件
├── base_strategy.py            # 基础策略类
├── moving_average_strategy.py  # 移动平均线策略
├── rsi_strategy.py            # RSI策略
├── bollinger_bands_strategy.py # 布林带策略
├── macd_strategy.py           # MACD策略
├── buy_hold_strategy.py       # Buy & Hold策略
├── data_loader.py             # 数据加载工具
├── backtest_utils.py          # 回测工具
├── example_usage.py           # 使用示例
└── README.md                  # 说明文档
```

## 依赖包

- backtrader: 回测框架
- pandas: 数据处理
- numpy: 数值计算
- yfinance: 数据获取
- matplotlib: 图表绘制

## 注意事项

1. 所有策略都继承自BaseStrategy，确保统一的接口
2. 数据格式必须符合OHLCV标准（Open, High, Low, Close, Volume）
3. 参数优化可能需要较长时间，建议先用小范围测试
4. 回测结果仅供参考，实际交易需要考虑更多因素

## 扩展开发

要添加新的策略，只需：
1. 继承BaseStrategy类
2. 实现next()方法
3. 在__init__.py中导入新策略
4. 添加到__all__列表中
