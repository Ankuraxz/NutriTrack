# HOW TO RUN BACKEND SERVER

1. Change Directory to Right Folder
```bash
git clone https://github.com/Ankuraxz/NutriTrack.git
cd NutriTrack/Backend
```

2. Install the required packages using the following command:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Setup Environment Variables:
```bash
AZURE_STORAGE_KEY=<YOUR_AZURE_BLOB_STORAGE_KEY>
AZURE_STORAGE_CONN_STRING=<YOUR_AZURE_BLOB_STORAGE_CONN_STRING>
MONGO_URI=<YOUR_MONGO_URI>
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```

4. Run the backend server using the following command:
```bash
uvicorn main:app --reload --port 8000
```

5. The backend server will be running on `http://localhost:8000/`