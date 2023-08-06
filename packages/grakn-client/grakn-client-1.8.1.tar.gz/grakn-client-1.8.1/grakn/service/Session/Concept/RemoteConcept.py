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

from grakn.service.Session.util import enums
from grakn.service.Session.util.RequestBuilder import RequestBuilder
from grakn.exception.GraknError import GraknError
from six.moves import map


class RemoteConcept(object):

    def __init__(self, concept_id, base_type, tx_service):
        self.id = concept_id
        self.base_type = base_type
        self._tx_service = tx_service

    def as_remote(self, tx_service):
        return type(self)(self.id, self.base_type, tx_service)

    def delete(self):
        del_request = RequestBuilder.ConceptMethod.delete()
        method_response = self._tx_service.run_concept_method(self.id, del_request)
        return

    def is_deleted(self):
        retrieved = self._tx_service.get_concept(self.id)
        return retrieved is None

    def is_schema_concept(self):
        """ Check if this concept is a schema concept """
        return isinstance(self, RemoteSchemaConcept)

    is_schema_concept.__annotations__ = {'return': bool}

    def is_type(self):
        """ Check if this concept is a Type concept """
        return isinstance(self, RemoteType)

    is_type.__annotations__ = {'return': bool}

    def is_thing(self):
        """ Check if this concept is a Thing concept """
        return isinstance(self, RemoteThing)

    is_thing.__annotations__ = {'return': bool}

    def is_attribute_type(self):
        """ Check if this concept is an AttributeType concept """
        return isinstance(self, RemoteAttributeType)

    is_attribute_type.__annotations__ = {'return': bool}

    def is_entity_type(self):
        """ Check if this concept is an EntityType concept """
        return isinstance(self, RemoteEntityType)

    is_entity_type.__annotations__ = {'return': bool}

    def is_relation_type(self):
        """ Check if this concept is a RelationType concept """
        return isinstance(self, RemoteRelationType)

    is_relation_type.__annotations__ = {'return': bool}

    def is_role(self):
        """ Check if this concept is a Role """
        return isinstance(self, RemoteRole)

    is_role.__annotations__ = {'return': bool}

    def is_rule(self):
        """ Check if this concept is a Rule concept """
        return isinstance(self, RemoteRule)

    is_rule.__annotations__ = {'return': bool}

    def is_attribute(self):
        """ Check if this concept is an Attribute concept """
        return isinstance(self, RemoteAttribute)

    is_attribute.__annotations__ = {'return': bool}

    def is_entity(self):
        """ Check if this concept is an Entity concept """
        return isinstance(self, RemoteEntity)

    is_entity.__annotations__ = {'return': bool}

    def is_relation(self):
        """ Check if this concept is a Relation concept """
        return isinstance(self, RemoteRelation)

    is_relation.__annotations__ = {'return': bool}


