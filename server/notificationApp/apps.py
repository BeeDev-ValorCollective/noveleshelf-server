from django.apps import AppConfig


class NotificationappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notificationApp'

    def ready(self):
        import notificationApp.signals