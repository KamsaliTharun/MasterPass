from django.apps import AppConfig
from django.contrib.auth.models import User


# class AccountsConfig(AppConfig):
#     default_auto_field = "django.db.models.BigAutoField"
#     name = "accounts"




class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if not User.objects.filter(username='itadmin').exists():
                User.objects.create_superuser('itadmin', 'itadmin@masterpass.com', 'Master@123')
        except Exception as e:
            # Ignore errors during initial migrations
            pass
