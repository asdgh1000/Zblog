
def check_keywords(input_dict, mode='and', *key_list):
    """
    检查字典中键值是否存在
    :param input_dict: 待检测的字典
    :param mode: 可以为 'and' 或者 'or', 如果为'or'只要有一个键存在就返回True
    :param key_list: 需要检查的键值 
    :return: True/False
    """
    if not input_dict:
        raise Exception('传入的字典为空')

    if not key_list:
        raise Exception('需要至少一个键值')

    if mode == 'or':
        for key in key_list:
            if key in input_dict:
                return True
        return False

    for key in key_list:
        if key not in input_dict:
            return False
    return True