class RemoteSchemaConcept(RemoteConcept):

    def label(self, value=None):
        """ 
        Get or set label of this schema concept. 
        If used as setter returns self 
        """
        if value is None:
            get_label_req = RequestBuilder.ConceptMethod.SchemaConcept.get_label()
            method_response = self._tx_service.run_concept_method(self.id, get_label_req)
            return method_response.schemaConcept_getLabel_res.label
        else:
            set_label_req = RequestBuilder.ConceptMethod.SchemaConcept.set_label(value)
            method_response = self._tx_service.run_concept_method(self.id, set_label_req)
            return self

    def sup(self, super_concept=None):
        """ 
        Get or set super schema concept.
        If used as a setter returns self
        """
        if super_concept is None:
            # get direct super schema concept
            get_sup_req = RequestBuilder.ConceptMethod.SchemaConcept.get_sup()
            method_response = self._tx_service.run_concept_method(self.id, get_sup_req)
            get_sup_response = method_response.schemaConcept_getSup_res
            # check if received a Null or Concept
            whichone = get_sup_response.WhichOneof('res')
            if whichone == 'schemaConcept':
                grpc_schema_concept = get_sup_response.schemaConcept
                from grakn.service.Session.Concept import ConceptFactory
                concept = ConceptFactory.create_remote_concept(self._tx_service, grpc_schema_concept)
                return concept
            elif whichone == 'null':
                return None
            else:
                raise GraknError("Unknown response concent for getting super schema concept: {0}".format(whichone))
        else:
            # set direct super SchemaConcept of this SchemaConcept
            set_sup_req = RequestBuilder.ConceptMethod.SchemaConcept.set_sup(super_concept)
            method_response = self._tx_service.run_concept_method(self.id, set_sup_req)
            return self

    def subs(self):
        """ Retrieve the sub schema concepts of this schema concept, as an iterator """
        subs_req = RequestBuilder.ConceptMethod.SchemaConcept.subs()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.schemaConcept_subs_iter_res.schemaConcept),
                   self._tx_service.run_concept_iter_method(self.id, subs_req))

    def sups(self):
        """ Retrieve the all supertypes (direct and higher level) of this schema concept as an iterator """
        sups_req = RequestBuilder.ConceptMethod.SchemaConcept.sups()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.schemaConcept_sups_iter_res.schemaConcept),
                   self._tx_service.run_concept_iter_method(self.id, sups_req))


class RemoteType(RemoteSchemaConcept):

    def is_abstract(self, value=None):
        """
        Get/Set whether this schema Type object is abstract.
        When used as a setter returns `self` 
        """
        if value is None:
            # return True/False if the type is set to abstract
            is_abstract_req = RequestBuilder.ConceptMethod.Type.is_abstract()
            method_response = self._tx_service.run_concept_method(self.id, is_abstract_req)
            return method_response.type_isAbstract_res.abstract
        else:
            set_abstract_req = RequestBuilder.ConceptMethod.Type.set_abstract(value)
            method_response = self._tx_service.run_concept_method(self.id, set_abstract_req)
            return self

    is_abstract.__annotations__ = {'value': bool, 'return': bool}

    def attributes(self):
        """ Retrieve all attributes attached to this Type as an iterator """
        attributes_req = RequestBuilder.ConceptMethod.Type.attributes()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.type_attributes_iter_res.attributeType),
                   self._tx_service.run_concept_iter_method(self.id, attributes_req))

    def instances(self):
        """ Retrieve all instances of this Type as an iterator """
        instances_req = RequestBuilder.ConceptMethod.Type.instances()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.type_instances_iter_res.thing),
                   self._tx_service.run_concept_iter_method(self.id, instances_req))

    def playing(self):
        """ Retrieve iterator of roles played by this type """
        playing_req = RequestBuilder.ConceptMethod.Type.playing()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.type_playing_iter_res.role),
                   self._tx_service.run_concept_iter_method(self.id, playing_req))

    def plays(self, role_concept):
        """ Set a role that is played by this Type """
        plays_req = RequestBuilder.ConceptMethod.Type.plays(role_concept)
        method_response = self._tx_service.run_concept_method(self.id, plays_req)
        return self

    def unplay(self, role_concept):
        """ Remove a role that is played by this Type """
        unplay_req = RequestBuilder.ConceptMethod.Type.unplay(role_concept)
        method_response = self._tx_service.run_concept_method(self.id, unplay_req)
        return

    def has(self, attribute_concept_type):
        """ Attach an attributeType concept to the type """
        has_req = RequestBuilder.ConceptMethod.Type.has(attribute_concept_type)
        method_response = self._tx_service.run_concept_method(self.id, has_req)
        return self

    def unhas(self, attribute_concept_type):
        """ Remove an attribute type concept from this type """
        unhas_req = RequestBuilder.ConceptMethod.Type.unhas(attribute_concept_type)
        method_response = self._tx_service.run_concept_method(self.id, unhas_req)
        return self

    def keys(self):
        """ Retrieve an iterator of attribute types that this Type uses as keys """
        keys_req = RequestBuilder.ConceptMethod.Type.keys()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.type_keys_iter_res.attributeType),
                   self._tx_service.run_concept_iter_method(self.id, keys_req))

    def key(self, attribute_concept_type):
        """ Add an attribute type to be a key for this Type """
        key_req = RequestBuilder.ConceptMethod.Type.key(attribute_concept_type)
        method_response = self._tx_service.run_concept_method(self.id, key_req)
        return self

    def unkey(self, attribute_concept_type):
        """ Remove an attribute type from this Type from being a key """
        unkey_req = RequestBuilder.ConceptMethod.Type.unkey(attribute_concept_type)
        method_response = self._tx_service.run_concept_method(self.id, unkey_req)
        return self


