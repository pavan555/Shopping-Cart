from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        import core.signals.handler  # Importing signal handlers to ensure they are registered
