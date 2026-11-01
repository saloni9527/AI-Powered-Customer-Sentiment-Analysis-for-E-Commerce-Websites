# MongoDB Atlas Setup Guide for SentimentPulse

## Prerequisites
- MongoDB Atlas account created
- Cluster created
- Python packages installed (`pip install -r requirements.txt`)

---

## Step 1: Get MongoDB Atlas Connection String

1. **Log in to MongoDB Atlas**
   - Visit: https://account.mongodb.com/account/login
   - Use your credentials

2. **Navigate to Clusters**
   - Click on **Clusters** in the left sidebar
   - Find your cluster

3. **Get Connection String**
   - Click **Connect** button on your cluster
   - Select **Connect your application**
   - Choose **Python** as driver and **3.12 or later** as version
   - Copy the connection string (it should look like):
     ```
     mongodb+srv://<username>:<password>@cluster-name.mongodb.net/sentiment_analyzer?retryWrites=true&w=majority
     ```

4. **Update Credentials**
   - Replace `<username>` with your MongoDB database user
   - Replace `<password>` with your MongoDB database password
   - Verify cluster name is correct

---

## Step 2: Create `.env` File

1. **Duplicate `.env.example`**
   - Copy the provided `.env.example` file
   - Rename it to `.env` in the same directory

2. **Update MONGO_URI**
   - Paste your MongoDB Atlas connection string
   - Example:
     ```
     MONGO_URI=mongodb+srv://saloni:Sec@re123@sentiment-cluster.mongodb.net/sentiment_analyzer?retryWrites=true&w=majority
     ```

3. **Update Flask Secret Key** (for production)
   - Replace `your-secret-key-change-this-in-production` with a random string
   - You can generate one with: `python -c "import os; print(os.urandom(32).hex())"`

4. **Configure Email** (optional, for password reset OTP)
   - Use Gmail, Outlook, or SendGrid
   - For Gmail (recommended):
     - Use App Passwords (not your regular password)
     - Enable 2-Factor Authentication first

---

## Step 3: Verify MongoDB Connection

Run this test script:

```python
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    mongo_client.admin.command('ping')
    print("✅ MongoDB Atlas connection successful!")
    
    # Check database
    db = mongo_client.sentiment_analyzer
    print(f"✅ Database 'sentiment_analyzer' accessed")
    print(f"✅ Collections: {db.list_collection_names()}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

Save as `test_mongo_connection.py` and run:
```bash
python test_mongo_connection.py
```

---

## Step 4: Test Sign-up and Login

1. **Start your Flask app**
   ```bash
   python app.py
   ```

2. **Open in browser**
   - Go to: http://localhost:5000/auth/signup

3. **Create a test account**
   - Fill in email, password (min 8 chars, uppercase, special char)
   - Account will be stored in MongoDB Atlas

4. **Test Login**
   - Go to: http://localhost:5000/auth/login
   - Use your test credentials

5. **Verify in MongoDB Atlas**
   - Go to Collections > sentiment_analyzer > users
   - You should see your test user document

---

## Troubleshooting

### Connection String Issues
- **Error: "Invalid credentials"** → Check username/password in connection string
- **Error: "IP not whitelisted"** → Add your IP in MongoDB Atlas Network Access
- **Error: "DNS error"** → Internet connection issue or wrong cluster name

### Common Problems

| Problem | Solution |
|---------|----------|
| Connection timeout | Check Network Access in MongoDB Atlas settings |
| Invalid credentials | Verify database user username and password (not account) |
| Database not found | Ensure URI includes `/sentiment_analyzer` |
| Wrong Python version | Use Python 3.7+ (3.10+ recommended) |

---

## File Structure After Setup

```
sentiment-analyzer/
├── app.py
├── .env                 ← Create this with MongoDB URI
├── .env.example         ← Reference template
├── requirements.txt
├── templates/
│   ├── login.html
│   ├── signup.html
│   └── ...
└── MongoDB Atlas       ← All data storage (users, analyses, reviews)
```

---

## MongoDB Collections Created Automatically

The app creates these collections when users interact:

```javascript
// users - stores signup/login data
{
  _id: ObjectId,
  email: "user@example.com",
  password_hash: "hashed_password",
  first_name: "John",
  last_name: "Doe",
  role: "user",
  created_at: "2026-04-03T..."
}

// analyses - stores sentiment analysis results
{
  _id: ObjectId,
  user_id: ObjectId,
  text: "...",
  emotion: "joy",
  confidence: 0.95,
  created_at: "2026-04-03T..."
}
```

---

## Security Notes

⚠️ **Important:**
- Never commit `.env` file to version control
- Use environment variables in production
- Rotate credentials periodically
- Keep `FLASK_SECRET_KEY` secret and long

---

## Next Steps

✅ Setup complete! Your app now has:
- User authentication (signup/login) with MongoDB
- Secure password hashing
- Email OTP for password reset
- Sentiment analysis storage per user

Enjoy your SentimentPulse app! 🚀
