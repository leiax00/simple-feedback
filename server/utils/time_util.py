import re
from datetime import timedelta

def parse_timedelta(time_str: str) -> timedelta:
    """
    将时间字符串（如 15m、1h30m、2d5h）转换为 timedelta 对象

    Args:
        time_str: 支持的单位标记：
            - d: 天
            - h: 小时
            - m: 分钟
            - s: 秒

    Returns:
        datetime.timedelta 对象

    Raises:
        ValueError: 输入格式错误时抛出
    """
    units = {
        'd': 'days',
        'h': 'hours',
        'm': 'minutes',
        's': 'seconds'
    }

    # 正则匹配所有时间单位（不区分大小写）
    pattern = re.compile(
        r'(?i)(\d+)\s*([dhms])'  # 匹配 "数值+单位"
    )
    matches = pattern.findall(time_str)

    if not matches:
        raise ValueError(f"无效的时间格式: {time_str}")

    # 初始化时间参数
    time_params = {}
    for value, unit in matches:
        unit = unit.lower()
        param_name = units[unit]
        time_params[param_name] = time_params.get(param_name, 0) + int(value)

    return timedelta(**time_params)
