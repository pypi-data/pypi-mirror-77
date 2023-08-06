#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains non manifold edge validation implementation
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import tpDcc as tp

import pyblish.api


class SelectNonManifoldEdges(pyblish.api.Action):
    label = 'Select Non-Manifold Edges'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Select Non-Manifold Edges Action is only available in Maya!')
            return False

        for instance in context:
            if not instance.data['publish']:
                continue

            node = instance.data.get('node', None)
            assert node and tp.Dcc.object_exists(node), 'No valid node found in current instance: {}'.format(instance)

            non_manifold_edges = instance.data.get('non_manifold_edges', None)
            if not non_manifold_edges:
                continue

            tp.Dcc.select_object(non_manifold_edges, replace_selection=False)


class ValidateNonManifoldEdges(pyblish.api.InstancePlugin):
    """
    Checks if there are geometry with non manifold edges
    """

    label = 'Topology - Non-Manifold Edges'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    families = ['geometry']
    optional = False
    actions = [SelectNonManifoldEdges]

    def process(self, instance):

        import maya.api.OpenMaya as OpenMaya

        node = instance.data.get('node', None)
        assert tp.Dcc.object_exists(node), 'No valid node found in current instance: {}'.format(instance)

        nodes_to_check = self._nodes_to_check(node)
        assert nodes_to_check, 'No Nodes to check found!'

        meshes_selection_list = OpenMaya.MSelectionList()
        for node in nodes_to_check:
            meshes_selection_list.add(node)

        non_manifold_edges_found = list()
        sel_it = OpenMaya.MItSelectionList(meshes_selection_list)
        while not sel_it.isDone():
            edge_it = OpenMaya.MItMeshEdge(sel_it.getDagPath())
            object_name = sel_it.getDagPath().getPath()
            while not edge_it.isDone():
                if edge_it.numConnectedFaces() > 2:
                    edge_index = edge_it.index()
                    component_name = '{}.e[{}]'.format(object_name, edge_index)
                    non_manifold_edges_found.append(component_name)
                edge_it.next()
            sel_it.next()

        if non_manifold_edges_found:
            instance.data['non_manifold_edges'] = non_manifold_edges_found

        assert not non_manifold_edges_found, 'Non-Manifold Edges in the following components: {}'.format(
            non_manifold_edges_found)

    def _nodes_to_check(self, node):

        valid_nodes = list()
        nodes = tp.Dcc.list_children(node=node, all_hierarchy=True, full_path=True, children_type='transform')
        if not nodes:
            nodes = [node]
        else:
            nodes.append(node)

        for node in nodes:
            shapes = tp.Dcc.list_shapes(node=node, full_path=True)
            if not shapes:
                continue
            valid_nodes.append(node)

        return valid_nodes
