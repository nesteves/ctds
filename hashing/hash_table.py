__author__ = 'nunoe'


class SimpleHashTable(object):
    """ Basic implementation of a hash table """
    def __init__(self, bucket_num):
        self.buckets = []
        self.bucket_num = bucket_num
        for i in range(bucket_num):
            self.buckets.append([])

    def add_value(self, key, value):
        bucket = self.buckets[self.hash_value(key)]
        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value) # remember tuples are immutable, we need to replace the whole thing
                return
        bucket.append((key, value))

    def get_value(self, key):
        for k, v in self.buckets[self.hash_value(key)]:
            if k == key:
                return v
        return None

    def hash_value(self, s):
        index = ''
        for c in str(s):
            index += str(ord(c))
        return int(index) % self.bucket_num

    def __str__(self):
        res = ''
        for bucket in self.buckets:
            for k, v in bucket:
                res += str(k) + ': ' + str(v) + ', '
        return '{' + res[:-2] + '}'

if __name__ == '__main__':
    my_hash = SimpleHashTable(101)
    my_hash.add_value('Jill', 1)
    my_hash.add_value('Chris', 2)
    my_hash.add_value('Chris', 3)
    my_hash.add_value(1, 3)

    print my_hash.get_value('Jill')
    print my_hash.get_value('Chris')
    print my_hash.get_value('Non-existing key')
    print my_hash