class RemoteEntityType(RemoteType):

    def create(self):
        """ Instantiate an entity of the given type and return it """
        create_req = RequestBuilder.ConceptMethod.EntityType.create()
        method_response = self._tx_service.run_concept_method(self.id, create_req)
        grpc_entity_concept = method_response.entityType_create_res.entity
        from grakn.service.Session.Concept import ConceptFactory
        return ConceptFactory.create_remote_concept(self._tx_service, grpc_entity_concept)


class RemoteAttributeType(RemoteType):

    def create(self, value):
        """ Create an instance with this AttributeType """
        self_value_type = self.value_type()
        create_inst_req = RequestBuilder.ConceptMethod.AttributeType.create(value, self_value_type)
        method_response = self._tx_service.run_concept_method(self.id, create_inst_req)
        grpc_attribute_concept = method_response.attributeType_create_res.attribute
        from grakn.service.Session.Concept import ConceptFactory
        return ConceptFactory.create_remote_concept(self._tx_service, grpc_attribute_concept)

    def attribute(self, value):
        """ Retrieve an attribute instance by value if it exists """
        self_value_type = self.value_type()
        get_attribute_req = RequestBuilder.ConceptMethod.AttributeType.attribute(value, self_value_type)
        method_response = self._tx_service.run_concept_method(self.id, get_attribute_req)
        response = method_response.attributeType_attribute_res
        whichone = response.WhichOneof('res')
        if whichone == 'attribute':
            from grakn.service.Session.Concept import ConceptFactory
            return ConceptFactory.create_remote_concept(self._tx_service, response.attribute)
        elif whichone == 'null':
            return None
        else:
            raise GraknError("Unknown `res` key in AttributeType `attribute` response: {0}".format(whichone))

    def value_type(self):
        """ Get the ValueType enum (grakn.ValueType) corresponding to the type of this attribute """
        get_value_type_req = RequestBuilder.ConceptMethod.AttributeType.value_type()
        method_response = self._tx_service.run_concept_method(self.id, get_value_type_req)
        response = method_response.attributeType_valueType_res
        whichone = response.WhichOneof('res')
        if whichone == 'valueType':
            # iterate over enum ValueType enum to find matching data type
            for e in enums.ValueType:
                if e.value == response.valueType:
                    return e
            else:
                # loop exited normally
                raise GraknError("Reported valuetype NOT in enum: {0}".format(response.valueType))
        elif whichone == 'null':
            return None
        else:
            raise GraknError("Unknown valuetype response for AttributeType: {0}".format(whichone))

    def regex(self, pattern=None):
        """ Get or set regex """
        if pattern is None:
            get_regex_req = RequestBuilder.ConceptMethod.AttributeType.get_regex()
            method_response = self._tx_service.run_concept_method(self.id, get_regex_req)
            return method_response.attributeType_getRegex_res.regex
        else:
            set_regex_req = RequestBuilder.ConceptMethod.AttributeType.set_regex(pattern)
            method_response = self._tx_service.run_concept_method(self.id, set_regex_req)
            return self

    regex.__annotations__ = {'pattern': str}


