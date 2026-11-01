from monitor.probes import calculate_stats, tcp_probe
from monitor.storage import initialize, insert, latest

def test_summary_empty():
    assert calculate_stats([])['observed_success_pct'] is None

def test_summary_math():
    rows=[{'ok':True,'connect_ms':10.0},{'ok':False,'connect_ms':None}]
    assert calculate_stats(rows)['observed_success_pct']==50
    assert calculate_stats(rows)['avg_tcp_connect_ms']==10

def test_storage_roundtrip(tmp_path):
    db=str(tmp_path/'test.db')
    initialize(db)
    insert(db,{'timestamp':'2026-10-31T10:00:00+00:00','host':'example.test','port':443,'ok':True,'connect_ms':12,'error':None})
    assert latest(db)[0]['ok'] is True
    assert latest(db)[0]['connect_ms']==12

def test_tcp_probe_failure():
    # Localhost unbound port may fail; no real internet dependency.
    result=tcp_probe('127.0.0.1', 0, timeout=.1)
    assert result['ok'] is False
