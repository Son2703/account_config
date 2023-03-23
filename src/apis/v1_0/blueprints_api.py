#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Company: MobioVN
    Date created: 2023/02/28
"""

from src.apis import app
from src.apis.v1_0.merchant_rule_service import merchant_role

from src.controllers.merchant import merchant_url
from src.controllers.root import root_url

v1_0_prefix = '/api/v1.0'

app.register_blueprint(merchant_role, url_prefix=v1_0_prefix)
app.register_blueprint(merchant_url, url_prefix=f'{v1_0_prefix}/merchants')
app.register_blueprint(root_url, url_prefix=v1_0_prefix)
