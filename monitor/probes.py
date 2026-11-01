import socket
import time
from datetime import datetime, timezone

def tcp_probe(host: str, port: int, timeout: float =3.0 ) -> dict:
    """TCP Connect probe, NOT an icmp ping or bandwidth isp est"""
    start = time.perf_counter()
    try: 
        with socket.create_connection((host, port), timeout= timeout):
            pass
        latency_ms = round((time.perf_counter()- start) * 1000, 2)
        return {'timestamp': datetime.now(timezone.utc).isoformat(),
                'host':host, 'port': port, 'ok': True,
                'connect_ms': latency_ms, 'error': None}
    except OSError as exc:
        return {'timestamp': datetime.now(timezone.utc).isoformat(),
                'host': host, 'port': port, 'ok': False,
                'connect_ms': None, 'error': type(exc).__name__ + ': ' + str(exc)[:150]}

def calculate_stats(rows: list[dict]) -> dict:
        n = len(rows)
        successes = [r for r in rows if r['ok']]
        latencies = [r['connect_ms'] for r in successes if r['connect_ms'] is not None]
        return {'samples': n, 'successful': len(successes),
            'observed_success_pct': round(100 * len(successes) / n, 2) if n else None,
            'avg_tcp_connect_ms': round(sum(latencies) / len(latencies), 2) if latencies else None}