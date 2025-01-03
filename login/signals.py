from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from .models import UserProfile
from datetime import datetime

@receiver(post_save, sender=SocialAccount)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update UserProfile when a user logs in via Google.
    """
    user = instance.user

    # Parse birthday if present
    birthday_str = instance.extra_data.get('birthday', '')
    try:
        birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date() if birthday_str else None
    except ValueError:
        birthday = None

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.picture = instance.get_avatar_url()
    user_profile.google_email = instance.extra_data.get('email', '')
    user_profile.google_name = instance.extra_data.get('name', '')
    user_profile.google_locale = instance.extra_data.get('locale', '')
    user_profile.google_gender = instance.extra_data.get('gender', '')
    user_profile.time_zone = instance.extra_data.get('time_zone', '')
    user_profile.birthday = birthday
    user_profile.save()
