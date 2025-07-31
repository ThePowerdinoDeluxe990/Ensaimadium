def linespace(font):
    metrics = font.getMetrics()
    return metrics.fDescent - metrics.fAscent
