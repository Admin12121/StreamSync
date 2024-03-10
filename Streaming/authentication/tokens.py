from django.contrib.auth.tokens import PasswordResetTokenGenerator

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (
        str(user.pk) + str(timestamp) 
        # text_type(user.profile.signup_confirmation)
        )

generate_token = TokenGenerator()