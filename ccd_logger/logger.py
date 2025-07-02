import logging
import sys
from pythonjsonlogger import jsonlogger
from .config import get_config

class JsonFormatterSIEM(jsonlogger.JsonFormatter):
    '''Formatter para logs em formato JSON, compatível com SIEMs.'''
    def __init__(self, context="generic", *args, **kwargs):
        fmt = "%(asctime)s %(levelname)s %(name)s %(message)s %(service)s %(environment)s"
        if context == "django":
            fmt += " %(path)s %(method)s %(status_code)s %(response_time)s %(user)s %(user_agent)s %(user_ip)s"
        elif context == "lambda":
            fmt += " %(function_name)s %(memory_limit_in_mb)s %(request_id)s"
        super().__init__(fmt, *args, **kwargs)

class CustomLoggerAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        extra = self.extra.copy()
        extra.update(kwargs.get("extra", {}))
        kwargs["extra"] = extra
        return msg, kwargs


def get_logger(name=None, context="generic", context_data=None) -> CustomLoggerAdapter:
    config = get_config()
    logger = logging.getLogger(name or config["service_name"])

    if logger.handlers:
        return CustomLoggerAdapter(logger, logger.handlers[0].formatter.extra)

    handler = logging.StreamHandler(sys.stdout)

    if config["log_format"] == "json":
        formatter = JsonFormatterSIEM(context=context)
    else:
        formatter = logging.Formatter('[%(asctime)s] %(levelname)s [%(name)s] %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(config["log_level"].upper())
    logger.propagate = False

    # Adiciona campos comuns + lambda context
    extra = {
        "service": config["service_name"],
        "environment": config["environment"],
    }

    if context == "lambda" and context_data:
        extra.update({
            "function_name": context_data.function_name,
            "memory_limit_in_mb": context_data.memory_limit_in_mb,
            "request_id": context_data.aws_request_id,
        })

    return CustomLoggerAdapter(logger, extra)
