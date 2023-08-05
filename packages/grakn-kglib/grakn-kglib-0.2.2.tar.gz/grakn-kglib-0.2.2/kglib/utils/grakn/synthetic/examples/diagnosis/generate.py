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

import inspect

import numpy as np
from grakn.client import GraknClient

from kglib.utils.grakn.synthetic.statistics.pmf import PMF


def get_example_queries(pmf, example_id):

    variable_values = pmf.select()

    queries = [f'insert $p isa person, has example-id {example_id};',
               f'insert $doc isa person, has example-id {20000 + example_id};']

    if variable_values['Multiple Sclerosis'] is not False:
        queries.append(inspect.cleandoc(f'''match
                       $d isa disease, has name "Multiple Sclerosis";
                       $p isa person, has example-id {example_id};
                       $doc isa person, has example-id {20000 + example_id};
                       insert
                       (patient: $p, diagnosed-disease: $d, doctor: $doc) isa diagnosis;
                       $p has age {int(variable_values['Multiple Sclerosis']['age']())};'''))

    if variable_values['Diabetes Type II'] is not False:
        queries.append(inspect.cleandoc(f'''match
                       $p isa person, has example-id {example_id};
                       $d isa disease, has name "Diabetes Type II";
                       $doc isa person, has example-id {20000 + example_id};
                       insert
                       (patient: $p, diagnosed-disease: $d, doctor: $doc) isa diagnosis;
                       $p has age {int(variable_values['Diabetes Type II']['age']())};'''))

    if variable_values['Fatigue'] is not False:
        queries.append(inspect.cleandoc(f'''match
                       $p isa person, has example-id {example_id};
                       $s isa symptom, has name "Fatigue";
                       insert
                       (presented-symptom: $s, symptomatic-patient: $p) isa 
                       symptom-presentation, has severity {variable_values['Fatigue']['severity']()};'''))

    if variable_values['Blurred vision'] is not False:
        queries.append(inspect.cleandoc(f'''match
                       $p isa person, has example-id {example_id};
                       $s isa symptom, has name "Blurred vision";
                       insert
                       (presented-symptom: $s, symptomatic-patient: $p) isa 
                       symptom-presentation, has severity {variable_values['Blurred vision']['severity']()};'''))

    if variable_values['Drinking'] is not False:
        queries.append(inspect.cleandoc(f'''match
                       $p isa person, has example-id {example_id};
                       $s isa substance, has name "Alcohol";
                       insert
                       $c(consumer: $p, consumed-substance: $s) isa consumption, 
                       has units-per-week {int(variable_values['Drinking']['units-per-week']())};'''))

    if variable_values['Parent has Diabetes Type II'] is not False:
        queries.append(inspect.cleandoc(f'''match
                       $p isa person, has example-id {example_id};
                       $d isa disease, has name "Diabetes Type II";
                       insert
                       (parent: $parent, child: $p) isa parentship;
                       $parent isa person, has example-id {example_id + 10000};
                       (patient: $parent, diagnosed-disease: $d) isa diagnosis;
                       '''))

    if variable_values['Cigarettes'] is not False:
        queries.append(inspect.cleandoc(f'''match
                       $p isa person, has example-id {example_id};
                       $s isa substance, has name "Cigarettes";
                       insert
                       $c(consumer: $p, consumed-substance: $s) isa consumption, 
                       has units-per-week {int(variable_values['Cigarettes']['units-per-week']())};'''))

    return queries


def generate_example_graphs(num_examples, keyspace="diagnosis", uri="localhost:48555"):

    client = GraknClient(uri=uri)
    session = client.session(keyspace=keyspace)

    pmf_array = np.zeros([2, 2, 2, 2, 3, 2, 3], dtype=np.float)
    pmf_array[0, 1, 0, 1, 0, 0, 0] = 0.1
    pmf_array[1, 0, 1, 0, 0, 0, 0] = 0.05
    pmf_array[1, 0, 1, 0, 2, 0, 0] = 0.1
    pmf_array[0, 1, 1, 0, 0, 0, 0] = 0.05
    pmf_array[1, 0, 0, 1, 0, 0, 0] = 0.19
    pmf_array[1, 0, 0, 1, 0, 1, 0] = 0.15
    pmf_array[1, 1, 1, 1, 0, 0, 0] = 0.01
    pmf_array[0, 1, 1, 1, 0, 0, 0] = 0.05
    pmf_array[0, 1, 1, 1, 0, 0, 1] = 0.05
    pmf_array[0, 1, 1, 1, 0, 0, 2] = 0.1
    pmf_array[1, 0, 1, 1, 0, 0, 0] = 0.05
    pmf_array[1, 0, 1, 1, 2, 1, 2] = 0.1

    def normal_dist(mean, var):
        return lambda: round(np.random.normal(mean, var, 1)[0], 2)

    pmf = PMF({
        'Diabetes Type II':             [False, {'age': normal_dist(60, 10)}],
        'Multiple Sclerosis':           [False, {'age': normal_dist(30, 10)}],
        'Fatigue':                      [False, {'severity': normal_dist(0.3, 0.1)}],
        'Blurred vision':               [False, {'severity': normal_dist(0.5, 0.2)}],
        'Drinking':                     [False, {'units-per-week': normal_dist(5, 1)}, {'units-per-week': normal_dist(20, 3)}],
        'Parent has Diabetes Type II':  [False, True],
        'Cigarettes':                   [False, {'units-per-week': normal_dist(5, 1)}, {'units-per-week': normal_dist(20, 3)}],
    }, pmf_array, seed=0)

    # print(pmf.to_dataframe()) # TODO Remove pandas if this is not needed now

    for example_id in range(0, num_examples):
        tx = session.transaction().write()
        for query in get_example_queries(pmf, example_id):
            print(query)
            tx.query(query)
        tx.commit()

    session.close()
    client.close()


if __name__ == '__main__':
    generate_example_graphs(100, keyspace="diagnosis", uri="localhost:48555")
