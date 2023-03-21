#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Company: MobioVN
    Date created: 2023/02/28
"""
# from mobio.sdks.base.apis.check_service import checking_service_mod

from src.apis import app
from src.controllers.merchant_config import merchant_cf 

v1_0_prefix = '/api/v1.0'

# app.register_blueprint(checking_service_mod, url_prefix=v1_0_prefix)
app.register_blueprint(merchant_cf, url_prefix=v1_0_prefix)
