import jwt
from rest_framework.exceptions import ValidationError
from decouple import config

from users.models import Wallet


def FindWallet(id):
    try:
        p = Wallet.objects.get(id=id)
        return p
    except Wallet.DoesNotExist:
        raise ValidationError('Profile Not Found!')


def VerifyToken(token):
    try:
        tokenDecoded = jwt.decode(token, config('SECRET'), algorithms=["HS256"])
        print(tokenDecoded)
        if tokenDecoded['service'] == config('SERVICE_ID'):
            return tokenDecoded
        else:
            raise ValidationError('This token is not for this service')
    except:
        raise ValidationError('Token is not Valid')


def GetToken(request):
    if 'Authorization' in request.headers:
        return request.headers['Authorization']
    else:
        raise ValidationError('There is no Token!')


def CheckBan(profile):
    if not profile.ban:
        return profile
    else:
        raise ValidationError('This profile has been banned')


def GetWallet(request):
    token = GetToken(request)
    wallet_id = VerifyToken(token)['wallet_id']
    profile = FindWallet(wallet_id)
    return CheckBan(profile)
