# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2020 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import logging

from django.conf import settings
from django.contrib import auth
from django.core.cache import caches
from django.shortcuts import redirect
from django.urls import reverse
from authentication.keycloak.forms import AuthenticationForm

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

logger = logging.getLogger("component")
cache = caches["login_db"]


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_view(self, request, view, args, kwargs):
        """
        Login paas by two ways
        1. views decorated with 'login_exempt' keyword
        2. User has logged in calling auth.login
        """
        if getattr(view, "login_exempt", False):
            return None

        # 先做数据清洗再执行逻辑
        form = AuthenticationForm(request.COOKIES)
        if form.is_valid():
            bk_token = form.cleaned_data["bk_token"]
            session_key = request.session.session_key
            if session_key:
                # 确认 cookie 中的 ticket 和 cache 中的是否一致
                cache_session = cache.get(session_key)
                is_match = cache_session and bk_token == cache_session.get("bk_token")
                if is_match and request.user.is_authenticated:
                    return None

            user = auth.authenticate(request=request, bk_token=bk_token)
            if user is not None:
                auth.login(request, user)
                session_key = request.session.session_key
                if not session_key:
                    logger.info("删除了session_session_key")
                    request.session.cycle_key()
                session_key = request.session.session_key
                cache.set(session_key, {"bk_token": bk_token}, settings.LOGIN_CACHE_EXPIRED)
                # 登录成功，重新调用自身函数，即可退出
                return self.process_view(request, view, args, kwargs)

        return redirect_login(request)

    def process_response(self, request, response):
        return response


def redirect_login(request):
    return redirect(
        f'http://{request.get_host().split(":")[0]}:{settings.KEYCLOAK_SETTINGS["PORT"]}/realms/{settings.KEYCLOAK_SETTINGS["REALM_NAME"]}'
        # f'http://appdev.weops.com:8081/realms/{self._settings.KEYCLOAK_SETTINGS["REALM_NAME"]}'
        f'/protocol/openid-connect/auth'
        f'?client_id={settings.KEYCLOAK_SETTINGS["CLIENT_ID"]}'
        f'&response_type=code'
        f'&scope=openid'
        f'&redirect_uri={request.build_absolute_uri(reverse("keycloak_code_login"))}'
        # f'&redirect_uri=http://appdev.weops.com:8081{reverse("keycloak_code_login")}'
    )