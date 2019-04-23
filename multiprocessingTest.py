import time
import multiprocessing

def do_this_other_thing_that_may_take_too_long(duration):
    time.sleep(duration)
    return 'done after sleeping {0} seconds.'.format(duration)

pool = multiprocessing.Pool(1)
print('starting....')
res = pool.apply_async(do_this_other_thing_that_may_take_too_long, [8])

for timeout in range(1, 10):
    try:
        print('{0}: {1}'.format(duration, res.get(timeout)))
    except multiprocessing.TimeoutError:
        print('{0}: timed out'.format(duration))

print('end')