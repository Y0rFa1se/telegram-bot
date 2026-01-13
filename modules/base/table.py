from sqlite_utils import Database


class Table:
    """
    `<<`: upsert
    `>>`: delete
    `in`: primary key exists
    `[]`: index, slice, or primary key
    `@`: LIKE search
    `^`: startswith search
    `/`: endswith search
    `%`: sample n random rows
    `~`: vacuum the database
    """

    db = None
    table = None

    @staticmethod
    def text_preproc(text):
        return text.strip().lower().replace(" ", "_")

    def __init__(
        self,
        table_name: str,
        db_name="data/db.sqlite3",
        scheme: dict = None,
        pk: str = None,
        not_null: set = None,
        defaults: dict = None,
    ):
        self.db = Database(db_name)

        if table_name in self.db.table_names():
            self.table = self.db[table_name]
        else:
            args = dict()
            if pk:
                args["pk"] = pk
            else:
                raise ValueError("Primary key must be provided.")
            if not_null:
                args["not_null"] = not_null
            if defaults:
                args["defaults"] = defaults

            self.table = self.db[table_name].create(scheme, **args)

    def __call__(self, data: dict):
        self.table.upsert(data, pk=self.table.pks[0])

    def __contains__(self, key):
        """in operator to check if primary key exists."""

        key = self.text_preproc(key)
        row = next(
            self.table.rows_where(f"{self.table.pks[0]} = ?", [key], limit=1), None
        )
        return row is not None

    def __len__(self):
        return self.table.count

    def __getitem__(self, key, order_by="rowid") -> list[dict] | dict | None:
        if isinstance(key, int):
            row = next(
                self.table.rows_where(order_by=order_by, limit=1, offset=key), None
            )
            return row if row else None

        elif isinstance(key, slice):
            start = key.start or 0
            stop = key.stop
            limit = stop - start if stop is not None else -1
            rows = list(
                self.table.rows_where(order_by=order_by, limit=limit, offset=start)
            )
            return rows if rows else None

        elif isinstance(key, str):
            key = self.text_preproc(key)
            row = next(
                self.table.rows_where(f"{self.table.pks[0]} = ?", [key], limit=1), None
            )
            return row if row else None

        raise TypeError

    def __lshift__(self, data: dict):
        """Insert or update by primary key."""

        if isinstance(data, dict):
            self.table.upsert(data, pk=self.table.pks[0])

        elif isinstance(data, (list, tuple)):
            self.table.upsert_all(data, pk=self.table.pks[0])

        return self

    def __rshift__(self, pk: str):
        """Delete by primary key."""

        if isinstance(pk, str):
            pk = self.text_preproc(pk)
            self.table.delete(pk)

        elif isinstance(pk, (list, tuple)):
            for key in pk:
                key = self.text_preproc(key)
                self.table.delete(key)

        return self

    def __matmul__(self, key: str):
        """Search by primary key using LIKE operator."""

        key = self.text_preproc(key)
        rows = self.table.rows_where(f"{self.table.pks[0]} LIKE ?", [f"%{key}%"])

        ret = []
        for row in rows:
            ret.append(row[self.table.pks[0]])
        return ret

    def __xor__(self, key: str):
        """Search by primary key starting with the key"""

        key = self.text_preproc(key)
        rows = self.table.rows_where(f"{self.table.pks[0]} LIKE ?", [f"{key}%"])

        ret = []
        for row in rows:
            ret.append(row[self.table.pks[0]])
        return ret

    def __truediv__(self, key: str):
        """Search by primary key ending with the key"""

        key = self.text_preproc(key)
        rows = self.table.rows_where(f"{self.table.pks[0]} LIKE ?", [f"%{key}"])

        ret = []
        for row in rows:
            ret.append(row[self.table.pks[0]])
        return ret

    def __mod__(self, key: int | float):
        """Sample n random rows from the table."""

        if isinstance(key, float):
            key = int(len(self) * key)

        rows = self.table.rows_where(order_by="RANDOM()", limit=max(0, key))

        ret = []
        for row in rows:
            ret.append(row[self.table.pks[0]])
        return ret

    def __invert__(self):
        """vacuum the database"""

        self.db.vacuum()
        return self
