# Quick Start: MongoDB Atlas Connection

## Your Current IP Address
**51.9.140.71** - You need to whitelist this in MongoDB Atlas

## Step 1: Whitelist Your IP

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Sign in to your account  
3. Click **Network Access** (left sidebar)
4. Click **Add IP Address**
5. **Choose one option:**
   - **Quick (Development)**: Select "Allow Access from Anywhere" (0.0.0.0/0)
   - **Secure (Production)**: Enter your IP: `51.9.140.71`
6. Click **Confirm**
7. Wait 1-2 minutes for changes to take effect

## Step 2: Test Connection

```bash
cd /Users/evelyn/ProofOfTalent/backend
source venv/bin/activate
python test_atlas_connection.py
```

Expected output:
```
✅ Successfully connected to MongoDB Atlas!
✅ All tests passed!
```

## Step 3: Configure Application

```bash
# Copy Atlas config to .env
cp .env.production .env
```

## Step 4: Run Your Application

```bash
python main_mongodb.py
```

Your CV documents will now be stored in **MongoDB Atlas cloud database**! 🎉

---

## Files Created

- **test_atlas_connection.py** - Test MongoDB Atlas connection
- **.env.production** - MongoDB Atlas configuration template
- **MONGODB_ATLAS_SETUP.md** - Detailed setup and troubleshooting guide

## Troubleshooting

If connection still fails after whitelisting:
- See detailed guide: `MONGODB_ATLAS_SETUP.md`
- Check cluster status in Atlas dashboard
- Verify username/password are correct
