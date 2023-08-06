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

from grakn_protocol.keyspace.Keyspace_pb2_grpc import KeyspaceServiceStub
import grakn_protocol.keyspace.Keyspace_pb2 as keyspace_messages


class KeyspaceService(object):

    def __init__(self, uri, channel, credentials=None):
        self.uri = uri
        self.stub = KeyspaceServiceStub(channel)
        self.credentials = credentials

    def retrieve(self):
        retrieve_request = keyspace_messages.Keyspace.Retrieve.Req()
        if self.credentials:
            retrieve_request.username = self.credentials['username']
            retrieve_request.password = self.credentials['password']
        response = self.stub.retrieve(retrieve_request)
        return list(response.names)

    def delete(self, keyspace):
        delete_request = keyspace_messages.Keyspace.Delete.Req()
        delete_request.name = keyspace
        if self.credentials:
            delete_request.username = self.credentials['username']
            delete_request.password = self.credentials['password']
        self.stub.delete(delete_request)
        return
