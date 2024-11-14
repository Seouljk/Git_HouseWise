import os
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import pickle
import time
import re

# Define Google Sheets setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SHEET_NAME = 'Housewise Crawler Results'  # Update with your Google Sheet name
CREDENTIALS_FILE = r'C:\Git_HouseWise\Athesis\resources\secure-stone-412401-bef03f4658ac.json'  # Your Google credentials

# Cache expiration (1 hour)
CACHE_EXPIRATION = 60  # in seconds
CACHE_FILE = 'crawler_cache.pkl'

class Command(BaseCommand):
    help = 'Run web crawler to get construction material prices and update Google Sheets'

    def handle(self, *args, **kwargs):
        # Load Google Sheets credentials
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(credentials)
        sheet = client.open(SHEET_NAME).sheet1  

        # Load materials from Google Sheets
        material_sheet = client.open(SHEET_NAME).worksheet('MATERIALS')
        materials_data = material_sheet.get_all_values()  # Get all material data (ID and name)

        # Updated MATERIALS dictionary to include alternate names
        MATERIALS = {
            row[0]: {
                'material_name': row[1].strip().lower(),
                'alt_name1': row[2].strip().lower() if len(row) > 2 else '',
                'alt_name2': row[3].strip().lower() if len(row) > 3 else ''
            } 
            for row in materials_data if row[0] and row[1]
        }

        # Load links from specific sheets

        philcon_links = client.open(SHEET_NAME).worksheet('PHILCON LINKS').col_values(1)
        citihardware_links = client.open(SHEET_NAME).worksheet('CITIHARDWARE').col_values(1)
        pinastoolsph_links = client.open(SHEET_NAME).worksheet('PINASHARDWARE').col_values(1)
        constph_links = client.open(SHEET_NAME).worksheet('CONSTPH/PB').col_values(1)
        constructph_links = client.open(SHEET_NAME).worksheet('CONSTRUCTPH').col_values(1)
        pinoybuilders_links = client.open(SHEET_NAME).worksheet('CONSTPH/PB').col_values(3)

        # Initialize cache
        cache = self.load_cache()

        # Scraping logic
        self.stdout.write(f"Scraping Citihardware links...")
        self.scrape_website_links(citihardware_links, sheet, cache, MATERIALS, self.scrape_citihardware)

        self.stdout.write(f"Scraping Pinastoolsph links...")
        self.scrape_website_links(pinastoolsph_links, sheet, cache, MATERIALS, self.scrape_pinastoolsph)

        self.stdout.write(f"Scraping Constph links...")
        self.scrape_website_links(constph_links, sheet, cache, MATERIALS, self.scrape_constph)

        # self.stdout.write(f"Scraping Constructph links...")
        # self.scrape_website_links(constructph_links, sheet, cache, MATERIALS, self.scrape_constructph)

        self.stdout.write(f"Scraping PinoyBuilders links...")
        self.scrape_website_links(pinoybuilders_links, sheet, cache, MATERIALS, self.scrape_pinoybuilders)

        self.stdout.write(f"Scraping Philcon links...")
        self.scrape_website_links(philcon_links, sheet, cache, MATERIALS, self.scrape_philcon)
        
        # Ensure date is recorded in Google Sheets, even if no data was added
        self.ensure_date_entry(sheet)

        # Save cache after scraping
        self.save_cache(cache)
        self.stdout.write('Scraping complete and data updated in Google Sheets.')
  
    def scrape_citihardware(self, soup, url, sheet, materials):
        products = soup.find_all('h2', class_='h3 product-title')
        prices = soup.find_all('span', itemprop='price')
        
        for product, price in zip(products, prices):
            description_text = product.text.strip().lower()
            for material_id, material_names in materials.items():
                material_name = material_names['material_name']
                alt_name1 = material_names.get('alt_name1', '')
                alt_name2 = material_names.get('alt_name2', '')
                if (
                    re.search(re.escape(material_name), description_text) or
                    (alt_name1 and re.search(re.escape(alt_name1), description_text)) or
                    (alt_name2 and re.search(re.escape(alt_name2), description_text))
                    ):
                    try:
                        price = price.text.strip()
                        self.stdout.write(f'Scraped {material_name}: {price} from {url}')
                        self.update_google_sheet(sheet, material_id, material_name, price, url)
                        break  # Stop after the first match is found for the row
                    except Exception as e:
                        self.stdout.write(f'Error scraping {material_name} from {url}: {str(e)}')

    def scrape_pinastoolsph(self, soup, url, sheet, materials):
        """Scrape Pinastoolsph for material prices."""
        rows = soup.find_all('tr')
        for row in rows:
            material_description = row.find('td')
            if material_description:
                description_text = material_description.text.strip().lower()

                for material_id, material_names in materials.items():
                    material_name = material_names['material_name']
                    alt_name1 = material_names.get('alt_name1', '')
                    alt_name2 = material_names.get('alt_name2', '')
                    # Match material name using regex for partial matching
                    if (
                        re.search(re.escape(material_name), description_text) or
                        (alt_name1 and re.search(re.escape(alt_name1), description_text)) or
                        (alt_name2 and re.search(re.escape(alt_name2), description_text))
                    ):
                        try:
                            price = row.find_all('td')[-1].text.strip()
                            self.stdout.write(f'Scraped {material_name}: {price} from {url}')
                            self.update_google_sheet(sheet, material_id, material_name, price, url)
                            break  # Move to the next row once a material is matched
                        except Exception as e:
                            self.stdout.write(f'Error scraping {material_names["material_name"]} from {url}: {str(e)}')

    def scrape_constph(self, soup, url, sheet, materials):
        """Scrape Const.ph for material prices."""
        products = soup.find_all('h2', class_='woocommerce-loop-product__title')
        prices = soup.find_all('span', class_='price')
        
        for product, price in zip(products, prices):
            description_text = product.text.strip().lower()
            for material_id, material_names in materials.items():
                material_name = material_names['material_name']
                alt_name1 = material_names.get('alt_name1', '')
                alt_name2 = material_names.get('alt_name2', '')
                if (
                    re.search(re.escape(material_name), description_text) or
                    (alt_name1 and re.search(re.escape(alt_name1), description_text)) or
                    (alt_name2 and re.search(re.escape(alt_name2), description_text))
                ):
                    try:
                        price = price.text.strip()
                        self.stdout.write(f'Scraped {material_name}: {price} from {url}')
                        self.update_google_sheet(sheet, material_id, material_name, price, url)
                        break  # Stop after the first match is found for the row
                    except Exception as e:
                        self.stdout.write(f'Error scraping {material_name} from {url}: {str(e)}')

    def scrape_constructph(self, soup, url, sheet, materials):
        """Scrape Constructph for material prices."""
        rows = soup.find_all('tr')  # Find all table rows

        for row in rows:
            tds = row.find_all('td')  # Get all <td> elements in the row
            if not tds:
                continue  # Skip empty rows

            description_text = tds[0].text.strip().lower()  # Use the first <td> as description

            for material_id, material_names in materials.items():
                material_name = material_names['material_name']
                alt_name1 = material_names.get('alt_name1', '')
                alt_name2 = material_names.get('alt_name2', '')

                # Check for matching material name or alternate names
                if (re.search(re.escape(material_name), description_text) or
                    (alt_name1 and re.search(re.escape(alt_name1), description_text)) or
                    (alt_name2 and re.search(re.escape(alt_name2), description_text))):
                    
                    try:
                        price = tds[-1].text.strip()  # Get the last <td> for the price
                        self.stdout.write(f'Scraped {material_name}: {price} from {url}')
                        self.update_google_sheet(sheet, material_id, material_name, price, url)
                        break  # Move to the next row once a material is matched
                    except Exception as e:
                        self.stdout.write(f'Error scraping {material_name} from {url}: {str(e)}')

    def scrape_pinoybuilders(self, soup, url, sheet, materials):
        """Scrape PinoyBuilders for material prices."""
        rows = soup.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if columns and len(columns) == 3:
                description_text = columns[0].text.strip().lower()
                for material_id, material_names in materials.items():
                    material_name = material_names['material_name']
                    alt_name1 = material_names.get('alt_name1', '')
                    alt_name2 = material_names.get('alt_name2', '')
                    if (
                        re.search(re.escape(material_name), description_text) or
                        (alt_name1 and re.search(re.escape(alt_name1), description_text)) or
                        (alt_name2 and re.search(re.escape(alt_name2), description_text))
                    ):
                        try:
                            price = columns[2].text.strip()
                            self.stdout.write(f'Scraped {material_name}: {price} from {url}')
                            self.update_google_sheet(sheet, material_id, material_name, price, url)
                            break  # Stop after the first match is found for the row
                        except Exception as e:
                            self.stdout.write(f'Error scraping {material_name} from {url}: {str(e)}')

    def scrape_philcon(self, soup, url, sheet, materials):
        """Scrape material prices from the HTML soup."""
        rows = soup.find_all('tr')
        for row in rows:
            material_description = row.find('td')
            if material_description:
                description_text = material_description.text.strip().lower()

                for material_id, material_names in materials.items():
                    material_name = material_names['material_name']
                    alt_name1 = material_names.get('alt_name1', '')
                    alt_name2 = material_names.get('alt_name2', '')

                    # Match material name using regex for partial matching
                    if  (
                            re.search(re.escape(material_name), description_text) or
                            (alt_name1 and re.search(re.escape(alt_name1), description_text)) or
                            (alt_name2 and re.search(re.escape(alt_name2), description_text))
                        ):
                        try:
                            price = row.find_all('td')[-1].text.strip()
                            self.stdout.write(f'Scraped {material_name}: {price} from {url}')
                            self.update_google_sheet(sheet, material_id, material_name, price, url)
                            break  # Stop after the first match is found for the row
                        except Exception as e:
                            self.stdout.write(f'Error scraping {material_name} from {url}: {str(e)}')

    def scrape_website_links(self, links, sheet, cache, materials, scrape_function):
        """Scrapes the list of provided links for material prices."""
        for link in links:
            if not link.startswith('http'):
                continue  # Skip invalid URLs
            self.stdout.write(f"Scraping {link}...")
            if self.is_cached(link, cache):
                self.stdout.write(f'Loading {link} from cache.')
                continue
            try:
                response = requests.get(link)
                if response.status_code != 200:
                    self.stdout.write(f"Failed to load {link}")
                    continue
                soup = BeautifulSoup(response.content, 'html.parser')
                scrape_function(soup, link, sheet, materials)
                cache[link] = {'time': datetime.now(), 'content': response.content}
            except Exception as e:
                self.stdout.write(f'Error scraping {link}: {str(e)}')
            time.sleep(10)  # Delay between requests

    def update_google_sheet(self, sheet, material_id, material_name, price, website):
        """Updates the Google Sheet with scraped data."""
        try:
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            response = sheet.append_row([material_id, material_name, price, website, current_date])
            self.stdout.write(f'Updated Google Sheets with {material_name} price: {price} from {website}')
        except Exception as e:
            self.stdout.write(f"Error updating Google Sheets: {str(e)}")

    def ensure_date_entry(self, sheet):
        """Ensures that a date entry is added to the Google Sheet even if no data is scraped."""
        try:
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sheet.append_row(['No data', 'No data', 'No data', 'No data', current_date])
            self.stdout.write('Added date entry to Google Sheets with no new data.')
        except Exception as e:
            self.stdout.write(f"Error adding date entry: {str(e)}")

    def is_cached(self, url, cache):
        """Checks if the URL is cached and still valid."""
        if url in cache:
            cached_time = cache[url]['time']
            if datetime.now() - cached_time < timedelta(seconds=CACHE_EXPIRATION):
                return True
        return False

    def load_cache(self):
        """Loads the cache from a file."""
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'rb') as f:
                return pickle.load(f)
        return {}

    def save_cache(self, cache):
        """Saves the cache to a file."""
        with open(CACHE_FILE, 'wb') as f:
            pickle.dump(cache, f)