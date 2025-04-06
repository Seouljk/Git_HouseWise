# Project Overview

This project includes:
- API integration  
- Database creation with PostgreSQL  
- Web crawling functionality  
- Google Sheets integration for real-time monitoring  

**Built with:**
- Django framework  
- PostgreSQL  
- Google Cloud Services (Sheets, Drive, Cloud Storage)

---

# Prerequisites & Installation

## 1. Install Required Tools
- PostgreSQL (includes `psql` and `pgAdmin`)  
- Django  
- Python Virtual Environment (optional but recommended)

## 2. Database Setup
- After installing PostgreSQL, create a new user and database.
- Update your `DATABASES` configuration in `housewise_app/housewise/settings.py` with your PostgreSQL credentials:

DATABASES = { 'default': { 'ENGINE': 'django.db.backends.postgresql', 'NAME': '<your_db_name>', 'USER': '<your_username>', 'PASSWORD': '<your_password>', 'HOST': 'localhost', 'PORT': '5432', } }

---

# Google Sheets Integration

## 1. Create a Google Cloud Project
- Visit: https://console.cloud.google.com/
- Navigate to: APIs & Services > Library
- Enable the following APIs:
  - Google Sheets API  
  - Google Drive API  
  - Cloud Storage API

## 2. Create Service Account & Credentials
- Go to: APIs & Services > Credentials > Create Credentials > Service Account
- Set up the account and download the JSON credentials file
- Move the file to your project's `resources/` directory

## 3. Update Django Settings
- In `housewise/settings.py`, update:

GOOGLE_SHEETS_CREDENTIALS = os.path.join(BASE_DIR, 'resources', '<your_credentials_file>.json')


## 4. Configure the Crawler
- Edit the following in `housewise_app/housewise/management/commands/crawl_prices.py`:

SHEET_NAME = "<your_google_sheet_name>" CREDENTIALS_FILE = "resources/<your_credentials_file>.json"

---

# Running the Server Locally

To run the server locally, use the following commands:

venv\Scripts\activate cd .\housewise_app
python manage.py runserver 0.0.0.0:8000

---

# Deployment (via Railway)

## 1. Create a Railway Account & Project
- Go to: https://railway.app  
- Sign up and complete setup (free $5 credit)  
- Create a new project and add a **PostgreSQL** database plugin  

## 2. Configure Environment Variables
- Copy the `DATABASE_URL` from Railway
- Add it to the `.env` file in `housewise_app/housewise_app/.env`:

DATABASE_URL=<your_railway_database_url>


## 3. Deploy the Django App
- Upload the project files to Railway
- After deployment, apply migrations:

venv\Scripts\activate cd .\housewise_app
python manage.py makemigrations python manage.py migrate


## 4. Create a Superuser
python manage.py createsuperuser

## 5. Access the Admin Panel
- Visit the deployment URL provided by Railway
- Navigate to link + `/mgagardy/` and log in with the superuser credentials
