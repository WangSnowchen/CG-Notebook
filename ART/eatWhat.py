import random
from datetime import datetime

# 饭店列表
restaurants = [
    "饭店A",
    "饭店B",
    "饭店C",
    "饭店D",
    "饭店E",
    # ... 添加更多的饭店
]

# 记录上次选择的日期和饭店
last_choice = None

def get_random_restaurant():
    """
    从饭店列表中随机选择一家饭店，确保每天不重复。
    """
    global last_choice
    today = datetime.now().date()
    if last_choice and last_choice[0] == today:
        print("昨天选择了 " + last_choice[1] + "，今天尝试另一家。")
        # 如果是同一天，重新选择
        last_choice = (today, random.choice(restaurants))
    else:
        # 记录今天的选择
        last_choice = (today, random.choice(restaurants))
    
    return last_choice[1]

# 示例：每天运行这个函数来获取随机饭店
if __name__ == "__main__":
    print("今天的随机饭店是：", get_random_restaurant())