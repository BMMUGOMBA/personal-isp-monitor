import argparse
import time
from .config import Settings
from .probes import tcp_probe
from .storage import initialize, insert

def run(count: int | None = None) -> None:
    s = Settings()
    initialize(s.database_path)
    n = 0
    print(f'Probing {s.host}:{s.port}; interval={s.interval}s; database={s.database_path}')
    try:
        while count is None or n < count:
            result = tcp_probe(s.host, s.port, s.timeout)
            insert(s.database_path, result)
            print(result, flush=True)
            n += 1
            if count is None or n < count:
                time.sleep(s.interval)
    except KeyboardInterrupt:
        print('Stopped')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=None, help='Optional number of probes')
    args = parser.parse_args()
    run(args.count)
