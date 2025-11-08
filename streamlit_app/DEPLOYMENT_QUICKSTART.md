# BIO-RED Validation Portal - Deployment Quick Start

## 🚀 Fastest Path to Production

Since you already have **Hostinger** for innovationchat.eu, here's the recommended deployment path:

---

## Option 1: Streamlit Cloud (Recommended for Quick Testing)

**⏱ Time to Deploy: 5 minutes**

### Steps:

1. **Ensure code is pushed to GitHub:**
```bash
cd /Users/balazsfurjes/Cursor\ files/ProjMgmt
git add streamlit_app/
git commit -m "Add BIO-RED validation portal (Task 25.3)"
git push origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Click "New app"
   - Repository: `fbal23/ProjMgmt`
   - Branch: `main`
   - Main file path: `streamlit_app/validation_portal.py`
   - Click "Deploy!"

3. **Get your URL:**
   - URL will be: `https://fbal23-projmgmt-streamlit-appvalidation-portal-xxxxx.streamlit.app`
   - Share this with partners immediately!

**Pros:**
- ✅ Free forever (1 app)
- ✅ No infrastructure setup
- ✅ Auto-deploys on git push
- ✅ Built-in SSL

**Cons:**
- ❌ Public URL (but partners can access)
- ❌ Limited resources on free tier

---

## Option 2: Hostinger Subdomain (Recommended for Production)

**⏱ Time to Deploy: 30-60 minutes**

Since you have **innovationchat.eu** on Hostinger, deploy as:
**`validation.innovationchat.eu`**

### Prerequisites Check:

First, determine your Hostinger plan type:

1. **Login to Hostinger hPanel:** https://hpanel.hostinger.com
2. **Check your plan:**
   - **Shared Hosting** → Use Streamlit Cloud instead
   - **VPS/Cloud** → Follow VPS deployment below
   - **Business/Premium** → Check if Python support available

### VPS Deployment (If you have VPS):

```bash
# 1. SSH into your Hostinger VPS
ssh your_username@your_hostinger_server.com

# 2. Install Python & dependencies
sudo apt update
sudo apt install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# 3. Clone repository
cd /var/www
sudo git clone https://github.com/fbal23/ProjMgmt.git
cd ProjMgmt/streamlit_app

# 4. Create virtual environment
sudo python3 -m venv venv
sudo venv/bin/pip install -r requirements.txt

# 5. Create systemd service
sudo tee /etc/systemd/system/biored-validation.service > /dev/null <<EOF
[Unit]
Description=BIO-RED Validation Portal
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/ProjMgmt/streamlit_app
ExecStart=/var/www/ProjMgmt/streamlit_app/venv/bin/streamlit run validation_portal.py --server.port=8501 --server.address=127.0.0.1
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 6. Start service
sudo systemctl daemon-reload
sudo systemctl enable biored-validation
sudo systemctl start biored-validation
sudo systemctl status biored-validation

# 7. Configure Nginx
sudo tee /etc/nginx/sites-available/validation.innovationchat.eu > /dev/null <<EOF
server {
    listen 80;
    server_name validation.innovationchat.eu;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_read_timeout 86400;
    }
}
EOF

# 8. Enable site
sudo ln -s /etc/nginx/sites-available/validation.innovationchat.eu /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 9. Add SSL certificate
sudo certbot --nginx -d validation.innovationchat.eu

# 10. Configure DNS (in Hostinger DNS panel)
# Add A record: validation.innovationchat.eu → Your VPS IP
```

### Test Deployment:

```bash
# Check service status
sudo systemctl status biored-validation

# Check logs
sudo journalctl -u biored-validation -f

# Test locally
curl http://localhost:8501
```

---

## Option 3: Docker on Hostinger VPS

**⏱ Time to Deploy: 20 minutes**

If your Hostinger VPS has Docker:

