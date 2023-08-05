# -*- coding: utf-8 -*-
###
# (C) Copyright [2019] Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from future import standard_library

standard_library.install_aliases()

from hpOneView.resources.resource import ResourceClient


class Scopes(object):
    """
    Scopes API client.

    Note:
        This resource is available for API version 300 or later.

    """
    URI = '/rest/scopes'

    DEFAULT_VALUES = {
        '300': {"type": "Scope"},
        '500': {"type": "ScopeV2"}
    }

    def __init__(self, con):
        self._connection = con
        self._client = ResourceClient(con, self.URI)

    def get_all(self, start=0, count=-1, sort='', query='', view=''):
        """
         Gets a list of scopes.

        Args:
            start:
                The first item to return, using 0-based indexing.
                If not specified, the default is 0 - start with the first available item.
            count:
                The number of resources to return. A count of -1 requests all items.
                The actual number of items in the response might differ from the requested
                count if the sum of start and count exceeds the total number of items.
            sort:
                The sort order of the returned data set. By default, the sort order is based
                on create time with the oldest entry first.
            query:
                A general query string to narrow the list of resources returned. The default
                is no query - all resources are returned.
            view:
                 Returns a specific subset of the attributes of the resource or collection, by
                 specifying the name of a predefined view. The default view is expand (show all
                 attributes of the resource and all elements of collections of resources).

        Returns:
            list: A list of scopes.
        """
        return self._client.get_all(start, count, sort=sort, query=query, view=view)

    def get(self, id_or_uri):
        """
        Gets the Scope with the specified ID or URI.

        Args:
            id_or_uri: ID or URI of the Scope

        Returns:
            dict: Scope
        """
        return self._client.get(id_or_uri)

    def get_by_name(self, name):
        """
        Gets a Scope by name.

        Args:
            name: Name of the Scope

        Returns:
            dict: Scope.
        """
        scopes = self._client.get_all()
        result = [x for x in scopes if x['name'] == name]
        return result[0] if result else None

    def create(self, resource, timeout=-1):
        """
        Creates a scope.

        Args:
            resource (dict): Object to create.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Created scope.

        """
        return self._client.create(resource, timeout=timeout, default_values=self.DEFAULT_VALUES)

    def update(self, resource, timeout=-1):
        """
        Updates a scope.

        Args:
            resource (dict): Object to update.
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView, just stop waiting for its completion.

        Returns:
            dict: Updated scope.

        """
        headers = {'If-Match': resource.get('eTag', '*')}
        return self._client.update(resource, timeout=timeout, default_values=self.DEFAULT_VALUES,
                                   custom_headers=headers)

    def delete(self, resource, timeout=-1):
        """
        Deletes a Scope.

        Args:
            resource: dict object to delete
            timeout:
                Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            bool: Indicates if the resource was successfully deleted.

        """
        if type(resource) is dict:
            headers = {'If-Match': resource.get('eTag', '*')}
        else:
            headers = {'If-Match': '*'}
        return self._client.delete(resource, timeout=timeout, custom_headers=headers)

    def update_resource_assignments(self, id_or_uri, resource_assignments, timeout=-1):
        """
        Modifies scope membership by adding or removing resource assignments.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            resource_assignments (dict):
                A dict object with a list of resource URIs to be added and a list of resource URIs to be removed.
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        uri = self._client.build_uri(id_or_uri) + "/resource-assignments"

        headers = {'Content-Type': 'application/json'}

        return self._client.patch_request(uri, resource_assignments, timeout=timeout, custom_headers=headers)

    def patch(self, id_or_uri, operation, path, value, timeout=-1):
        """
        Uses the PATCH to update a resource for the given scope.

        Only one operation can be performed in each PATCH call.

        Args:
            id_or_uri: Can be either the resource ID or the resource URI.
            operation: Patch operation
            path: Path
            value: Value
            timeout: Timeout in seconds. Wait for task completion by default. The timeout does not abort the operation
                in OneView; it just stops waiting for its completion.

        Returns:
            dict: Updated resource.
        """
        headers = {'Content-Type': 'application/json-patch+json'}
        return self._client.patch(id_or_uri, operation, path, value, timeout=timeout, custom_headers=headers)
