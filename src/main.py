from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import traceback


class ManipulationGoogleDrive:
    def __init__(self) -> None:
        self.drive = self.login_with_service_account()

    def main(self) -> None:
        # Create GoogleDriveFile instance with title 'Hello.txt'.
        file1 = self.drive.CreateFile({"title": "Hello.txt"})
        file1.Upload()  # Upload the file.
        print("title: %s, id: %s" % (file1["title"], file1["id"]))
        # title: Hello.txt, id: {{FILE_ID}}

        file1.InsertPermission({"type": "anyone", "role": "reader", "value": "anyone"})
        # TODO: not work
        # 'Bad Request. User message:
        # "You cannot share this item because it has been flagged as inappropriate."'
        # , 'domain': 'global', 'reason': 'invalidSharingRequest'}
        # permission = file1.InsertPermission({
        #                 'type': 'user',
        #                 'role': 'reader',
        #                 'value': 'example@example.com'
        #                 })

        print(file1["alternateLink"])  # Display the sharable link.

    # https://docs.iterative.ai/PyDrive2/oauth/#authentication-with-a-service-account
    def login_with_service_account(self, service_account_file_path: str = ""):
        if service_account_file_path == "":
            service_account_file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "../secrets.json"
            )
        settings = {
            "client_config_backend": "service",
            "service_config": {
                "client_json_file_path": service_account_file_path,
            },
        }

        try:
            gauth = GoogleAuth(settings=settings)
            gauth.ServiceAuth()
            return GoogleDrive(gauth)
        except Exception:
            print(traceback.format_exc())


if __name__ == "__main__":
    manipulation_google_drive = ManipulationGoogleDrive()
    manipulation_google_drive.main()
