# Google Sheets Integration Setup

## Step 1: Create Google Cloud Project & Service Account

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create a new project** or select existing one
3. **Enable Google Sheets API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

## Step 2: Create Service Account

1. **Go to "APIs & Services" > "Credentials"**
2. **Click "Create Credentials" > "Service Account"**
3. **Fill in details**:
   - Service account name: `homeus-scraper`
   - Description: `Service account for Homeus property scraper`
4. **Click "Create and Continue"**
5. **Skip role assignment** (click "Continue")
6. **Click "Done"**

## Step 3: Generate Service Account Key

1. **Click on the created service account**
2. **Go to "Keys" tab**
3. **Click "Add Key" > "Create new key"**
4. **Select "JSON" format**
5. **Click "Create"**
6. **Download the JSON file**
7. **Rename it to `google_credentials.json`**
8. **Move it to the `config/` folder in your project**

## Step 4: Share Google Sheet with Service Account

1. **Open your Google Sheet**: https://docs.google.com/spreadsheets/d/1py3r-yJr0MQ5bIK8E-esEt_AVkn2eCd62OB0g37-i9E/edit
2. **Click "Share" button**
3. **Add the service account email** (found in the JSON file, looks like: `homeus-scraper@your-project.iam.gserviceaccount.com`)
4. **Set permission to "Editor"**
5. **Click "Send"**

## Step 5: Test the Integration

Run the scraper to test:

```bash
# Activate virtual environment
source venv/bin/activate

# Run once to test
python src/main.py --config config/config.yaml --once
```

## Expected Result

The scraper will:

1. Find new properties from SS.ge and MyHome.ge
2. Save them to the SQLite database
3. Export new properties to your Google Sheet with columns:
   - Property ID
   - Title
   - Price
   - Currency
   - Location
   - Size (m²)
   - Rooms
   - Property Type
   - Description
   - Images Count
   - Source URL
   - Detail URL
   - Scraped At
   - Status

## Troubleshooting

### Common Issues:

1. **"Permission denied" error**:

   - Make sure you shared the sheet with the service account email
   - Check that the service account has "Editor" permissions

2. **"File not found" error**:

   - Ensure `google_credentials.json` is in the `config/` folder
   - Check the file path in `config.yaml`

3. **"Worksheet not found" error**:

   - Make sure the worksheet name in config matches your sheet
   - Default is "Sheet1" - change if your sheet has a different name

4. **API not enabled**:
   - Go to Google Cloud Console
   - Enable Google Sheets API for your project

### Service Account Email Location

Your service account email is in the `google_credentials.json` file:

```json
{
  "client_email": "homeus-scraper@your-project.iam.gserviceaccount.com",
  ...
}
```

## Security Notes

- Keep `google_credentials.json` secure and never commit it to version control
- The `.gitignore` should include `config/google_credentials.json`
- Only share the Google Sheet with the specific service account email
