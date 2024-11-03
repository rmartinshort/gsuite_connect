from gsuite_connect.base.GSuiteService import GSuiteService
from googleapiclient.discovery import build


class GoogleDriveService(GSuiteService):

    def get_scopes(self):
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        return SCOPES

    def get_service(self, creds):
        return build("drive", "v3", credentials=creds, cache_discovery=False)
