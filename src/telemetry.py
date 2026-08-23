from prometheus_client import Counter, Histogram

BYTES_PROCESSED = Counter('adc_bytes_total', 'Total bytes compressed')
COMP_TIME = Histogram('adc_compression_seconds', 'Time spent compressing')

def record_metrics(byte_len: int, duration: float):
    BYTES_PROCESSED.inc(byte_len)
    COMP_TIME.observe(duration)
