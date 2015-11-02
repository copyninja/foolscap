import pickle

class ThisIsActuallyAFurlFileError(Exception):
    pass

def get_events(fn, ignore_value_error=False):
    if fn.endswith(".bz2"):
        import bz2
        f = bz2.BZ2File(fn, "r")
    else:
        f = open(fn, "rb")

    with f:
        while True:
            try:
                e = pickle.load(f)
                yield e
            except EOFError:
                break
            except ValueError:
                if ignore_value_error:
                    break
                raise
            except IndexError:
                # this happens when you point "flogtool dump" at a furl by
                # mistake (which cannot be parsed as a pickle). Emit a useful
                # error message.
                f.seek(0)
                if f.read(3) == "pb:":
                    raise ThisIsActuallyAFurlFileError
