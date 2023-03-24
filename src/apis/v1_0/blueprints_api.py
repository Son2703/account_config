#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Company: MobioVN
    Date created: 2023/02/28
"""

from src.apis import app


from src.controllers.merchant import merchant_url
from src.controllers.root import root_url
from src.controllers.user_ex import user_url
from src.apis.v1_0.user_service import user_service

v1_0_prefix = '/api/v1.0'

from src.apis.v1_0.rule_service import rule_service
app.register_blueprint(rule_service, url_prefix=v1_0_prefix)


from src.apis.v1_0.merchant_rule_service import merchant_role
app.register_blueprint(merchant_role, url_prefix=v1_0_prefix)

app.register_blueprint(merchant_url, url_prefix=f'{v1_0_prefix}/merchants')
app.register_blueprint(root_url, url_prefix=v1_0_prefix)


from src.apis.v1_0.user_service import user_service

app.register_blueprint(user_service, url_prefix=v1_0_prefix)
