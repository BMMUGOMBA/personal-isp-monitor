import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    database_path: str = os.getenv('DATABASE_PATH', 'measurements.db')
    host: str = os.getenv('PROBE_HOST', '1.1.1.1')
    port: int = int(os.getenv('PROBE_PORT', '443'))
    interval: float = float(os.getenv('PROBE_INTERVAL_SECONDS', '30'))
    timeout: float = float(os.getenv('PROBE_TIMEOUT_SECONDS', '3'))