```bash
# 1. SSH into server
ssh your_username@your_hostinger_server.com

# 2. Clone repo
cd ~
git clone https://github.com/fbal23/ProjMgmt.git
cd ProjMgmt/streamlit_app

# 3. Create Dockerfile
cat > Dockerfile <<EOF
FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY validation_portal.py .
COPY ../scripts/validate_submission.py ../scripts/

EXPOSE 8501

CMD ["streamlit", "run", "validation_portal.py", "--server.port=8501", "--server.address=0.0.0.0"]
EOF

# 4. Build and run
docker build -t biored-validation .
docker run -d -p 8501:8501 --name biored-validation --restart always biored-validation

# 5. Configure Nginx (same as VPS deployment step 7-9)
```

---

## Recommended Deployment Strategy

### For Immediate Testing (Today):
1. ✅ **Deploy to Streamlit Cloud** (5 minutes)
2. ✅ **Test with partners** using provided URL
3. ✅ **Gather feedback** over 1-2 weeks

### For Production (Week 2):
1. ✅ **Check Hostinger plan type**
2. ✅ If VPS: Deploy to `validation.innovationchat.eu`
3. ✅ If Shared: Keep Streamlit Cloud (works great!)

---

## Testing Checklist

After deployment, test:

- [ ] Upload Organization Registry file
- [ ] Upload file with errors → See error messages
- [ ] Download JSON report
- [ ] Download text report
- [ ] Test from mobile device
- [ ] Share with 1 test partner

---

## URLs After Deployment

### Streamlit Cloud:
```
https://[your-app-name].streamlit.app
```

### Hostinger VPS:
```
https://validation.innovationchat.eu
```

---

## Monitoring

### Streamlit Cloud:
- Dashboard: https://share.streamlit.io/
- View logs in real-time
- Monitor usage metrics

### Hostinger VPS:
```bash
# Service status
sudo systemctl status biored-validation

# Live logs
sudo journalctl -u biored-validation -f

# Restart if needed
sudo systemctl restart biored-validation
```

---

## Updating the App

### Streamlit Cloud:
```bash
# Just push to GitHub
git add .
git commit -m "Update validation portal"
git push origin main
# Auto-deploys in 1-2 minutes!
```

### Hostinger VPS:
```bash
# SSH and pull updates
ssh your_username@your_hostinger_server.com
cd /var/www/ProjMgmt
sudo git pull origin main
sudo systemctl restart biored-validation
```

---

## Need Help?

### Hostinger Support:
- Live chat: https://www.hostinger.com/support
- Check your plan type: hPanel → Hosting → Your plan

### Streamlit Cloud Issues:
- Docs: https://docs.streamlit.io/streamlit-community-cloud
- Community: https://discuss.streamlit.io

### BIO-RED Technical:
- GitHub Issues: https://github.com/fbal23/ProjMgmt/issues
- Email: support@biored-project.eu

---

## What We Built

**Files Created:**
- ✅ `streamlit_app/validation_portal.py` - Main Streamlit app (479 lines)
- ✅ `streamlit_app/requirements.txt` - Python dependencies
- ✅ `streamlit_app/README.md` - Full deployment guide
- ✅ `streamlit_app/start_local.sh` - Local testing script
- ✅ `streamlit_app/test_validation_portal.py` - Test suite

**Features:**
- ✅ File upload for all 9 templates
- ✅ Real-time AI validation
- ✅ Visual error/warning display
- ✅ Completeness metrics
- ✅ Downloadable reports (JSON + text)
- ✅ Mobile-responsive UI
- ✅ Regional partner selection
- ✅ Template-specific guidance

**Integration:**
- ✅ Uses existing `validate_submission.py` from Task 25.1-25.2
- ✅ Supports all TEMPLATE_SCHEMAS
- ✅ Compatible with partner-portal.html workflow

---

## Next Actions

1. **Deploy to Streamlit Cloud now** (5 min)
2. **Test with one sample file**
3. **Share URL with coordinator for review**
4. **Decide on Hostinger VPS for production**
5. **Update partner communications with validation URL**

**Ready to deploy? Run:**
```bash
cd /Users/balazsfurjes/Cursor\ files/ProjMgmt
git add streamlit_app/
git commit -m "Add BIO-RED validation portal (Task 25.3)"
git push origin main
```

Then go to https://share.streamlit.io and deploy!
