from ccd_logger import get_logger

logger = get_logger(__name__, context="django")
logger.info("Teste de log INFO")
logger.error("Erro simulado", extra={"cpf": "12345678900"})
