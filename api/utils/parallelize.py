from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def process_map(func, iterable, max_workers=None):
    """
    Applies a function to each item in an iterable using multiple processes.

    Args:
        func (callable): The function to apply to each item.
        iterable (iterable): An iterable of items to process.
        max_workers (int, optional): The maximum number of worker processes to use.
                                     Defaults to the number of processors on the machine.

    Returns:
        list: A list of results from applying the function to each item.
    """
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(func, iterable))
    return results


def thread_map(func, iterable, max_workers=None):
    """
    Applies a function to each item in an iterable using multiple threads.

    Args:
        func (callable): The function to apply to each item.
        iterable (iterable): An iterable of items to process.
        max_workers (int, optional): The maximum number of worker processes to use.
                                     Defaults to the number of processors on the machine.

    Returns:
        list: A list of results from applying the function to each item.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(func, iterable))
    return results
