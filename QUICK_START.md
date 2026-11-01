# Quick MongoDB Atlas Setup - 5 Steps

## 🚀 Quick Start

### Step 1: Get Your Connection String
```
1. Go to https://account.mongodb.com (login)
2. Click Clusters → Connect
3. Select "Connect your application"
4. Copy the connection string
```

### Step 2: Create `.env` File
```bash
# Copy the template
copy .env.example .env
```

### Step 3: Add Your MongoDB URI
Edit `.env` and replace:
```
MONGO_URI=mongodb+srv://YOUR_USERNAME:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/sentiment_analyzer?retryWrites=true&w=majority
```

**Important:** 
- `YOUR_USERNAME` = MongoDB database user (NOT your account email)
- `YOUR_PASSWORD` = Database user password (special chars must be URL-encoded, e.g., @ = %40)
- `YOUR_CLUSTER` = Your cluster name (e.g., sentiment-cluster)

### Step 4: Test Connection
```bash
python test_mongodb_connection.py
```

Expected output:
```
✅ All tests passed! MongoDB is correctly configured.
```

### Step 5: Test Sign-up & Login
```bash
# Start Flask app
python app.py

# In browser:
# - Signup: http://localhost:5000/auth/signup
# - Login: http://localhost:5000/auth/login
```

---

## 📋 Your App Already Has:

✅ **MongoDB Integration** - User data stored in MongoDB  
✅ **Signup Page** - Creates users in MongoDB with hashed passwords  
✅ **Login Page** - Authenticates against MongoDB users  
✅ **Password Hashing** - Using werkzeug.security  
✅ **Session Management** - Stores user info after login  

---

## 🔒 MongoDB Collections

When users signup/login, this structure is created:

```javascript
// sentiment_analyzer.users
{
  "_id": ObjectId("..."),
  "email": "user@example.com",
  "password_hash": "pbkdf2:sha256:...",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user",
  "created_at": "2026-04-03T..."
}
```

---

## ⚠️ Common Errors & Fixes

| Error | Fix |
|-------|-----|
| "auth failed" | Wrong username/password for DB user |
| "connect ENOTFOUND" | IP not whitelisted in Network Access |
| "SyntaxError in URI" | Special characters need URL encoding (@ = %40, ! = %21) |
| "Permission denied" | Database user needs read/write permissions |

---

## 🎯 What's Connected

```
signup.html ─→ POST /auth/signup ─→ Users stored in MongoDB
                                      ↓
                                    users_collection.insert_one()

login.html ─→ POST /auth/login ─→ Check MongoDB users_collection
                                   ↓
                                validate_password() + session["user_id"]
```

---

## 📚 Files Created

1. **`.env.example`** - Template with all configuration options
2. **`MONGODB_SETUP.md`** - Detailed setup guide  
3. **`test_mongodb_connection.py`** - Connection test script
4. **`QUICK_START.md`** - This file

---

## 🆘 Still Need Help?

Run the test script:
```bash
python test_mongodb_connection.py
```

It will tell you exactly what's wrong and how to fix it!

---

**Ready? Start with Step 1 above and follow through Step 5.** ✨
