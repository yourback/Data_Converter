# 字转化为int - check
def word_num(word, check):
    # 最高位为1  负数处理
    if int(word[0], 16) >= 8:
        # 现将除了第一位转换为数字

        # 转换为10进制数字
        result = int(word, 16)

        # 转化为源码 （按位取反后 + 1）
        result = ~result & 0xffff
        result += 1
        result = -result
    else:
        # 正数 原反补都相同
        result = int(word, 16)

    result -= int(check, 16)

    return result / 100


# 字节转化为int - check
def byte_num(byte, check):
    result = 0
    # 最高位为1  负数处理
    if int(byte[0], 16) >= 8:
        # 现将除了第一位转换为数字

        # 转换为10进制数字
        result = int(byte, 16)

        # 转化为源码 （按位取反后 + 1）
        result = ~result & 0xff
        result += 1
        result = -result
    else:
        # 正数 原反补都相同
        result = int(byte, 16)

    result -= int(check, 16)
    return result
