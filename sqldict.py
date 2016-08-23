
class SqlTable(object):
    def __init__(self, db, table, keys, **kwargs):
        self._db = db
        self._table = table
        self._keys = keys
        self._names = None

    def toTuple(self, root):
        list_ = []
        for key in self._keys:
            node = root
            for subkey in key.split("/"):
                if subkey.isdigit():
                    subkey = int(subkey)
                    if -len(node) <= subkey < len(node):
                        node = node[subkey]
                    else:
                        node = None
                        break

                else:
                    node = node.get(subkey)

            list_.append(node)

        return tuple(list_)


    def insertmany(self, data, replace=False):
        list_ = []
        statement = self.insert_statement(replace)

        for item in data:
            list_.append(self.toTuple(item))

        with self._db as conn:
            conn.executemany(statement, list_)


    def insert(self, value, replace=False):
        statement = self.insert_statement(replace)
        item = self.toTuple(value)
        with self._db as conn:
            conn.execute(statement, item)


    def insert_statement(self, replace=False):
        stmt = """INSERT OR %s INTO %s (%s) values (%s);"""
        action = "REPLACE" if replace else "IGNORE"
        keys = ", ".join(self.keys)
        values = ", ".join(["?"]*len(self.keys))
        return stmt % (action, self._table, keys, values)


    @property
    def keys(self):
        if self._names is None:
            self._names = []
            for key in self._keys:
                parts = key.split("/")
                name = parts.pop()
                while name.isdigit():
                    name = parts.pop() + name

                self._names.append(name)

        return self._names



if __name__ == "__main__":
    pass
