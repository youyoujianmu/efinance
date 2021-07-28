import pandas as pd
import re
from typing import Union, Callable
from functools import wraps
import pandas as pd


def to_numeric(func: Callable) -> Union[pd.DataFrame, pd.Series]:
    """
    将 DataFrame 或者 Series 尽可能地转为数字的装饰器

    Parameters
    ----------
    func : Callable
        返回结果为 DataFrame 或者 Series 的函数

    Returns
    -------
    Union[pd.DataFrame, pd.Series]

    """

    ignore = ['股票代码', '基金代码', '代码', '市场类型']

    @wraps(func)
    def run(*args, **kwargs):
        values = func(*args, **kwargs)
        if isinstance(values, pd.DataFrame):
            for column in values.columns:
                if column not in ignore:

                    values[column] = values[column].apply(convert)
        elif isinstance(values, pd.Series):
            for index in values.index:
                if index not in ignore:

                    values[index] = convert(values[index])
        return values

    def convert(o: Union[str, int, float]) -> Union[str, float, int]:
        if not re.findall('\d', str(o)):
            return o
        try:
            o = float(o)
        except:
            pass
        return o
    return run
