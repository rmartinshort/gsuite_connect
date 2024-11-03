from gsuite_connect.base.GSuiteService import GSuiteService
from googleapiclient.discovery import build


class GoogleDocsService(GSuiteService):

    def get_scopes(self):
        SCOPES = ["https://www.googleapis.com/auth/documents"]
        return SCOPES

    def get_service(self, creds):
        return build("docs", "v1", credentials=creds, cache_discovery=False)
