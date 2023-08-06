#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from enum import Enum
import grakn_protocol.session.Session_pb2 as SessionMessages
import grakn_protocol.session.Concept_pb2 as ConceptMessages


class TxType(Enum):
    READ = SessionMessages.Transaction.Type.Value('READ')
    WRITE = SessionMessages.Transaction.Type.Value('WRITE')
    BATCH = SessionMessages.Transaction.Type.Value('BATCH')
    

VALUE_TYPE_map = {}

class ValueType(Enum):
    STRING = ConceptMessages.AttributeType.VALUE_TYPE.Value('STRING')
    BOOLEAN = ConceptMessages.AttributeType.VALUE_TYPE.Value('BOOLEAN')
    INTEGER = ConceptMessages.AttributeType.VALUE_TYPE.Value('INTEGER')
    LONG = ConceptMessages.AttributeType.VALUE_TYPE.Value('LONG')
    FLOAT = ConceptMessages.AttributeType.VALUE_TYPE.Value('FLOAT')
    DOUBLE = ConceptMessages.AttributeType.VALUE_TYPE.Value('DOUBLE')
    DATETIME = ConceptMessages.AttributeType.VALUE_TYPE.Value('DATETIME')
