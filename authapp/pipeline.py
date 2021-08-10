from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
from geekshop import settings


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != "vk-oauth2":
        return

    api_url = urlunparse(
        (
            "https",
            "api.vk.com",
            "/method/users.get",
            None,
            urlencode(
                OrderedDict(fields=",".join(("bdate", "sex", "about", "photo_max_orig")), access_token=response["access_token"], v="5.92")
            ),
            None,
        )
    )

    # api_url = f'https://api.vk.com/method/users.get/?fields=bdate,sex,about&access_token={response["access_token"]}&v=5.92'

    # api_url = f'{settings.VK_API_URL}method/users.get/'
    #
    # params = {
    #     "fields" : "bdate,sex,about",
    #     "access_token" : response["access_token"],
    #     "v" : "5.92"
    # }
    #
    # requests.get(api_url, params=params)

    response = requests.get(api_url)
    if response.status_code != 200:
        return

    data = response.json()["response"][0]
    if data["sex"]:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data["sex"] == 2 else ShopUserProfile.FEMALE

    if 'photo_max_orig' in data:
        photo_content = requests.get(data['photo_max_orig'])
        with open(f'{settings.MEDIA_ROOT}/users_avatars/{user.pk}.jpg', 'wb') as photo_file:
            photo_file.write(photo_content.content)
            user.avatar = f'users_avatars/{user.pk}.jpg'

    if data["about"]:
        user.shopuserprofile.aboutMe = data["about"]

    if data["bdate"]:
        bdate = datetime.strptime(data["bdate"], "%d.%m.%Y").date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden("social_core.backends.vk.VKOAuth2")

    user.save()