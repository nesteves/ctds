__author__ = 'nunoe'


def int_from_str(s):
    """ Simple hashing function
    The indexes return grow bigger as the provided string grows
    :param s: str, given string
    :return: the hash value for s
    """
    index = ''
    for c in s:
        index += str(ord(c))
    return int(index)


def hash_str(s, table_size=101):
    """ A more complex hashing function
    prevents the returned index from getting bigger than the value of table_size
    :param s: str, given string to hash
    :param table_size: int, the range of different possible hash values returned by this function
    :return: the hash value for s
    """
    index = ''
    for c in s:
        index += str(ord(c))
    index = int(index) % table_size
    return index


if __name__ == '__main__':
    print('Test the simple hash function: ')
    print '\tfor a: {0}'.format(str(int_from_str('a')))
    print '\tfor Test a string: {0}'.format(str(int_from_str('Test a string.')))

    print('Test the hash function with limited values: ')
    print '\tfor a: {0}'.format(str(hash_str('a')))
    print '\tfor Test a string: {0}'.format(str(hash_str('Test a string.')))