from gsuite_connect.drive.GoogleDriveService import GoogleDriveService
from googleapiclient.http import MediaFileUpload


class GoogleDriveHelper:

    def __init__(self, folder_name):

        self.folder_name = folder_name
        self.drive_service = GoogleDriveService().build()
        self.top_level_folder_id = self.get_folder_id()

    @staticmethod
    def create_export_link(file_id):

        return f"https://drive.google.com/uc?export=download&id={file_id}"

    def get_webview_link(self, file_id):

        return (
            self.drive_service.files()
            .get(fileId=file_id, fields="webViewLink")
            .execute()["webViewLink"]
        )

    def upload_image(self, image_name, parent_folder_id=None):

        #ToDo: check supported image types

        if not parent_folder_id:
            parent_folder_id = self.top_level_folder_id

        file_metadata = {"name": image_name, "parents": [parent_folder_id]}
        media = MediaFileUpload(image_name, mimetype="image/jpg")
        file = (
            self.drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        return file.get("id")

    def create_new_permission(self, file_id, permission):
        """
        new_permission = {
            "role": "reader",
            "type": "anyone"
        }
        """

        result = (
            self.drive_service.permissions()
            .create(fileId=file_id, body=permission)
            .execute()
        )

        return result

    def create_new_folder(self, new_folder_name, parent_folder_id=None):

        if parent_folder_id:
            parents = [parent_folder_id]
        else:
            parents = [self.top_level_folder_id]

        folder_metadata = {
            "name": new_folder_name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": parents,
        }

        folder = (
            self.drive_service.files().create(body=folder_metadata, fields="id").execute()
        )
        return folder.get("id")

    def get_folder_id(self):

        folder_details = (
            self.drive_service.files()
            .list(
                q=f"mimeType = 'application/vnd.google-apps.folder' and name = '{self.folder_name}'"
            )
            .execute()
        )

        if not folder_details:
            raise ValueError("No folder called {self.folder_name} is found")

        return folder_details["files"][0].get("id", None)

    def create_basic_document(self, document_name, parent_folder_id=None):

        if not parent_folder_id:
            parent_folder_id = self.top_level_folder_id

        document_metadata = {
            "name": document_name,
            "mimeType": "application/vnd.google-apps.document",
            "parents": [parent_folder_id],
        }
        # make the document
        doc = (
            self.drive_service.files()
            .create(body=document_metadata, fields="id")
            .execute()
        )
        doc_id = doc.get("id")

        return doc_id
