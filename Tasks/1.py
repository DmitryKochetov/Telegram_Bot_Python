# Написать функцию-декоратор для кеширования значений функции
# Написать функцию seq(n)
# n = 0 ....N
# (1 + n) ** n возвращает [x1, x2, x3, , , , xn]
# 
# seq(3)
# seq(8)
# seq(100)
# seq(8)
# seq(3)
# seq(100)
# 
# 1.1 (**) с помощью декоратора-логгера создать лог функции (с замером времени выполнения функции)
# Написать функцию-декоратор для кеширования значений функции



import datetime
import time
from functools import wraps


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        wraps docs
        :param args:
        :param kwargs:
        :return:
        """
        log_msg = f'{datetime.datetime.now():%d.%m.%Y %H:%M:%S}\t'
        log_msg += f'функция: {func.__name__}\t'
        log_msg += f"параметры: {', '.join(map(str, args))}\t"
        start = time.time_ns()
        res = func(*args, **kwargs)
        finish = time.time_ns()
        log_msg += f'Время выполнения операции: {finish - start}\t'
        log_msg += f'результат: {res}\n'
        with open('log_file.log', 'a', encoding='utf-8') as fp:
            fp.write(log_msg)
        return res

    return wrapper


# def timer(func):
#     def wrapper(*args, **kwargs):
#         start = time.time_ns()
#         res = func(*args, **kwargs)
#         finish = time.time_ns()
#         print(f'Время выполнения операции: {finish - start}')
#         return res
#     return wrapper


def cacher(func):
    cach = {}

    @wraps(func)
    def wrapper(*args):
        key = args
        if key not in cach:
            cach[key] = func(*args)
        print(cach)
        return cach[key]

    return wrapper

# @timer
@logger
@cacher
def seq(n):
    """
    Функция возвращает (1 + n) ** n 
    :param n:
    :return:
    """
    time.sleep(0.00000001)
    return (1 + n) ** n 



def main():
    print(f'результат: {seq(3)}')
    print(f'результат: {seq(8)}')
    print(f'результат: {seq(12)}')
    print(f'результат: {seq(8)}')
    print(f'результат: {seq(3)}')
    print(f'результат: {seq(10)}')
    print(f'результат: {seq(8)}')
    print(f'результат: {seq(8)}')

    
if __name__ == '__main__':
    main()



# def <конструктор декоратора>(<параметры декоратора>):
#
#     def <декоратор>(<декорируемая ф-ция>):
#         def <обёртка>(*args):
#             res = <декорируемая ф-ция>(*args)
#             return res
#         return <обёртка>
#
#     return <декоратор>
