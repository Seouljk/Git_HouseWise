import gspread
from oauth2client.service_account import ServiceAccountCredentials

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Your command description'

    def handle(self, *args, **kwargs):
        # Your command logic here
        pass

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDENTIALS_FILE = r'C:\Git_HouseWise\Athesis\resources\secure-stone-412401-bef03f4658ac.json'
SHEET_NAME = 'Housewise Crawler Results'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
client = gspread.authorize(credentials)
sheet = client.open(SHEET_NAME).sheet1
sheet.append_row(['Test Material', 'Test Price', 'Test Website', '2024-01-01 00:00:00'])
print("Test row added to Google Sheets.")
