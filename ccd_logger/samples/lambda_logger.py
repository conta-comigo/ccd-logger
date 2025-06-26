from ccd_logger import get_logger

logger = get_logger(__name__, context="lambda")
logger.info("Teste de log INFO")
logger.info("Teste de log com extra args", extra={"source_bucket": "source_bucket", "source_key": "source_key"})
logger.error("Erro simulado", extra={"cpf": "12345678900"})
