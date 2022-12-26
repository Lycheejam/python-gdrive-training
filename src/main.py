from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os
import traceback
import gspread
from gspread import Client, Spreadsheet
from pathlib import Path


class ManipulationGoogleDrive:
    def __init__(self) -> None:
        self.drive = self.login_with_service_account()
        self.client = self.authorize_service_account()

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

        # スプレッドシートを新規作成して共有設定
        spreadsheet = self.create_spreadsheet("test desu")
        file_spreadsheet = self.drive.CreateFile({"id": spreadsheet.id})
        file_spreadsheet.FetchMetadata(fetch_all=True)

        file_spreadsheet.InsertPermission(
            {"type": "user", "role": "writer", "value": "example@example.com"},
            param={"sendNotificationEmails": False},
        )

        # 作成したスプレッドシートの配置場所を移動
        file_spreadsheet["parents"] = [{"id": "//parent id"}]
        file_spreadsheet.Upload()

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

    def authorize_service_account(self, service_account_file_path: str = "") -> Client:
        if service_account_file_path == "":
            # NOTICE: SENSITIVE INFO FILE !!!!!
            service_account_file_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "../secrets.json"
            )

        try:
            return gspread.service_account(filename=Path(service_account_file_path))

        except Exception:
            print(traceback.format_exc())

    def create_spreadsheet(
        self, spreadsheet_name: str = "default spreadsheet name"
    ) -> Spreadsheet:
        try:
            return self.client.create(spreadsheet_name)
        except Exception:
            print(traceback.format_exc())


if __name__ == "__main__":
    manipulation_google_drive = ManipulationGoogleDrive()
    manipulation_google_drive.main()
