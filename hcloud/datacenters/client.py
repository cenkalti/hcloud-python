# -*- coding: utf-8 -*-
from hcloud.core.client import ClientEntityBase, BoundModelBase

from hcloud.datacenters.domain import Datacenter, DatacenterServerTypes
from hcloud.locations.client import BoundLocation
from hcloud.server_types.client import BoundServerType


class BoundDatacenter(BoundModelBase):
    model = Datacenter

    def __init__(self, client, data):
        location = data.get("location")
        if location is not None:
            data['location'] = BoundLocation(client._client.locations, location)

        server_types = data.get("server_types")
        if server_types is not None:
            available = [BoundServerType(client._client.server_types, {"id": server_type}, complete=False) for server_type in server_types['available']]
            supported = [BoundServerType(client._client.server_types, {"id": server_type}, complete=False) for server_type in server_types['supported']]
            available_for_migration = [BoundServerType(client._client.server_types, {"id": server_type}, complete=False) for server_type in server_types['available_for_migration']]
            data['server_types'] = DatacenterServerTypes(available=available, supported=supported, available_for_migration=available_for_migration)

        super(BoundDatacenter, self).__init__(client, data)


class DatacentersClient(ClientEntityBase):
    results_list_attribute_name = 'datacenters'

    def get_by_id(self, id):
        # type: (int) -> BoundDatacenter
        response = self._client.request(url="/datacenters/{datacenter_id}".format(datacenter_id=id), method="GET")
        return BoundDatacenter(self, response['datacenter'])

    def get_list(self,
                 name=None,     # type: Optional[str]
                 page=None,     # type: Optional[int]
                 per_page=None  # type: Optional[int]
                 ):
        # type: (...) -> PageResults[List[BoundDatacenter], Meta]
        params = {}
        if name is not None:
            params["name"] = name

        if page is not None:
            params['page'] = page

        if per_page is not None:
            params['per_page'] = per_page

        response = self._client.request(url="/datacenters", method="GET", params=params)

        datacenters = [BoundDatacenter(self, datacenter_data) for datacenter_data in response['datacenters']]

        return self.add_meta_to_result(datacenters, response)

    def get_all(self, name=None):
        # type: (Optional[str]) -> List[BoundDatacenter]
        return super(DatacentersClient, self).get_all(name=name)