class RemoteRelationType(RemoteType):
    def create(self):
        """ Create an instance of a relation with this type """
        create_rel_inst_req = RequestBuilder.ConceptMethod.RelationType.create()
        method_response = self._tx_service.run_concept_method(self.id, create_rel_inst_req)
        grpc_relation_concept = method_response.relationType_create_res.relation
        from grakn.service.Session.Concept import ConceptFactory
        return ConceptFactory.create_remote_concept(self._tx_service, grpc_relation_concept)

    def roles(self):
        """ Retrieve roles in this relation schema type """
        get_roles = RequestBuilder.ConceptMethod.RelationType.roles()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.relationType_roles_iter_res.role),
                   self._tx_service.run_concept_iter_method(self.id, get_roles))


    def relates(self, role):
        """ Set a role in this relation schema type """
        relates_req = RequestBuilder.ConceptMethod.RelationType.relates(role)
        method_response = self._tx_service.run_concept_method(self.id, relates_req)
        return self

    def unrelate(self, role):
        """ Remove a role in this relation schema type """
        unrelate_req = RequestBuilder.ConceptMethod.RelationType.unrelate(role)
        method_response = self._tx_service.run_concept_method(self.id, unrelate_req)
        return self


class RemoteRule(RemoteSchemaConcept):

    def get_when(self):
        """ Retrieve the `when` clause for this rule """
        when_req = RequestBuilder.ConceptMethod.Rule.when()
        method_response = self._tx_service.run_concept_method(self.id, when_req)
        response = method_response.rule_when_res
        whichone = response.WhichOneof('res')
        if whichone == 'pattern':
            return response.pattern
        elif whichone == 'null':
            return None
        else:
            raise GraknError("Unknown field in get_when of `rule`: {0}".format(whichone))

    def get_then(self):
        """ Retrieve the `then` clause for this rule """
        then_req = RequestBuilder.ConceptMethod.Rule.then()
        method_response = self._tx_service.run_concept_method(self.id, then_req)
        response = method_response.rule_then_res
        whichone = response.WhichOneof('res')
        if whichone == 'pattern':
            return response.pattern
        elif whichone == 'null':
            return None
        else:
            raise GraknError("Unknown field in get_then or `rule`: {0}".format(whichone))


class RemoteRole(RemoteSchemaConcept):

    def relations(self):
        """ Retrieve relations that this role participates in, as an iterator """
        relations_req = RequestBuilder.ConceptMethod.Role.relations()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.role_relations_iter_res.relationType),
                   self._tx_service.run_concept_iter_method(self.id, relations_req))

    def players(self):
        """ Retrieve an iterator of entities that play this role """
        players_req = RequestBuilder.ConceptMethod.Role.players()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.role_players_iter_res.type),
                   self._tx_service.run_concept_iter_method(self.id, players_req))


class RemoteThing(RemoteConcept):

    def is_inferred(self):
        """ Is this instance inferred """
        is_inferred_req = RequestBuilder.ConceptMethod.Thing.is_inferred()
        method_response = self._tx_service.run_concept_method(self.id, is_inferred_req)
        return method_response.thing_isInferred_res.inferred

    is_inferred.__annotations__ = {'return': bool}

    def type(self):
        """ Get the type (schema concept) of this Thing """
        type_req = RequestBuilder.ConceptMethod.Thing.type()
        method_response = self._tx_service.run_concept_method(self.id, type_req)
        from grakn.service.Session.Concept import ConceptFactory
        return ConceptFactory.create_remote_concept(self._tx_service, method_response.thing_type_res.type)

    def relations(self, *roles):
        """ Get iterator this Thing's relations, filtered to the optionally provided roles """
        relations_req = RequestBuilder.ConceptMethod.Thing.relations(roles)
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.thing_relations_iter_res.relation),
                   self._tx_service.run_concept_iter_method(self.id, relations_req))

    def attributes(self, *attribute_types):
        """ Retrieve iterator of this Thing's attributes, filtered by optionally provided attribute types """
        attrs_req = RequestBuilder.ConceptMethod.Thing.attributes(attribute_types)
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.thing_attributes_iter_res.attribute),
                   self._tx_service.run_concept_iter_method(self.id, attrs_req))

    def roles(self):
        """ Retrieve iterator of roles this Thing plays """
        roles_req = RequestBuilder.ConceptMethod.Thing.roles()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.thing_roles_iter_res.role),
                   self._tx_service.run_concept_iter_method(self.id, roles_req))

    def keys(self, *attribute_types):
        """ Retrieve iterator of keys (i.e. actual attributes) of this Thing, filtered by the optionally provided attribute types """
        keys_req = RequestBuilder.ConceptMethod.Thing.keys(attribute_types)
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.thing_keys_iter_res.attribute),
                   self._tx_service.run_concept_iter_method(self.id, keys_req))

    def has(self, attribute):
        """ Attach an attribute instance to this Thing """
        has_req = RequestBuilder.ConceptMethod.Thing.has(attribute)
        method_response = self._tx_service.run_concept_method(self.id, has_req)
        return

    def unhas(self, attribute):
        """ Remove an attribute instance from this Thing """
        unhas_req = RequestBuilder.ConceptMethod.Thing.unhas(attribute)
        method_response = self._tx_service.run_concept_method(self.id, unhas_req)
        return


