AMOUNT_BANDS = {
    "LOW": 50000,          # < 500 INR
    "MEDIUM": 200000,      # < 2000 INR
    "HIGH": 1000000,       # < 10000 INR
    "VERY_HIGH": float('inf') # >= 10000 INR
}

TEMPORAL_BUCKETS = {
    "RETRY_SPEED": {
        "IMMEDIATE": 5,      # <= 5s
        "FAST": 15,          # <= 15s
        "NORMAL": 60,        # <= 60s
        "SLOW": float('inf') # > 60s
    },
    "WEBHOOK_LATENCY": {
        "LOW": 2,            # <= 2s
        "NORMAL": 5,         # <= 5s
        "ELEVATED": 15,      # <= 15s
        "HIGH": float('inf') # > 15s
    }
}

SEQUENCE_CONFIG = {
    "MIN_SUPPORT": 10,
    "MAX_NGRAM": 4
}

DISCOVERY_CONFIG = {
    "MIN_SUPPORT": 0.01,
    "MIN_LIFT": 1.5,
    "MIN_LOSS_COUNT": 5,
    "P_VALUE_THRESHOLD": 0.05,
    "MAX_PATTERN_SIZE": 3,
    "MAX_PATTERNS": 50,
    "STABILITY_THRESHOLD": 0.7
}
