# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['AchievementsStateTest::test_to_json achievements_json'] = '{"code_cracker":{"id":"code_cracker","completed":false}}'
