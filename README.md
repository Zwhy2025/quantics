# 量化交易策略回测与优化框架

本项目提供了一个用于量化交易策略回测、比较和参数优化的框架。它集成了数据加载、多种经典策略实现以及详细的回测分析功能，旨在帮助用户快速评估和改进交易策略。

## 主要功能

*   支持多种股票数据加载（通过 `yfinance`）。
*   实现多种经典量化交易策略（移动平均线交叉、RSI、布林带、MACD、买入并持有）。
*   提供详细的回测指标（夏普比率、最大回撤、年化收益、总收益、胜率、盈亏比等）。
*   支持策略性能比较。
*   支持策略参数网格搜索优化。
*   提供 Jupyter Notebook 演示，方便交互式学习和使用。

## 安装

1.  **克隆仓库:**
    ```bash
    git clone https://github.com/your-username/quantics.git
    ```
    (请将 `your-username` 替换为实际的 GitHub 用户名和仓库名)
2.  **进入项目目录:**
    ```bash
    cd quantics
    ```
3.  **安装依赖:**
    ```bash
    pip install -r requirements.txt
    ```

## 使用

### Jupyter Notebook 演示

推荐通过 `jupyter/strategy.ipynb` 进行交互式学习和使用。

1.  **启动 Jupyter Lab/Notebook:**
    ```bash
    jupyter lab
    # 或者
    jupyter notebook
    ```
2.  打开 `jupyter/strategy.ipynb` 文件，并按照 Notebook 中的步骤运行代码单元格。

### 命令行运行示例

您也可以直接运行 `example_usage.py` 脚本来查看一个简单的策略回测示例：

```bash
python quantics/strategy/example_usage.py
```

## 项目结构

*   `jupyter/`: 包含 Jupyter Notebook 演示文件和数据缓存。
*   `papers/`: 存放相关研究论文。
*   `quantics/`: 核心代码目录。
    *   `quantics/strategy/`: 包含策略实现、回测工具和数据加载器。
        *   `base_strategy.py`: 策略基类。
        *   `data_loader.py`: 数据加载模块。
        *   `backtest_utils.py`: 回测工具类。
        *   `moving_average_strategy.py`: 移动平均线交叉策略。
        *   `rsi_strategy.py`: RSI 策略。
        *   `bollinger_bands_strategy.py`: 布林带策略。
        *   `macd_strategy.py`: MACD 策略。
        *   `buy_hold_strategy.py`: 买入并持有策略。
        *   `example_usage.py`: 示例用法脚本。

## 贡献

欢迎对本项目进行贡献！如果您有任何改进建议、新功能或 Bug 修复，请遵循以下步骤：

1.  Fork 本仓库。
2.  创建新的分支 (`git checkout -b feature/YourFeature`)。
3.  提交您的更改 (`git commit -m 'feat: Add new feature'`)。
4.  推送到远程仓库 (`git push origin feature/YourFeature`)。
5.  提交 Pull Request。

## 许可证

(此处可以添加您的项目许可证信息，例如 MIT License, Apache License 2.0 等)