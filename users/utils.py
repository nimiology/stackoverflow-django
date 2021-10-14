import jwt
from rest_framework.exceptions import ValidationError
from decouple import config

from users.models import Wallet, Company


def FindWallet(id):
    try:
        p = Wallet.objects.get(id=id)
        return p
    except Wallet.DoesNotExist:
        raise ValidationError('Profile Not Found!')


def CheckTheServiceID(token):
    if token['service'] == config('SERVICE_ID'):
        return True
    else:
        raise ValidationError('This token is not for this service')


def VerifyToken(token):
    try:
        decodedToken = jwt.decode(token, config(
            'AUTH_SECRET_KEY'), algorithms=["HS256"])
        return decodedToken
    except Exception as e:
        raise ValidationError('Token is not Valid')


def GetTokenFromHeader(request):
    if 'Authorization' in request.headers:
        return request.headers['Authorization']
    else:
        raise ValidationError('There is no Token!')


def BanCheck(profile):
    if not profile.ban:
        return profile
    else:
        raise ValidationError('This profile has been banned')


def GetWallet(request):
    token = GetTokenFromHeader(request)
    DecodedToken = VerifyToken(token)
    CheckTheServiceID(DecodedToken)
    profile = FindWallet(DecodedToken['wallet_id'])
    return BanCheck(profile)


def GetCompany(profile):
    try:
        company = profile.company
        return company
    except Company.DoesNotExist:
        raise ValidationError('There is no company on this profile')
