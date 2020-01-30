import inspect


def accepts_kwarg(func, kwarg):
    """
    Determine whether the callable `func` has a signature that accepts the
    keyword argument `kwarg`
    """
    signature = inspect.signature(func)
    try:
        signature.bind_partial(**{kwarg: None})
        return True
    except TypeError:
        return False
