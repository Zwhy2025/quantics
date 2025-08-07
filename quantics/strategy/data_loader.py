"""
数据加载工具

提供统一的数据加载和预处理功能，支持：
- 从yfinance获取数据
- 本地缓存管理
- 数据格式标准化
"""

import os
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import backtrader as bt


class DataLoader:
    """
    数据加载工具类
    
    提供统一的数据加载和预处理功能：
    - 从yfinance获取历史数据
    - 本地缓存管理，避免重复下载
    - 数据格式标准化，确保符合Backtrader要求
    - 数据验证和修复
    """
    
    def __init__(self, cache_dir="data_cache"):
        """
        初始化数据加载器
        
        参数：
        - cache_dir: 缓存目录，默认为"data_cache"
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def load_stock_data(self, ticker_symbol, start_date, end_date, use_cache=True):
        """
        加载股票数据
        
        参数：
        - ticker_symbol: 股票代码，如'002745.SZ'
        - start_date: 开始日期，格式'YYYY-MM-DD'
        - end_date: 结束日期，格式'YYYY-MM-DD'
        - use_cache: 是否使用缓存，默认True
        
        返回：
        - pandas.DataFrame: 标准格式的股票数据
        """
        # 本地缓存文件名
        cache_file = os.path.join(
            self.cache_dir, 
            f"{ticker_symbol}_{start_date.replace('-', '')}_{end_date.replace('-', '')}_data.csv"
        )
        
        # 优先加载本地数据
        if use_cache and os.path.exists(cache_file):
            print(f"从本地缓存加载数据: {cache_file}")
            try:
                # 读取原始文件，跳过前3行元数据
                df_tmp = pd.read_csv(cache_file, skiprows=3, index_col=0, parse_dates=True)
                
                # 重命名列名，使其符合标准格式
                df_tmp.columns = ['Close', 'High', 'Low', 'Open', 'Volume']
                
                # 重新排列列的顺序，使其符合OHLCV标准格式
                stock_data = df_tmp[['Open', 'High', 'Low', 'Close', 'Volume']]
                
                print("数据格式修复完成")
                
            except Exception as e:
                print(f"修复数据格式时出错: {e}")
                print("尝试原始读取方式...")
                # 如果修复失败，尝试原始读取方式
                df_tmp = pd.read_csv(cache_file)
                if 'Date' in df_tmp.columns:
                    df_tmp['Date'] = pd.to_datetime(df_tmp['Date'])
                    df_tmp.set_index('Date', inplace=True)
                stock_data = df_tmp
        else:
            print("从远端拉取数据...")
            stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
            
            if use_cache:
                stock_data.to_csv(cache_file)
                print(f"数据已缓存到: {cache_file}")
        
        # 数据验证和修复
        stock_data = self._validate_and_fix_data(stock_data)
        
        print(f"获取到{ticker_symbol}从{start_date}到{end_date}的数据，共{len(stock_data)}个交易日")
        print("数据列名:", stock_data.columns.tolist())
        print("数据类型:")
        print(stock_data.dtypes)
        print("\n前5行数据:")
        print(stock_data.head())
        
        return stock_data
    
    def _validate_and_fix_data(self, stock_data):
        """
        验证和修复数据格式
        
        参数：
        - stock_data: 原始股票数据
        
        返回：
        - pandas.DataFrame: 修复后的标准格式数据
        """
        # 确保数据类型正确
        stock_data['Volume'] = stock_data['Volume'].astype(int)
        stock_data[['Open', 'High', 'Low', 'Close']] = stock_data[['Open', 'High', 'Low', 'Close']].astype(float)
        
        # 验证数据格式是否正确
        print("\n数据验证:")
        print(f"索引类型: {type(stock_data.index)}")
        print(f"索引前5个值: {stock_data.index[:5]}")
        print(f"数值列是否都是数值类型: {stock_data.select_dtypes(include=[np.number]).columns.tolist()}")
        print(f"Volume列是否都是整数: {stock_data['Volume'].dtype}")
        
        print("\n修复后的数据类型:")
        print(stock_data.dtypes)
        
        return stock_data
    
    def create_bt_data_feed(self, stock_data, start_date=None, end_date=None):
        """
        创建Backtrader数据源
        
        参数：
        - stock_data: pandas DataFrame格式的股票数据
        - start_date: 开始日期，可选
        - end_date: 结束日期，可选
        
        返回：
        - bt.feeds.PandasData: Backtrader数据源对象
        """
        if start_date and end_date:
            return bt.feeds.PandasData(
                dataname=stock_data,
                fromdate=datetime.strptime(start_date, '%Y-%m-%d'),
                todate=datetime.strptime(end_date, '%Y-%m-%d')
            )
        else:
            return bt.feeds.PandasData(dataname=stock_data)
    
    def save_data_to_csv(self, stock_data, filename):
        """
        保存数据到CSV文件
        
        参数：
        - stock_data: 股票数据
        - filename: 文件名
        """
        stock_data.to_csv(filename)
        print(f"数据已保存到: {filename}")
    
    def get_data_info(self, stock_data):
        """
        获取数据基本信息
        
        参数：
        - stock_data: 股票数据
        
        返回：
        - dict: 数据信息字典
        """
        info = {
            '数据行数': len(stock_data),
            '开始日期': stock_data.index[0].strftime('%Y-%m-%d'),
            '结束日期': stock_data.index[-1].strftime('%Y-%m-%d'),
            '数据列': list(stock_data.columns),
            '数据类型': stock_data.dtypes.to_dict(),
            '缺失值': stock_data.isnull().sum().to_dict(),
            '价格范围': {
                'Open': (stock_data['Open'].min(), stock_data['Open'].max()),
                'High': (stock_data['High'].min(), stock_data['High'].max()),
                'Low': (stock_data['Low'].min(), stock_data['Low'].max()),
                'Close': (stock_data['Close'].min(), stock_data['Close'].max()),
            }
        }
        return info
