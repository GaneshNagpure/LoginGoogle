from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Extract Google user data
        google_data = sociallogin.account.extra_data
        user = sociallogin.user
        
        # Store the data in the custom UserProfile model
        if not user.pk:
            user.first_name = google_data.get('given_name', '')
            user.last_name = google_data.get('family_name', '')
            user.email = google_data.get('email', '')
            user.save()

            # Create or update the user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.picture = google_data.get('picture', '')
            profile.google_email = google_data.get('email', '')
            profile.google_name = google_data.get('name', '')
            profile.google_locale = google_data.get('locale', '')
            profile.google_gender = google_data.get('gender', '')
            profile.save()

        super().pre_social_login(request, sociallogin)
