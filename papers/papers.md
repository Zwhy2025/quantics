# 量化投资论文


# 🧱 一、经典因子与规则策略
1. **Fama and French (1993)**
   *Common risk factors in the returns on stocks and bonds*
   🔗 [https://www.sciencedirect.com/science/article/abs/pii/0304405X93900235](https://www.sciencedirect.com/science/article/abs/pii/0304405X93900235)

   > 奠定多因子模型三因子（市值、账面市值比、市场）基础，是金融界经典

2. **Jegadeesh & Titman (1993)**
   *Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency*
   🔗 [https://www.jstor.org/stable/2329112](https://www.jstor.org/stable/2329112)

   > 提出动量策略，揭示趋势跟随在实证数据中的有效性。

3. **Grinold & Kahn (1999)**
   *Active Portfolio Management*（书）

   > 虽不是论文，但是因子投资+风险控制的实战圣经，建议长期翻阅。

---

# 📊 二、因子构造与组合策略
4. **Harvey, Liu, and Zhu (2016)**
   *...and the Cross-Section of Expected Returns*
   🔗 [https://papers.ssrn.com/sol3/papers.cfm?abstract\_id=2249314](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2249314)
   📄 [本地链接](./Harvey,_Liu,_Zhu_(2016)_..._and_the_Cross-Section_of_Expected_Returns.pdf)

   > 指出很多"看似有效"的因子其实是数据挖掘结果，提出p-hacking警示。

5. **Israel & Moskowitz (2013)**
   *The Role of Shorting, Firm Size, and Time on Market Anomalies*
   🔗 [https://papers.ssrn.com/sol3/papers.cfm?abstract\_id=2288373](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2288373)

   > 分析各种因子在不同市场、时间尺度下的稳定性。

---

# 🧠 三、机器学习与量化融合

6. **Gu, Kelly & Xiu (2020)**
   *Empirical Asset Pricing via Machine Learning*
   🔗 [https://papers.ssrn.com/sol3/papers.cfm?abstract\_id=3254510](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3254510)
   📄 [本地链接](./Gu,_Kelly,_Xiu_(2020)_Empirical_Asset_Pricing_via_Machine_Learning.pdf)

   > 非常前沿的一篇论文，系统比较了神经网络 vs 传统模型在资产定价中的效果。建议必读。

7. **Kakushadze & Yu (2016)**
   *Statistical Industry Classification*
   🔗 [https://papers.ssrn.com/sol3/papers.cfm?abstract\_id=2722093](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2722093)
   📄 [本地链接](./Kakushadze,_Yu_(2016)_Statistical_Industry_Classification.pdf)

   > 介绍了如何用聚类和统计手段构建"行业"因子。

8. **Heaton, Polson, Witte (2016)**
   *Deep Learning in Finance*
   🔗 [https://arxiv.org/abs/1602.06561](https://arxiv.org/abs/1602.06561)
   📄 [本地链接](./Heaton,_Polson,_Witte_(2016)_Deep_Learning_in_Finance.pdf)

   > 早期将深度学习引入金融建模的论文之一，易读。

---

# ⚙️ 四、系统实现与代码工程

9. **Zipline Backtest Framework**
   GitHub: [https://github.com/quantopian/zipline](https://github.com/quantopian/zipline)

   > 虽不是论文，但它的代码结构是许多论文策略的基准实现。

10. **Quantitative Trading with Reinforcement Learning**
    *Deng, Bao, et al. (2016)*
    🔗 [https://arxiv.org/abs/1605.06459](https://arxiv.org/abs/1605.06459)
    📄 [本地链接](./Deng,_Bao,_et_al._(2016)_Deep_Reinforcement_Learning_in_Quantitative_Algorithmic_Trading.pdf)

    > 用强化学习构建交易策略的经典论文之一。