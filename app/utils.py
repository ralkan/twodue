from functools import lru_cache

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class AzureKeyVaultClient:
    _client = None
    _conf = None

    def __init__(self, conf, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conf = conf

    @property
    def client(self):
        if self._client is None:
            credential = DefaultAzureCredential()
            self._client = SecretClient(vault_url=self._conf.KV_URI, credential=credential)
        return self._client

    @lru_cache(maxsize=10)
    def get_secret(self, secret_name):
        return self.client.get_secret(secret_name)
