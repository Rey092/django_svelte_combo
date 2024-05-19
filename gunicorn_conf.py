"""Gunicorn configuration file."""

bind = "0.0.0.0:8000"
workers = 3
accesslog = "-"
errorlog = "-"
forwarded_allow_ips = "*"
access_log_format = (
    '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)
timeout = 120
