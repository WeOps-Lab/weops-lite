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

import six

from blueapps.utils.request_provider import get_request, get_x_request_id

__all__ = [
    "get_request",
    "get_x_request_id",
    "ok",
    "ok_data",
    "failed",
    "failed_data",
]


def ok(message="", **options):
    result = {"result": True, "message": message, "msg": message}
    result.update(**options)
    return result


def failed(message="", **options):
    if not isinstance(message, str):
        if isinstance(message, six.string_types):
            message = message.encode("utf-8")
        message = str(message)
    result = {"result": False, "message": message, "data": {}, "msg": message}
    result.update(**options)
    return result


def failed_data(message, data, **options):
    if not isinstance(message, str):
        if isinstance(message, six.string_types):
            message = message.encode("utf-8")
        message = str(message)
    result = {"result": False, "message": message, "data": data, "msg": message}
    result.update(**options)
    return result


def ok_data(data=None, **options):
    if data is None:
        data = {}
    result = {"result": True, "message": "", "data": data, "msg": ""}
    result.update(**options)
    return result
