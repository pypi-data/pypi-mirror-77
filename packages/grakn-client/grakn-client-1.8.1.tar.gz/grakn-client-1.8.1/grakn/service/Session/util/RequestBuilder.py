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
from datetime import datetime

import grakn_protocol.session.Session_pb2 as transaction_messages
import grakn_protocol.session.Concept_pb2 as concept_messages
import grakn_protocol.session.Answer_pb2 as answer_messages
from grakn.service.Session.util import enums
from grakn.service.Session.Concept import BaseTypeMapping
from grakn.exception import GraknError

class QueryOptions(object):
    SERVER_DEFAULT = None
    BATCH_ALL = "all"

class RequestBuilder(object):
    """ Static methods for generating GRPC requests """

    @staticmethod
    def _base_iterate_with_options(batch_size):
        iter_options = transaction_messages.Transaction.Iter.Req.Options()
        if batch_size == QueryOptions.BATCH_ALL:
            iter_options.all = True
        elif type(batch_size) == int and batch_size > 0:
            iter_options.number = batch_size
        elif batch_size != QueryOptions.SERVER_DEFAULT:
            raise GraknError("batch_size parameter must either be an integer, SERVER_DEFAULT, or BATCH_ALL")

        transaction_iter_req = transaction_messages.Transaction.Iter.Req()
        transaction_iter_req.options.CopyFrom(iter_options)
        return transaction_iter_req

    @staticmethod
    def iter_req_to_tx_req(grpc_iter_req):
        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.iter_req.CopyFrom(grpc_iter_req)
        return transaction_req

    @staticmethod
    def _query_options(infer, explain):
        options_message = transaction_messages.Transaction.Query.Options()
        if infer != QueryOptions.SERVER_DEFAULT:
            if type(infer) == bool:
                options_message.inferFlag = infer
            else:
                raise GraknError("query 'infer' flag must be SERVER_DEFAULT or a boolean")
        if explain != QueryOptions.SERVER_DEFAULT:
            if type(explain) == bool:
                options_message.explainFlag = explain
            else:
                raise GraknError("query 'explain' flag must be SERVER_DEFAULT or a boolean")
        return options_message

    @staticmethod
    def start_iterating_query(query, infer, explain, batch_size):
        query_message = transaction_messages.Transaction.Query.Iter.Req()
        query_message.query = query
        query_options = RequestBuilder._query_options(infer, explain)
        query_message.options.CopyFrom(query_options)
        transaction_iter_req = RequestBuilder._base_iterate_with_options(batch_size)
        transaction_iter_req.query_iter_req.CopyFrom(query_message)
        return transaction_iter_req

    @staticmethod
    def start_iterating_concept_method(concept_id, grpc_concept_method_iter_req, batch_size=None):
        transaction_concept_method_iter_req = transaction_messages.Transaction.ConceptMethod.Iter.Req()
        transaction_concept_method_iter_req.id = concept_id
        transaction_concept_method_iter_req.method.CopyFrom(grpc_concept_method_iter_req)

        transaction_iter_req = RequestBuilder._base_iterate_with_options(batch_size)
        transaction_iter_req.conceptMethod_iter_req.CopyFrom(transaction_concept_method_iter_req)
        return transaction_iter_req

    def start_iterating_get_attributes_by_value(value, valuetype, batch_size=None):
        get_attrs_req = transaction_messages.Transaction.GetAttributes.Iter.Req()
        grpc_value_object = RequestBuilder.ConceptMethod.as_value_object(value, valuetype)
        get_attrs_req.value.CopyFrom(grpc_value_object)

        transaction_iter_req = RequestBuilder._base_iterate_with_options(batch_size)
        transaction_iter_req.getAttributes_iter_req.CopyFrom(get_attrs_req)
        return transaction_iter_req
    start_iterating_get_attributes_by_value.__annotations__ = {'valuetype': enums.ValueType}
    start_iterating_get_attributes_by_value = staticmethod(start_iterating_get_attributes_by_value)

    @staticmethod
    def continue_iterating(iterator_id, batch_options):
        transaction_iter_req = transaction_messages.Transaction.Iter.Req()
        transaction_iter_req.options.CopyFrom(batch_options)
        transaction_iter_req.iteratorId = iterator_id
        return transaction_iter_req

    @staticmethod
    def concept_method_req_to_tx_req(concept_id, grpc_concept_method_req):
        concept_method_req = transaction_messages.Transaction.ConceptMethod.Req()
        concept_method_req.id = concept_id
        concept_method_req.method.CopyFrom(grpc_concept_method_req)

        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.conceptMethod_req.CopyFrom(concept_method_req)
        return transaction_req

    # --- Top level functionality ---
    @staticmethod
    def open_tx(session_id, tx_type):
        open_request = transaction_messages.Transaction.Open.Req()
        open_request.sessionId = session_id
        open_request.type = tx_type.value

        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.open_req.CopyFrom(open_request)
        return transaction_req

    @staticmethod
    def open_session(keyspace, credentials):
        open_session_request = transaction_messages.Session.Open.Req()
        open_session_request.Keyspace = keyspace
        if credentials is not None:
            open_session_request.username = credentials['username']
            open_session_request.password = credentials['password']
        return open_session_request

    @staticmethod
    def close_session(session_id):
        close_session_request = transaction_messages.Session.Close.Req()
        close_session_request.sessionId = session_id
        return close_session_request

    @staticmethod
    def commit():
        commit_req = transaction_messages.Transaction.Commit.Req()
        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.commit_req.CopyFrom(commit_req)
        return transaction_req

    @staticmethod
    def get_concept(concept_id):
        get_concept_req = transaction_messages.Transaction.GetConcept.Req()
        get_concept_req.id = concept_id
        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.getConcept_req.CopyFrom(get_concept_req)
        return transaction_req

    @staticmethod
    def get_schema_concept(label):
        get_schema_concept_req = transaction_messages.Transaction.GetSchemaConcept.Req()
        get_schema_concept_req.label = label
        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.getSchemaConcept_req.CopyFrom(get_schema_concept_req)
        return transaction_req

    @staticmethod
    def put_entity_type(label):
        put_entity_type_req = transaction_messages.Transaction.PutEntityType.Req()
        put_entity_type_req.label = label
        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.putEntityType_req.CopyFrom(put_entity_type_req)
        return transaction_req

    @staticmethod
    def put_relation_type(label):
        put_relation_type_req = transaction_messages.Transaction.PutRelationType.Req()
        put_relation_type_req.label = label
        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.putRelationType_req.CopyFrom(put_relation_type_req)
        return transaction_req

    def put_attribute_type(label, value_type):
        put_attribute_type_req = transaction_messages.Transaction.PutAttributeType.Req()
        put_attribute_type_req.label = label
        put_attribute_type_req.valueType = value_type.value # retrieve enum value
        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.putAttributeType_req.CopyFrom(put_attribute_type_req)
        return transaction_req
    put_attribute_type.__annotations__ = {'value_type': enums.ValueType}
    put_attribute_type = staticmethod(put_attribute_type)

    @staticmethod
    def put_role(label):
        put_role_req = transaction_messages.Transaction.PutRole.Req()
        put_role_req.label = label
        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.putRole_req.CopyFrom(put_role_req)
        return transaction_req

    @staticmethod
    def put_rule(label, when, then):
        put_rule_req = transaction_messages.Transaction.PutRule.Req()
        put_rule_req.label = label
        put_rule_req.when = when
        put_rule_req.then = then
        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.putRule_req.CopyFrom(put_rule_req)
        return transaction_req

    # --- internal requests ---

    @staticmethod
    def explanation(explainable):
        concept_map = {}
        for variable, concept in explainable.map().items():
            grpc_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(concept)
            concept_map[variable] = grpc_concept

        grpc_concept_map = answer_messages.ConceptMap(map=concept_map)

        grpc_concept_map.hasExplanation = explainable.has_explanation()
        grpc_concept_map.pattern = explainable.query_pattern()

        explanation_req = answer_messages.Explanation.Req()
        explanation_req.explainable.CopyFrom(grpc_concept_map)

        transaction_req = transaction_messages.Transaction.Req()
        transaction_req.explanation_req.CopyFrom(explanation_req)

        return transaction_req

    # ------ Concept Method Requests ------

    class ConceptMethod(object):
        """ Construct Concept Method requests """

        @staticmethod
        def delete():
            delete_req = concept_messages.Concept.Delete.Req()
            concept_method_req = concept_messages.Method.Req()
            concept_method_req.concept_delete_req.CopyFrom(delete_req)
            return concept_method_req

        @staticmethod
        def _concept_to_grpc_concept(concept):
            """ Takes a concept from ConceptHierarcy and converts to GRPC message """
            grpc_concept = concept_messages.Concept()
            grpc_concept.id = concept.id
            base_type_name = concept.base_type
            grpc_base_type = BaseTypeMapping.name_to_grpc_base_type[base_type_name]
            grpc_concept.baseType = grpc_base_type
            return grpc_concept

        def as_value_object(data, valuetype):
            msg = concept_messages.ValueObject()
            if valuetype == enums.ValueType.STRING:
                msg.string = data
            elif valuetype == enums.ValueType.BOOLEAN:
                msg.boolean = data
            elif valuetype == enums.ValueType.INTEGER:
                msg.integer = data
            elif valuetype == enums.ValueType.LONG:
                msg.long = data
            elif valuetype == enums.ValueType.FLOAT:
                msg.float = data
            elif valuetype == enums.ValueType.DOUBLE:
                msg.double = data
            elif valuetype == enums.ValueType.DATETIME:
                # convert local datetime into long
                epoch = datetime(1970, 1, 1)
                diff = data - epoch
                epoch_seconds_utc = int(diff.total_seconds())
                epoch_ms_long_utc = int(epoch_seconds_utc*1000)
                msg.datetime = epoch_ms_long_utc
            else:
                # TODO specialize exception
                raise Exception("Unknown attribute valuetype: {}".format(valuetype))
            return msg
        as_value_object.__annotations__ = {'valuetype': enums.ValueType}
        as_value_object = staticmethod(as_value_object)



        class SchemaConcept(object):
            """ Generates SchemaConcept method messages """

            @staticmethod
            def get_label():
                get_schema_label_req = concept_messages.SchemaConcept.GetLabel.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.schemaConcept_getLabel_req.CopyFrom(get_schema_label_req)
                return concept_method_req
          
            @staticmethod
            def set_label(label):
                set_schema_label_req = concept_messages.SchemaConcept.SetLabel.Req()
                set_schema_label_req.label = label
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.schemaConcept_setLabel_req.CopyFrom(set_schema_label_req)
                return concept_method_req


            @staticmethod
            def get_sup():
                get_sup_req = concept_messages.SchemaConcept.GetSup.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.schemaConcept_getSup_req.CopyFrom(get_sup_req)
                return concept_method_req

            @staticmethod
            def set_sup(concept): 
                grpc_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(concept)
                set_sup_req = concept_messages.SchemaConcept.SetSup.Req()
                set_sup_req.schemaConcept.CopyFrom(grpc_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.schemaConcept_setSup_req.CopyFrom(set_sup_req)
                return concept_method_req

            @staticmethod
            def subs():
                subs_req = concept_messages.SchemaConcept.Subs.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.schemaConcept_subs_iter_req.CopyFrom(subs_req)
                return concept_method_req

            @staticmethod
            def sups():
                sups_req = concept_messages.SchemaConcept.Sups.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.schemaConcept_sups_iter_req.CopyFrom(sups_req)
                return concept_method_req

        class Rule(object):
            """ Generates Rule method messages """

            @staticmethod
            def when():
                when_req = concept_messages.Rule.When.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.rule_when_req.CopyFrom(when_req)
                return concept_method_req

            @staticmethod
            def then():
                then_req = concept_messages.Rule.Then.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.rule_then_req.CopyFrom(then_req)
                return concept_method_req

        class Role(object):
            """ Generates Role method messages """

            @staticmethod
            def relations():
                relations_req = concept_messages.Role.Relations.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.role_relations_iter_req.CopyFrom(relations_req)
                return concept_method_req

            @staticmethod
            def players():
                players_req = concept_messages.Role.Players.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.role_players_iter_req.CopyFrom(players_req)
                return concept_method_req

        class Type(object):
            """ Generates Type method messages """

            @staticmethod
            def is_abstract():
                is_abstract_req = concept_messages.Type.IsAbstract.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.type_isAbstract_req.CopyFrom(is_abstract_req)
                return concept_method_req

            @staticmethod
            def set_abstract(abstract):
                set_abstract_req = concept_messages.Type.SetAbstract.Req()
                assert type(abstract) == bool
                set_abstract_req.abstract = abstract
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.type_setAbstract_req.CopyFrom(set_abstract_req)
                return concept_method_req

            @staticmethod
            def instances():
                type_instances_req = concept_messages.Type.Instances.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.type_instances_iter_req.CopyFrom(type_instances_req)
                return concept_method_req

            @staticmethod
            def keys():
                type_keys_req = concept_messages.Type.Keys.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.type_keys_iter_req.CopyFrom(type_keys_req)
                return concept_method_req

            @staticmethod
            def attributes():
                type_attributes_req = concept_messages.Type.Attributes.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.type_attributes_iter_req.CopyFrom(type_attributes_req)
                return concept_method_req 

            @staticmethod
            def has(attribute_type_concept):
                grpc_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(attribute_type_concept)
                has_req = concept_messages.Type.Has.Req()
                has_req.attributeType.CopyFrom(grpc_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.type_has_req.CopyFrom(has_req)
                return concept_method_req

            @staticmethod
            def unhas(attribute_type_concept):
                grpc_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(attribute_type_concept)
                unhas_req = concept_messages.Type.Unhas.Req()
                unhas_req.attributeType.CopyFrom(grpc_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.type_unhas_req.CopyFrom(unhas_req)
                return concept_method_req

            @staticmethod
            def key(attribute_type_concept):
                grpc_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(attribute_type_concept)
                key_req = concept_messages.Type.Key.Req()
                key_req.attributeType.CopyFrom(grpc_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.type_key_req.CopyFrom(key_req)
                return concept_method_req

            @staticmethod
            def unkey(attribute_type_concept):
                grpc_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(attribute_type_concept)
                unkey_req = concept_messages.Type.Unkey.Req()
                unkey_req.attributeType.CopyFrom(grpc_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.type_unkey_req.CopyFrom(unkey_req)
                return concept_method_req

            @staticmethod
            def playing():
                playing_req = concept_messages.Type.Playing.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.type_playing_iter_req.CopyFrom(playing_req)
                return concept_method_req

            @staticmethod
            def plays(role_concept):
                grpc_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(role_concept)
                plays_req = concept_messages.Type.Plays.Req()
                plays_req.role.CopyFrom(grpc_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.type_plays_req.CopyFrom(plays_req)
                return concept_method_req

            @staticmethod
            def unplay(role_concept):
                grpc_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(role_concept)
                unplay_req = concept_messages.Type.Unplay.Req()
                unplay_req.role.CopyFrom(grpc_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.type_unplay_req.CopyFrom(unplay_req)
                return concept_method_req

        class EntityType(object):
            """ Generates EntityType method messages """

            @staticmethod
            def create():
                create_req = concept_messages.EntityType.Create.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.entityType_create_req.CopyFrom(create_req)
                return concept_method_req

        class RelationType(object):
            """ Generates RelationType method messages """
            
            @staticmethod
            def create():
                create_req = concept_messages.RelationType.Create.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.relationType_create_req.CopyFrom(create_req)
                return concept_method_req

            @staticmethod
            def roles():
                roles_req = concept_messages.RelationType.Roles.Iter.Req()
                concept_messages_req = concept_messages.Method.Iter.Req()
                concept_messages_req.relationType_roles_iter_req.CopyFrom(roles_req)
                return concept_messages_req

            @staticmethod
            def relates(role_concept):
                grpc_role_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(role_concept)
                relates_req = concept_messages.RelationType.Relates.Req()
                relates_req.role.CopyFrom(grpc_role_concept)
                concept_messages_req = concept_messages.Method.Req()
                concept_messages_req.relationType_relates_req.CopyFrom(relates_req)
                return concept_messages_req

            @staticmethod
            def unrelate(role_concept):
                grpc_role_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(role_concept)
                unrelate_req = concept_messages.RelationType.Unrelate.Req()
                unrelate_req.role.CopyFrom(grpc_role_concept)
                concept_messages_req = concept_messages.Method.Req()
                concept_messages_req.relationType_unrelate_req.CopyFrom(unrelate_req)
                return concept_messages_req

        class AttributeType(object):
            """ Generates AttributeType method messages """
            
            @staticmethod
            def create(value, valuetype):
                grpc_value_object = RequestBuilder.ConceptMethod.as_value_object(value, valuetype)
                create_attr_req = concept_messages.AttributeType.Create.Req()
                create_attr_req.value.CopyFrom(grpc_value_object)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.attributeType_create_req.CopyFrom(create_attr_req)
                return concept_method_req

            @staticmethod
            def attribute(value, valuetype):
                grpc_value_object = RequestBuilder.ConceptMethod.as_value_object(value, valuetype)
                attribute_req = concept_messages.AttributeType.Attribute.Req()
                attribute_req.value.CopyFrom(grpc_value_object)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.attributeType_attribute_req.CopyFrom(attribute_req)
                return concept_method_req

            @staticmethod
            def value_type():
                valuetype_req = concept_messages.AttributeType.ValueType.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.attributeType_valueType_req.CopyFrom(valuetype_req)
                return concept_method_req

            @staticmethod
            def get_regex():
                get_regex_req = concept_messages.AttributeType.GetRegex.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.attributeType_getRegex_req.CopyFrom(get_regex_req)
                return concept_method_req

            @staticmethod
            def set_regex(regex):
                set_regex_req = concept_messages.AttributeType.SetRegex.Req()
                set_regex_req.regex = regex
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.attributeType_setRegex_req.CopyFrom(set_regex_req)
                return concept_method_req

        class Thing(object):
            """ Generates Thing method messages """

            @staticmethod
            def is_inferred():
                is_inferred_req = concept_messages.Thing.IsInferred.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.thing_isInferred_req.CopyFrom(is_inferred_req)
                return concept_method_req

            @staticmethod
            def type():
                type_req = concept_messages.Thing.Type.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.thing_type_req.CopyFrom(type_req)
                return concept_method_req
                
            @staticmethod
            def attributes(attribute_types=[]):
                """ Takes a list of AttributeType concepts to narrow attribute retrieval """
                attributes_req = concept_messages.Thing.Attributes.Iter.Req()
                for attribute_type_concept in attribute_types:
                    grpc_attr_type_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(attribute_type_concept)
                    attributes_req.attributeTypes.extend([grpc_attr_type_concept])
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.thing_attributes_iter_req.CopyFrom(attributes_req)
                return concept_method_req

            @staticmethod
            def relations(role_concepts=[]):
                """ Takes a list of role concepts to narrow the relations retrieval """
                relations_req = concept_messages.Thing.Relations.Iter.Req()
                for role_concept in role_concepts:
                    grpc_role_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(role_concept)
                    # TODO this could use .add() if can be made to work...
                    relations_req.roles.extend([grpc_role_concept])
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.thing_relations_iter_req.CopyFrom(relations_req)
                return concept_method_req
            
            @staticmethod
            def roles():
                roles_req = concept_messages.Thing.Roles.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.thing_roles_iter_req.CopyFrom(roles_req)
                return concept_method_req

            @staticmethod
            def keys(attribute_types=[]):
                """ Takes a  list of AttributeType concepts to narrow the key retrieval """
                keys_req = concept_messages.Thing.Keys.Iter.Req()
                for attribute_type_concept in attribute_types:
                    grpc_attr_type_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(attribute_type_concept)
                    keys_req.attributeTypes.extend([grpc_attr_type_concept])
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.thing_keys_iter_req.CopyFrom(keys_req)
                return concept_method_req
            
            @staticmethod
            def has(attribute_concept):
                grpc_attribute_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(attribute_concept)
                has_req = concept_messages.Thing.Has.Req()
                has_req.attribute.CopyFrom(grpc_attribute_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.thing_has_req.CopyFrom(has_req)
                return concept_method_req

            @staticmethod
            def unhas(attribute_concept):
                grpc_attribute_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(attribute_concept)
                unhas_req = concept_messages.Thing.Unhas.Req()
                unhas_req.attribute.CopyFrom(grpc_attribute_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.thing_unhas_req.CopyFrom(unhas_req)
                return concept_method_req
        
        class Relation(object):
            """ Generates Relation method messages """

            @staticmethod
            def role_players_map():
                role_players_map_req = concept_messages.Relation.RolePlayersMap.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.relation_rolePlayersMap_iter_req.CopyFrom(role_players_map_req)
                return concept_method_req

            @staticmethod
            def role_players(roles=[]):
                """ Retrieve concepts that can play the given roles """
                role_players_req = concept_messages.Relation.RolePlayers.Iter.Req()
                for role_concept in roles:
                    grpc_role_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(role_concept)
                    role_players_req.roles.extend([grpc_role_concept])
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.relation_rolePlayers_iter_req.CopyFrom(role_players_req)
                return concept_method_req
    
            @staticmethod
            def assign(role_concept, player_concept):
                grpc_role_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(role_concept)
                grpc_player_concept  = RequestBuilder.ConceptMethod._concept_to_grpc_concept(player_concept)
                assign_req = concept_messages.Relation.Assign.Req()
                assign_req.role.CopyFrom(grpc_role_concept)
                assign_req.player.CopyFrom(grpc_player_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.relation_assign_req.CopyFrom(assign_req)
                return concept_method_req
            
            @staticmethod
            def unassign(role_concept, player_concept):
                grpc_role_concept = RequestBuilder.ConceptMethod._concept_to_grpc_concept(role_concept)
                grpc_player_concept  = RequestBuilder.ConceptMethod._concept_to_grpc_concept(player_concept)
                unassign_req = concept_messages.Relation.Unassign.Req()
                unassign_req.role.CopyFrom(grpc_role_concept)
                unassign_req.player.CopyFrom(grpc_player_concept)
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.relation_unassign_req.CopyFrom(unassign_req)
                return concept_method_req

        class Attribute(object):
            """ Generates Attribute method messages """

            @staticmethod
            def value():
                value_req = concept_messages.Attribute.Value.Req()
                concept_method_req = concept_messages.Method.Req()
                concept_method_req.attribute_value_req.CopyFrom(value_req)
                return concept_method_req

            @staticmethod
            def owners():
                owners_req = concept_messages.Attribute.Owners.Iter.Req()
                concept_method_req = concept_messages.Method.Iter.Req()
                concept_method_req.attribute_owners_iter_req.CopyFrom(owners_req)
                return concept_method_req
        
        class Entity(object):
            """ Empty implementation -- never create requests on Entity """
            pass
