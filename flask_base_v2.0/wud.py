#! /usr/bin/env python
# coding:utf-8

import pickle
from Log.log import Log


def get_pickling_errors(obj, seen=None):
    if seen == None:
        seen = []
    try:
        state = obj.__getstate__()
    except AttributeError:
        return

    if state == None:
        return
    if isinstance(state,tuple):
        if not isinstance(state[0],dict):
            state = state[1]
        else:
            state = state[0].update(state[1])
    result = {}
    for i in state:
        try:
            pickle.dumps(state[i],protocol=2)
        except pickle.PicklingError:
            if not state[i] in seen:
                seen.append(state[i])
                result[i] = get_pickling_errors(state[i], seen)
    return result


if __name__ == '__main__':
    my_instance = Log()
    get_pickling_errors(my_instance)
