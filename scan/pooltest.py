# from multiprocessing import Pool
# import time
#
# def f(x):
#     time.sleep(1)
#     print(str(x*x))
#
# if __name__ == '__main__':
#     with Pool(processes=100) as pool:         # start 4 worker processes
#         # for i in range(1,10):
#         #     print("index: " + str(i))
#         #     pool.apply_async(f, (i,))
#
#         [pool.apply_async(f, (i,)) for i in range(1,100)]
#         time.sleep(1000)
#
#         result = pool.apply_async(f, (10,)) # evaluate "f(10)" asynchronously in a single process
#         print(result.get(timeout=3))        # prints "100" unless your computer is *very* slow
#
#         print(pool.map(f, range(10)))       # prints "[0, 1, 4,..., 81]"
#
#         it = pool.imap(f, range(10))
#         print(next(it))                     # prints "0"
#         print(next(it))                     # prints "1"
#         print(it.next(timeout=3))           # prints "4" unless your computer is *very* slow
#
#         result = pool.apply_async(time.sleep, (10,))
#         print(result.get(timeout=3))        # raises multiprocessing.TimeoutError
#
#
