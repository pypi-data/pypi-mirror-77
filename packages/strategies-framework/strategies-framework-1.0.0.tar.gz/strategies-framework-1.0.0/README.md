**StrategiesManager**

# 这是一个策略回测库，支持内外盘期货历史回测跟实时回测两种模式

# 例子：
```python
from strategies_manager import StrategiesManager

# 自定义操作函数
def myAction(data):
    """
    自定义操作
    实现自己的策略
    :param data: 行情数据，字典类型
    :return:
    """
    print(data)

# 创建实例
manager = StrategiesManager()
# 注册自定义函数
manager.registAction(myAction)

# 实时数据使用
manager.runRealTime(stock_code='NYMEX_F_CL_2010', ktype='1Min')

# 历史数据回测使用
manager.runHistory(stock_code='NYMEX_F_CL_2010', startTime='2020-06-07', endTime='2020-08-17', ktype='1Min')
```
