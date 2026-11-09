from prometheus_client import Counter, Gauge, Histogram

SERVICE_REQUEST_SUBMISSIONS_TOTAL = Counter(
    "service_request_submissions_total",
    "Total service request submission attempts",
    ["result"],
)

SERVICE_REQUEST_SUBMISSION_FAILURES_TOTAL = Counter(
    "service_request_submission_failures_total",
    "Total failed service request submissions",
    ["reason"],
)

SERVICE_REQUEST_SUBMISSION_DURATION_SECONDS = Histogram(
    "service_request_submission_duration_seconds",
    "Service request submission duration in seconds",
    buckets=(0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)

ACTIVE_INCIDENTS = Gauge(
    "active_incidents",
    "Number of active (non-resolved) incidents",
)

REMEDIATION_ATTEMPTS_TOTAL = Counter(
    "remediation_attempts_total",
    "Total remediation attempts",
    ["action_type"],
)

REMEDIATION_SUCCESS_TOTAL = Counter(
    "remediation_success_total",
    "Total successful remediations",
    ["action_type"],
)
