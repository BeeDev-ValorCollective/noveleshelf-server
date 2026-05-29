from django.apps import AppConfig


class CurrencyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'currencyApp'

    def ready(self):
        import currencyApp.signals