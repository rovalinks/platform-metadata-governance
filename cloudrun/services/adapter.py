from clients.compute import ComputeClient
from clients.bigquery import BigQueryClient
from clients.storage import StorageClient


class AdapterService:

    def __init__(self):

        self.clients = [
            ComputeClient(),
            BigQueryClient(),
            StorageClient(),
        ]

    def client_for(self, asset_type: str):

        for client in self.clients:

            if client.supports(asset_type):

                return client

        return None