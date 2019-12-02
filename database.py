from playhouse.sqlite_ext import SqliteExtDatabase

db = SqliteExtDatabase('db_techpage.db', pragmas=(
    ('cache_size', -1024 * 64),  # 64MB page-cache.
    ('journal_mode', 'wal'),  
    ('foreign_keys', 1)))  