from ..loop import loop as _loop


def run_callback(callback, too_few_args_error_msg, *args, **kwargs):
    # check if callback takes in the required number of arguments
    if len(callback.__code__.co_varnames) == len(args) + len(kwargs):
        _loop.create_task(callback(*args, **kwargs))
    else:
        raise ValueError(too_few_args_error_msg)

async def run_async_callback(callback, too_few_args_error_msg, *args, **kwargs):
    # check if callback takes in the required number of arguments
    if len(callback.__code__.co_varnames) == len(args) + len(kwargs):
        await callback(*args, **kwargs)
    else:
        raise ValueError(too_few_args_error_msg)