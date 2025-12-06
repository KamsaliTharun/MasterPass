from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"




# from django.apps import AppConfig

# class AccountsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'accounts'

#     def ready(self):
#         try:
#             # Import here, so apps are fully loaded
#             from django.contrib.auth import get_user_model
#             User = get_user_model()

#             # Create superuser only if it doesn't exist
#             if not User.objects.filter(username='admin').exists():
#                 User.objects.create_superuser(
#                     username='Tharun',
#                     # email='admin@example.com',
#                     email='Tharun@masterpass.com',
#                     password='Light#2020'
#                 )
#         except Exception:
#             # Ignore errors during first migrations
#             pass
