def is_num(in_value):
    try:
        x = int(in_value)
    except TypeError:
        return False
    except ValueError:
        return False
    except Exception as e:
        return False
    else:
        return True
