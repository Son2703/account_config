#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Company: MobioVN
    Date created: 2023/02/28
"""
from mobio.sdks.base.apis.check_service import checking_service_mod

from src.apis import app

from src.controllers.merchant import merchant_url
from src.controllers.root import root_url
from src.controllers.user import user_url

v1_0_prefix = '/api/v1.0'

app.register_blueprint(checking_service_mod, url_prefix=v1_0_prefix)
app.register_blueprint(merchant_url, url_prefix=f'{v1_0_prefix}/merchants')
app.register_blueprint(root_url, url_prefix=v1_0_prefix)
app.register_blueprint(user_url, url_prefix=f'{v1_0_prefix}/users')