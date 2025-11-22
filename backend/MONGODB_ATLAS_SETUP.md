# MongoDB Atlas Setup Guide

## Connection Details
- **Cluster**: proofoftalent.pkhflyz.mongodb.net
- **Username**: evelynedjere_db_user
- **Database**: proof_of_talent
- **Connection String**: `mongodb+srv://evelynedjere_db_user:AQOADjJfYVQE19dV@proofoftalent.pkhflyz.mongodb.net/`

## ⚠️ Connection Issue Detected

The connection test failed. This is most commonly caused by **IP address not being whitelisted** in MongoDB Atlas.

## Fix: Whitelist Your IP Address

### Option 1: Allow Access from Anywhere (Development Only)
1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Sign in to your account
3. Navigate to your cluster: **ProofOfTalent**
4. Click **Network Access** in the left sidebar
5. Click **Add IP Address**
6. Select **Allow Access from Anywhere** (0.0.0.0/0)
7. Click **Confirm**
8. Wait 1-2 minutes for changes to propagate

### Option 2: Whitelist Your Current IP (Recommended for Production)
1. Get your current IP address:
   ```bash
   curl ifconfig.me
   ```
2. Go to MongoDB Atlas → **Network Access**
3. Click **Add IP Address**
4. Enter your IP address
5. Click **Confirm**

## Test Connection

After whitelisting your IP, test the connection:

```bash
cd backend
source venv/bin/activate
python test_atlas_connection.py
```

Expected output:
```
✅ Successfully connected to MongoDB Atlas!
✅ MongoDB version: X.X.X
✅ Insert successful!
✅ Read successful!
✅ All tests passed!
```

## Update Your Environment

Once the connection test passes:

```bash
# Copy the production config to .env
cp .env.production .env

# Or manually add to your .env file:
echo 'MONGODB_URL=mongodb+srv://evelynedjere_db_user:AQOADjJfYVQE19dV@proofoftalent.pkhflyz.mongodb.net/?appName=ProofOfTalent' >> .env
echo 'MONGODB_DATABASE=proof_of_talent' >> .env
```

## Start Your Application

```bash
# Run the MongoDB-based API
python main_mongodb.py
```

The API will now store all CV uploads and analysis results in your MongoDB Atlas cloud database!

## Verify in MongoDB Atlas

1. Go to [MongoDB Atlas](https://cloud.mongodb.com/)
2. Navigate to **Collections**
3. Select database: `proof_of_talent`
4. You should see collections:
   - `cv_analyses` - CV uploads and analysis results
   - `model_metrics` - ML model performance metrics

## Troubleshooting

### Still can't connect?

1. **Check internet connection**
   ```bash
   ping google.com
   ```

2. **Verify credentials**
   - Username: `evelynedjere_db_user`
   - Password: `AQOADjJfYVQE19dV`

3. **Check cluster status**
   - Ensure cluster is running in Atlas dashboard
   - Check for any maintenance notifications

4. **Firewall/VPN issues**
   - Disable VPN temporarily
   - Check corporate firewall settings
   - Ensure port 27017 is not blocked

5. **View detailed error**
   ```bash
   python test_atlas_connection.py 2>&1 | tee connection_log.txt
   ```

## Security Notes

> **⚠️ IMPORTANT**: The connection string contains your password. Never commit it to Git!

- `.env` is in `.gitignore` ✅
- Use `.env.production` as a template only
- For production deployment, use environment variables
- Rotate passwords periodically in Atlas

## Next Steps After Successful Connection

1. ✅ Test connection: `python test_atlas_connection.py`
2. ✅ Update `.env` with Atlas connection string
3. ✅ Run application: `python main_mongodb.py`
4. ✅ Upload a test CV through the API
5. ✅ Verify data in MongoDB Atlas dashboard
