from gsuite_connect.drive.GoogleDriveService import GoogleDriveService
from googleapiclient.http import MediaFileUpload
from typing import Optional, Dict, Any


class GoogleDriveHelper:
    """
    A helper class for interacting with Google Drive, allowing for file uploads,
    folder creation, and permission management.

    Attributes:
        folder_name (str): The name of the top-level folder in Google Drive.
        drive_service (GoogleDriveService): The service object for interacting with Google Drive API.
        top_level_folder_id (str): The ID of the top-level folder.
    """

    def __init__(self, folder_name: str) -> None:
        """
        Initializes the GoogleDriveHelper with the specified folder name.

        Args:
            folder_name (str): The name of the folder to be used as the top-level folder.
        """
        self.folder_name = folder_name
        self.drive_service = GoogleDriveService().build()
        self.top_level_folder_id = self.get_folder_id()

    @staticmethod
    def create_export_link(file_id: str) -> str:
        """
        Creates a direct download link for a file in Google Drive.

        Args:
            file_id (str): The ID of the file.

        Returns:
            str: A direct download link for the file.
        """
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    def get_webview_link(self, file_id: str) -> str:
        """
        Retrieves the web view link for a specified file.

        Args:
            file_id (str): The ID of the file.

        Returns:
            str: The web view link for the file.
        """
        return (
            self.drive_service.files()
            .get(fileId=file_id, fields="webViewLink")
            .execute()["webViewLink"]
        )

    def upload_image(
        self, image_name: str, parent_folder_id: Optional[str] = None
    ) -> str:
        """
        Uploads an image to Google Drive.

        Args:
            image_name (str): The name of the image file to upload.
            parent_folder_id (Optional[str]): The ID of the parent folder. If None, uses the top-level folder.

        Returns:
            str: The ID of the uploaded file.
        """
        # ToDo: check supported image types

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

    def create_new_permission(
        self, file_id: str, permission: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Creates a new permission for a specified file.

        Args:
            file_id (str): The ID of the file.
            permission (Dict[str, Any]): The permission details.

        Returns:
            Dict[str, Any]: The result of the permission creation.
        """
        result = (
            self.drive_service.permissions()
            .create(fileId=file_id, body=permission)
            .execute()
        )

        return result

    def create_new_folder(
        self, new_folder_name: str, parent_folder_id: Optional[str] = None
    ) -> str:
        """
        Creates a new folder in Google Drive.

        Args:
            new_folder_name (str): The name of the new folder.
            parent_folder_id (Optional[str]): The ID of the parent folder. If None, uses the top-level folder.

        Returns:
            str: The ID of the newly created folder.
        """
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
            self.drive_service.files()
            .create(body=folder_metadata, fields="id")
            .execute()
        )
        return folder.get("id")

    def get_folder_id(self) -> str:
        """
        Retrieves the ID of the top-level folder based on the folder name.

        Returns:
            str: The ID of the folder.

        Raises:
            ValueError: If no folder with the specified name is found.
        """
        folder_details = (
            self.drive_service.files()
            .list(
                q=f"mimeType = 'application/vnd.google-apps.folder' and name = '{self.folder_name}'"
            )
            .execute()
        )

        if not folder_details.get("files"):
            raise ValueError(f"No folder called {self.folder_name} is found")

        return folder_details["files"][0].get("id", None)

    def create_basic_document(
        self, document_name: str, parent_folder_id: Optional[str] = None
    ) -> str:
        """
        Creates a new Google Document.

        Args:
            document_name (str): The name of the document.
            parent_folder_id (Optional[str]): The ID of the parent folder. If None, uses the top-level folder.

        Returns:
            str: The ID of the newly created document.
        """
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
