from gsuite_connect.docs.GoogleDocsService import GoogleDocsService
import datetime


class GoogleDocsGenerator:

    def __init__(self):
        self.docs_service = GoogleDocsService().build()

    @staticmethod
    def default_document_name(document_title):
        return f"{datetime.date.today().strftime('%m-%d-%Y')}_{document_title}"

    def create_doc_template_header(self, document_title, doc_id):
        # add template header
        title_template = f"""
        {document_title}
        """
        template = f"""
        Written on {datetime.date.today()} at {datetime.datetime.now().strftime("%H:%M:%S")}
        """
        requests = [
            {
                "insertText": {
                    "location": {
                        "index": 1,
                    },
                    "text": title_template,
                }
            },
            {
                "insertText": {
                    "location": {
                        "index": len(title_template) + 1,
                    },
                    "text": template,
                }
            },
            {
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": 1,
                        "endIndex": len(title_template),
                    },
                    "paragraphStyle": {
                        "namedStyleType": "TITLE",
                        "spaceAbove": {"magnitude": 1.0, "unit": "PT"},
                        "spaceBelow": {"magnitude": 1.0, "unit": "PT"},
                    },
                    "fields": "namedStyleType,spaceAbove,spaceBelow",
                }
            },
            {
                "updateParagraphStyle": {
                    "range": {
                        "startIndex": len(title_template) + 1,
                        "endIndex": len(title_template) + len(template),
                    },
                    "paragraphStyle": {
                        "namedStyleType": "SUBTITLE",
                        "spaceAbove": {"magnitude": 1.0, "unit": "PT"},
                        "spaceBelow": {"magnitude": 1.0, "unit": "PT"},
                    },
                    "fields": "namedStyleType,spaceAbove,spaceBelow",
                }
            },
        ]
        result = (
            self.docs_service.documents()
            .batchUpdate(documentId=doc_id, body={"requests": requests})
            .execute()
        )
        end_index = len(title_template) + len(template) + 2
        return end_index

    def write_text_to_doc(self, start_index, text, doc_id):
        end_index = start_index + len(text)

        requests = [
            {
                "insertText": {
                    "location": {
                        "index": start_index,
                    },
                    "text": text,
                }
            },
        ]

        result = (
            self.docs_service.documents()
            .batchUpdate(documentId=doc_id, body={"requests": requests})
            .execute()
        )

        return end_index + 1

    def write_image_to_doc(self, start_index, image_url, doc_id):
        end_index = start_index

        requests = [
            {
                "insertInlineImage": {
                    "location": {
                        "index": start_index,
                    },
                    "uri": image_url,
                }
            }
        ]

        result = (
            self.docs_service.documents()
            .batchUpdate(documentId=doc_id, body={"requests": requests})
            .execute()
        )

        return end_index + 1
