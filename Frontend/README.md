# Getting Started with Frontend

1. Change Directory to Right Folder
```bash
git clone https://github.com/Ankuraxz/NutriTrack.git
cd NutriTrack/Frontend
```

2. Install the required packages using the following command:
```bash
npm install
```

3. Add Environment Variables:
```bash
nano .env
REACT_APP_BASE_URL=<Deployment Link>
REACT_APP_SUPABASE_URL=<YOUR_SUPABASE_URL>
REACT_APP_SUPABASE_KEY=<YOUR_SUPABASE_KEY>
BASE_BACKEND_URL=<YOUR_BACKEND_URL>
REACT_APP_GOOGLE_CALLBACK_URL=<YOUR_GOOGLE_CALLBACK_URL>
REACT_APP_SUPABASE_KEY=<YOUR_SUPABASE_KEY>
```

4. Run the frontend server using the following command:
```bash
npm start
```

5. The frontend server will be running on `http://localhost:3000/`