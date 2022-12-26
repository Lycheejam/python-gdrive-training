from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import traceback


class ManipulationGoogleDrive:
    def __init__(self) -> None:
        self.drive = self.login_with_service_account()

    def main(self) -> None:
        # テキストファイルを作成して共有設定
        text_file = self.drive.CreateFile({"title": "Hello.txt"})
        text_file.SetContentFile(
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "../Hello.txt")
        )
        text_file.Upload()

        text_file.InsertPermission(
            {"type": "user", "role": "reader", "value": "example@example.com"},
            param={"sendNotificationEmails": False},
        )

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
