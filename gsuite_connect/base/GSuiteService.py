from google.oauth2 import service_account
from abc import ABC, abstractmethod
from gsuite_connect.base.config import CREDENTIALS


class GSuiteService(ABC):

    @abstractmethod
    def get_scopes(self):
        raise NotImplementedError

    @abstractmethod
    def get_service(self, credentials):
        raise NotImplementedError

    def __init__(self):

        # The name of the file containing your credentials
        self.credential_path = CREDENTIALS
        self.SCOPES = self.get_scopes()

    def build(self):
        # Get credentials into the desired format
        creds = service_account.Credentials.from_service_account_file(
            self.credential_path, scopes=self.SCOPES
        )

        service = self.get_service(creds)
        return service