class RemoteEntity(RemoteThing):
    pass


class RemoteAttribute(RemoteThing):

    def value(self):
        """ Retrieve the value contained in this Attribute instance """
        value_req = RequestBuilder.ConceptMethod.Attribute.value()
        method_response = self._tx_service.run_concept_method(self.id, value_req)
        grpc_value_object = method_response.attribute_value_res.value
        from grakn.service.Session.util import ResponseReader
        return ResponseReader.ResponseReader.from_grpc_value_object(grpc_value_object)

    def owners(self):
        """ Retrieve entities that have this attribute value """
        owners_req = RequestBuilder.ConceptMethod.Attribute.owners()
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.attribute_owners_iter_res.thing),
                   self._tx_service.run_concept_iter_method(self.id, owners_req))


class RemoteRelation(RemoteThing):

    def role_players_map(self):
        """ Retrieve dictionary {role : set(players)} for this relation """
        role_players_map_req = RequestBuilder.ConceptMethod.Relation.role_players_map()

        tx_service = self._tx_service
        # create the iterator to obtain all the pairs of (role, player)
        def to_pair(iter_res):
            response = iter_res.relation_rolePlayersMap_iter_res
            from grakn.service.Session.Concept import ConceptFactory
            role = ConceptFactory.create_remote_concept(tx_service, response.role)
            from grakn.service.Session.Concept import ConceptFactory
            player = ConceptFactory.create_remote_concept(tx_service, response.player)
            return (role, player)

        # collect all pairs of (role, player) from the iterator (executes over network to Grakn server)
        pairs = list(map(to_pair, self._tx_service.run_concept_iter_method(self.id, role_players_map_req)))

        # aggregate into a map from role to set(player)
        # note: need to use role ID as the map key ultimately
        mapping = {}
        id_mapping = {}
        for (role, player) in pairs:
            role_id = role.id
            if role_id in id_mapping:
                role_key = id_mapping[role_id]
            else:
                id_mapping[role_id] = role
                role_key = role
                mapping[role_key] = []
            mapping[role_key].append(player)

        return mapping

    def role_players(self, *roles):
        """ Retrieve role players filtered by roles """
        role_players_req = RequestBuilder.ConceptMethod.Relation.role_players(roles)
        from grakn.service.Session.Concept import ConceptFactory
        return map(lambda iter_res:
                   ConceptFactory.create_remote_concept(self._tx_service,
                                                        iter_res.relation_rolePlayers_iter_res.thing),
                   self._tx_service.run_concept_iter_method(self.id, role_players_req))

    def assign(self, role, thing):
        """ Assign an entity to a role on this relation instance """
        assign_req = RequestBuilder.ConceptMethod.Relation.assign(role, thing)
        method_response = self._tx_service.run_concept_method(self.id, assign_req)
        return self

    def unassign(self, role, thing):
        """ Un-assign an entity from a role on this relation instance """
        unassign_req = RequestBuilder.ConceptMethod.Relation.unassign(role, thing)
        method_response = self._tx_service.run_concept_method(self.id, unassign_req)
        return self
