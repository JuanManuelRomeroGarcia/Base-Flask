import os
import logging
from logging.handlers import RotatingFileHandler


def configure_logging(app, config):
    #print("Configuring logging...")
    #print(f"Debug mode: {app.debug}, Testing mode: {app.testing}")

    if not app.debug and not app.testing:
        log_directory = config.LOG_DIR

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        # Definir el formato del logger
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Definir los niveles de logging
        levels = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }

        # Limpiar manejadores existentes
        if app.logger.hasHandlers():
            app.logger.handlers.clear()

        # Evitar la propagación a manejadores superiores
        app.logger.propagate = False

        # Configurar manejadores para cada nivel de logging
        for level_name, level_num in levels.items():
            file_handler = RotatingFileHandler(
                os.path.join(log_directory, f'Base_{level_name.lower()}.log'),
                maxBytes=512*1024,
                backupCount=10,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(level_num)
            file_handler.addFilter(LevelSpecificLogFilter(level_num))  # Aplicar filtro
            app.logger.addHandler(file_handler)

        # Establecer el nivel de logging para la aplicación
        app.logger.setLevel(logging.DEBUG)



class LevelSpecificLogFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()
        self.level = level

    def filter(self, record):
        # Permitir sólo registros de un nivel específico
        return record.levelno == self.level
    