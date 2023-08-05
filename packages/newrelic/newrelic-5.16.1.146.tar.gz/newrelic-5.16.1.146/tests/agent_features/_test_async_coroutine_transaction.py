# Copyright 2010 New Relic, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio

from newrelic.api.transaction import current_transaction

loop = asyncio.get_event_loop()


def native_coroutine_test(transaction, nr_enabled=True, does_hang=False,
        call_exit=False, runtime_error=False):
    @transaction
    async def task():
        txn = current_transaction()

        if not nr_enabled:
            assert txn is None

        if call_exit:
            txn.__exit__(None, None, None)
        else:
            assert current_transaction() is txn

        try:
            if does_hang:
                await loop.create_future()
            else:
                await asyncio.sleep(0.0)
        except GeneratorExit:
            if runtime_error:
                await asyncio.sleep(0.0)

    return task
