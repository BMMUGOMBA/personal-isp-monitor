import sqlite3
from contextlib import closing

SCHEMA = 'CREATE TABLE IF NOT EXISTS measurements (\n    id INTEGER PRIMARY KEY AUTOINCREMENT,\n    timestamp TEXT NOT NULL, host TEXT NOT NULL,\n    port INTEGER NOT NULL, ok INTEGER NOT NULL,\n    connect_ms REAL, error TEXT\n);\nCREATE INDEX IF NOT EXISTS idx_measurements_timestamp ON measurements(timestamp);\n'

def initialize(path: str ) -> None:
    with closing(sqlite3.connect(path)) as conn:
        conn.executescript(SCHEMA)


def insert(path: str, record: dict) -> None:
    with closing(sqlite3.connect(path)) as conn:
        conn.execute(
            '''
            INSERT INTO measurements
            (timestamp, host, port, ok, connect_ms, error)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                record['timestamp'],
                record['host'],
                record['port'],
                int(record['ok']),
                record['connect_ms'],
                record['error']
            )
        )
        conn.commit()


def latest(path: str, limit: int = 100) -> list[dict]:
    with closing(sqlite3.connect(path)) as conn:
        conn.row_factory = sqlite3.Row
        return [dict(r) | {'ok': bool(r['ok'])} for r in conn.execute(
            'SELECT * FROM measurements ORDER BY id DESC LIMIT ?', (limit,))]        

        