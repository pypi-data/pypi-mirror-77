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

from collections import namedtuple

import newrelic.core.trace_node

from newrelic.core.node_mixin import GenericNodeMixin
from newrelic.core.metric import TimeMetric

_MemcacheNode = namedtuple('_MemcacheNode',
        ['command', 'children', 'start_time', 'end_time', 'duration',
        'exclusive', 'guid', 'agent_attributes', 'user_attributes'])


class MemcacheNode(_MemcacheNode, GenericNodeMixin):

    @property
    def name(self):
        return 'Memcache/%s' % self.command

    def time_metrics(self, stats, root, parent):
        """Return a generator yielding the timed metrics for this
        memcache node as well as all the child nodes.

        """

        yield TimeMetric(name='Memcache/all', scope='',
                duration=self.duration, exclusive=self.exclusive)

        if root.type == 'WebTransaction':
            yield TimeMetric(name='Memcache/allWeb', scope='',
                    duration=self.duration, exclusive=self.exclusive)
        else:
            yield TimeMetric(name='Memcache/allOther', scope='',
                    duration=self.duration, exclusive=self.exclusive)

        name = 'Memcache/%s' % self.command

        yield TimeMetric(name=name, scope='', duration=self.duration,
                  exclusive=self.exclusive)

        yield TimeMetric(name=name, scope=root.path,
                duration=self.duration, exclusive=self.exclusive)

    def trace_node(self, stats, root, connections):
        name = root.string_table.cache(self.name)

        start_time = newrelic.core.trace_node.node_start_time(root, self)
        end_time = newrelic.core.trace_node.node_end_time(root, self)

        children = []

        root.trace_node_count += 1

        # Agent attributes
        params = self.get_trace_segment_params(root.settings)

        return newrelic.core.trace_node.TraceNode(start_time=start_time,
                end_time=end_time, name=name, params=params, children=children,
                label=None)
