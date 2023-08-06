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

import grpc

from grakn.service.Session.util.enums import ValueType   # user-facing ValueType enum

from grakn.service.Session.util.RequestBuilder import RequestBuilder, QueryOptions
from grakn.service.Session.util.enums import TxType as _TxType
from grakn.service.Keyspace.KeyspaceService import KeyspaceService
from grakn.service.Session.TransactionService import TransactionService
from grakn_protocol.session.Session_pb2_grpc import SessionServiceStub
from grakn.exception.GraknError import GraknError


class GraknClient(object):
    """ A client/representation of a Grakn instance"""

    def __init__(self, uri, credentials=None):
        self.uri = uri
        self.credentials = credentials
        self._channel = grpc.insecure_channel(uri)
        self._keyspace_service = KeyspaceService(self.uri, self._channel, credentials)

    def session(self, keyspace):
        """ Open a session for a specific  keyspace. Can be used as `with Grakn('localhost:48555').session(keyspace='test') as session: ... ` or as normal assignment"""
        return Session(self.uri, keyspace, self._channel, self.credentials)
    session.__annotations__ = {'keyspace': str}

    def keyspaces(self):
        return self._keyspace_service

    def close(self):
        self._channel.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()
        if tb is None:
            # No exception
            pass
        else:
            #print("Closing Client due to exception: {0} \n traceback: \n {1}".format(type, tb))
            return False


class Session(object):
    """ A session for a Grakn instance and a specific keyspace """

    def __init__(self, uri, keyspace, channel, credentials):

        if not isinstance(uri, str):
            raise TypeError('expected string for uri')

        if not isinstance(keyspace, str):
            raise TypeError('expected string for keyspace')

        self.keyspace = keyspace
        self.uri = uri
        self.credentials = credentials

        self._stub = SessionServiceStub(channel)
        self._closed = False

        try:
            open_session_response = self._stub.open(RequestBuilder.open_session(keyspace, self.credentials))
            self.session_id = open_session_response.sessionId
        except Exception as e:
            raise GraknError('Could not obtain sessionId for keyspace "{0}", stems from: {1}'.format(keyspace, e))

    __init__.__annotations__ = {'uri': str, 'keyspace': str}

    def transaction(self):
        """ Build a read or write transaction to Grakn on this keyspace (ie. session.transaction().read() or .write()) """
        if self._closed:
            raise GraknError("Session is closed")

        # create a transaction service which hides GRPC usage
        return TransactionBuilder(self.session_id, self._stub.transaction)

    def close(self):
        """ Close this keyspace session """
        close_session_req = RequestBuilder.close_session(self.session_id)
        self._stub.close(close_session_req)
        self._closed = True

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()
        if tb is None:
            # No exception
            pass
        else:
            #print("Closing Session due to exception: {0} \n traceback: \n {1}".format(type, tb))
            return False


class TransactionBuilder(object):
    def __init__(self, session_id, transaction_rpc_constructor):
        self._session_id = session_id
        self._transaction_rpc_constructor = transaction_rpc_constructor

    def read(self):
        transaction_service = TransactionService(self._session_id, _TxType.READ, self._transaction_rpc_constructor)
        return Transaction(transaction_service)

    def write(self):
        transaction_service = TransactionService(self._session_id, _TxType.WRITE, self._transaction_rpc_constructor)
        return Transaction(transaction_service)


class Transaction(object):
    """ Presents the Grakn interface to the user, actual work with GRPC happens in TransactionService """

    Options = QueryOptions

    def __init__(self, transaction_service):
        self._tx_service = transaction_service
    __init__.__annotations__ = {'transaction_service': TransactionService}

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        self.close()
        if tb is None:
            # No exception
            pass
        else:
            #print("Closing Transaction due to exception: {0} \n traceback: \n {1}".format(type, tb))
            return False

    def query(self, query, infer=Options.SERVER_DEFAULT, explain=Options.SERVER_DEFAULT, batch_size=Options.SERVER_DEFAULT):
        """ Execute a Graql query with query options"""
        return self._tx_service.query(query, infer, explain, batch_size)
    query.__annotations__ = {'query': str}

    def commit(self):
        """ Commit and close this transaction, persisting changes to Grakn """
        self._tx_service.commit()
        self.close()

    def close(self):
        """ Close this transaction without committing """
        self._tx_service.close() # close the service

    def is_open(self):
        """ Check if this transaction is open"""
        return not self._tx_service.is_closed()

    def get_concept(self, concept_id):
        """ Retrieve a concept by Concept ID (string) """
        return self._tx_service.get_concept(concept_id)
    get_concept.__annotations__ = {'concept_id': str}

    def get_schema_concept(self, label):
        """ Retrieve a schema concept by its label (eg. those defined using `define` or tx.put...() """
        return self._tx_service.get_schema_concept(label)
    get_schema_concept.__annotations__ = {'label': str}

    def get_attributes_by_value(self, attribute_value, value_type):
        """ Retrieve atttributes with a specific value and value type

        :param any attribute_value: the value to match
        :param grakn.ValueType value_type: The value type of the value in Grakn, as given by the grakn.ValueType enum
        """
        return self._tx_service.get_attributes_by_value(attribute_value, value_type)

    def put_entity_type(self, label):
        """ Define a new entity type with the given label """
        return self._tx_service.put_entity_type(label)
    put_entity_type.__annotations__ = {'label': str}

    def put_relation_type(self, label):
        """ Define a new relation type with the given label """
        return self._tx_service.put_relation_type(label)
    put_relation_type.__annotations__ = {'label': str}

    def put_attribute_type(self, label, value_type):
        """ Define a new attribute type with the given label and value type

        :param str label: the label of the attribute type
        :param grakn.ValueType value_type: the data type of the value to be stored, as given by the grakn.ValueType enum
        """
        return self._tx_service.put_attribute_type(label, value_type)
    put_attribute_type.__annotations__ = {'label': str}

    def put_role(self, label):
        """ Define a role with the given label """
        return self._tx_service.put_role(label)
    put_role.__annotations__ = {'label': str}

    def put_rule(self, label, when, then):
        """ Define a new rule with the given label, when and then clauses """
        return self._tx_service.put_rule(label, when, then)
    put_rule.__annotations__ = {'label': str, 'when': str, 'then': str}
