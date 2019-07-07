import inspect

#inspired by:
#https://stackoverflow.com/questions/5432964/is-it-somehow-possible-to-live-modify-python-code-like-in-lisp-or-erlang#comment6159803_5436556

def patchClass(old, new):
    print 'patching class', old, new
    for key in old.__dict__.keys():
        if key not in new.__dict__:
            print 'removing', old, key
            del old.__dict__[key]
    for key, value in new.__dict__.iteritems():
        print 'patching', old, key, value
        if key not in old.__dict__:
            old.__dict__[key] = value
        if inspect.isclass(old.__dict__[key]):
            patchClass(old.__dict__[key], value)
        elif inspect.isfunction(old.__dict__[key]):
            patchFunction(old.__dict__[key], value)
        else:
            old.__dict__[key] = value
    return old

def patchFunction(old, new):
    print 'patching function', old, new
    old.func_code = new.func_code
    return old

def patch(m):
    old = m.__dict__.copy()
    reload(m)
    new = m.__dict__
    for key in old:
        if key in new:
            if inspect.isclass(old[key]):
                new[key] = patchClass(old[key], new[key])
            elif inspect.isfunction(old[key]):
                new[key] = patchFunction(old[key], new[key])
