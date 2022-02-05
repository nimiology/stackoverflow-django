from rest_framework.exceptions import ValidationError

from users.models import Company


def GetCompany(profile):
    try:
        company = profile.company
        return company
    except Company.DoesNotExist:
        raise ValidationError('There is no company on this profile')
