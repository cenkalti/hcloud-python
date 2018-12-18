from hcloud.core.client import ClientEntityBase, BoundModelBase
from hcloud.server_types.domain import ServerType


class BoundServerType(BoundModelBase):
    model = ServerType


class ServerTypesClient(ClientEntityBase):
    results_list_attribute_name = 'server_types'

    def get_by_id(self, id):
        # type: (int) -> server_types.client.BoundServerType
        response = self._client.request(url="/server_types/{server_type_id}".format(server_type_id=id), method="GET")
        return BoundServerType(self, response['server_type'])

    def get_list(self, name=None, page=None, per_page=None):
        # type: (Optional[str], Optional[int], Optional[int]) -> PageResults[List[BoundServerType], Meta]
        params = {}
        if name is not None:
            params['name'] = name
        if page is not None:
            params['page'] = page
        if per_page is not None:
            params['per_page'] = per_page

        response = self._client.request(url="/server_types", method="GET", params=params)
        server_types = [BoundServerType(self, server_type_data) for server_type_data in response['server_types']]
        return self.add_meta_to_result(server_types, response)

    def get_all(self, name=None):
        # type: (Optional[str]) -> List[BoundServerType]
        return super(ServerTypesClient, self).get_all(name=name)