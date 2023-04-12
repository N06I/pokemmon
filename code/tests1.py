d = {
    'a': {
        'b': {
            'b1': {},
            'b2': {}
        },
        'c': {
            'c1': {}
        }
    }
}


def paths(curr, path=[]):
    for child, dikt in curr.items():
        path.append(child)
        yield path
        yield from paths(dikt)
        path.pop()


def iterate(dikt, path=[], paths=[]):
    for child, cdikt in dikt.items():
        path.append(child)
        paths.append(path.copy())
        iterate(cdikt)
        path.pop()
    return paths


for path in iterate(d):
    print(path)


#
# for path in paths(d):
#     if path[-1] == "c1":
#         print(path)
#         break
# #
# for path in iterate(d):
#     if path[-1] == "c1":
#         print(path)
#         break




