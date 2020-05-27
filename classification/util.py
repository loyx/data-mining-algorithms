""" util functions """


def csvReader(path, split=','):
    with open(path, 'r') as fp:
        for line in fp:
            yield line.strip().split(split)


def csvWriter(data: list, path, split=','):
    with open(path, 'w') as fp:
        for line in data:
            fp.write(split.join(map(str, line)) + '\n')
