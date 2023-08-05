#
#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.
#

from kglib.utils.grakn.object.comparable import PropertyComparable

VALUE_TYPE_NAMES = ('long', 'double', 'boolean', 'date', 'string')


class Thing(PropertyComparable):
    def __init__(self, id, type_label, base_type_label, value_type=None, value=None):
        self.id = id
        self.type_label = type_label
        self.base_type_label = base_type_label  # TODO rename to base_type in line with Client Python

        # If the thing is an attribute
        self.value_type = value_type
        self.value = value

        # TODO Make attribute a separate class
        if self.base_type_label == 'attribute':
            if self.value_type is None:
                raise ValueError('Attribute value_type must be provided')
            if self.value is None:
                raise ValueError('Attribute value must be provided')

    def __str__(self):
        string = f'<{self.type_label}, {self.id}'
        if self.base_type_label == 'attribute':
            string += f': {self.value}'
        return string + '>'

    def __repr__(self):
        return self.__str__()


def build_thing(grakn_thing, tx):

    id = grakn_thing.id
    type_label = grakn_thing.type().label()
    base_type_label = grakn_thing.as_remote(tx).base_type.replace('_TYPE', '').lower()

    assert(base_type_label in ['entity', 'relation', 'attribute'])

    if base_type_label == 'attribute':
        value_type = grakn_thing.as_remote(tx).type().value_type().name.lower()
        assert value_type in VALUE_TYPE_NAMES
        value = grakn_thing.value()

        return Thing(id, type_label, base_type_label, value_type, value)

    return Thing(id, type_label, base_type_label)
