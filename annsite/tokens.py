from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six as s

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            s.text_type(user.pk) + s.text_type(timestamp) +
            s.text_type(user.profile.email_confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()