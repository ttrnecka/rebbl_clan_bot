"""Imperiumr Sheet Service helpers"""
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

ROOT = os.path.dirname(__file__)

# use CREDS to create a client to interact with the Google Drive API
SCOPE = ['https://spreadsheets.google.com/feeds']
CREDS = ServiceAccountCredentials.from_json_keyfile_name(
    os.path.join(ROOT, 'client_secret.json'), SCOPE)


class SheetService:
    """Namespace class"""
    SPREADSHEET_ID="1zvXMjDOuFi73-Ni2uRe5bvhEcIwNWlA6CkZ_PBwdPV4"
    # dev spreadsheet below
    #SPREADSHEET_ID = "1KxgA8wD2GS7VKCePvJkrlQCprwONMU8x31VS3n1F0Xk"
    IMPORT_SHEET="TheBot"

    _matches = []

    @classmethod
    def matches(cls, refresh=False):
        """Returns torunaments from the sheet"""
        if not cls._matches or refresh:
            client = gspread.authorize(CREDS)
            sheet = client.open_by_key(cls.SPREADSHEET_ID).worksheet(cls.IMPORT_SHEET)
            cls._matches = sheet.get_all_records()
        return cls._matches

    @classmethod
    def append_match(cls, line):
        client = gspread.authorize(CREDS)
        sheet = client.open_by_key(cls.SPREADSHEET_ID)
        sheet.values_append(
            f'{cls.IMPORT_SHEET}!A1', 
            params={'valueInputOption': 'RAW'}, 
            body={'values': [line]}
        )

#if __name__ == "__main__":
