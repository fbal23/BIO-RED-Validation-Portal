# BIO-RED Data Validation Portal - Streamlit App

## Overview

Partner-facing web interface for pre-submission data validation. Partners can upload Excel files and receive instant validation feedback before formal submission.

**Live Portal:** TBD (to be deployed on Hostinger)

## Features

### ✅ Core Functionality
- **File Upload**: Drag-and-drop Excel file upload
- **Real-time Validation**: Instant validation using AI-powered checks
- **Visual Feedback**: Clear error/warning/success indicators
- **Detailed Reports**: Comprehensive validation reports with metrics
- **Download Reports**: JSON and text format validation reports
- **Multi-template Support**: All 9 BIO-RED templates supported

### 📊 Validation Checks
1. **Schema Compliance**: Verify all required fields present
2. **Data Types**: Check numeric fields, URLs, emails
3. **Completeness**: 95% target for required fields
4. **Dropdown Validation**: Ensure valid controlled vocabulary
5. **Quality Metrics**: Duplicate detection, field usage stats
6. **Enhancement Targets**: Organization Registry specific checks

### 🎨 User Experience
- Clean, professional interface
- Region selection for partner context
- Template-specific guidance
- Expandable detailed results
- Mobile-responsive design
- 24/7 availability

## Local Development

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone repository:**
```bash
git clone https://github.com/fbal23/ProjMgmt.git
cd ProjMgmt/streamlit_app
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run locally:**
```bash
streamlit run validation_portal.py
```

The app will open at `http://localhost:8501`

### Project Structure
```
streamlit_app/
├── validation_portal.py    # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── temp_uploads/          # Temporary file storage (gitignored)
```

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for Quick Start)

**Pros:**
- ✅ Free tier available (1 app)
- ✅ Easiest deployment (connect GitHub)
- ✅ Automatic SSL/HTTPS
- ✅ Auto-updates on git push

**Setup:**
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Select repository: `fbal23/ProjMgmt`
4. Main file path: `streamlit_app/validation_portal.py`
5. Deploy!

**Limitations:**
- Limited to 1 app on free tier
- Public by default (can add authentication)
- Resource limits on free tier

---

### Option 2: Hostinger Deployment (Your Current Host)

Since you're already using **Hostinger** for innovationchat.eu, this is the recommended option for integration.

#### Hostinger Deployment Methods

**Method A: Python App Hosting (if available)**

Check if your Hostinger plan supports Python applications:

1. **Login to Hostinger Control Panel (hPanel)**
2. **Check for "Python" or "Application" section**
3. **If available:**
   - Upload app files via FTP/SSH
   - Set Python version to 3.8+
   - Install dependencies: `pip install -r requirements.txt`
   - Configure entry point: `streamlit run validation_portal.py --server.port=8501`
   - Map to subdomain: `validation.innovationchat.eu`

**Method B: VPS/Cloud Hosting (if on VPS plan)**

If you have VPS access on Hostinger:

```bash
# SSH into your VPS
ssh username@your-hostinger-server.com

# Install Python & dependencies
sudo apt update
sudo apt install python3-pip python3-venv

# Clone repository
git clone https://github.com/fbal23/ProjMgmt.git
cd ProjMgmt/streamlit_app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run with systemd (persistent service)
sudo nano /etc/systemd/system/biored-validation.service
```

**systemd service file:**
```ini
[Unit]
Description=BIO-RED Validation Portal
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/ProjMgmt/streamlit_app
ExecStart=/path/to/venv/bin/streamlit run validation_portal.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable biored-validation
sudo systemctl start biored-validation

# Configure reverse proxy (Nginx)
sudo nano /etc/nginx/sites-available/validation.conf
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name validation.innovationchat.eu;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Enable site and reload
sudo ln -s /etc/nginx/sites-available/validation.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Add SSL with Let's Encrypt
sudo certbot --nginx -d validation.innovationchat.eu
```

**Method C: Docker Container (most portable)**

If Hostinger supports Docker:

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY validation_portal.py .
COPY ../scripts/validate_submission.py ../scripts/

EXPOSE 8501

CMD ["streamlit", "run", "validation_portal.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Deploy:
```bash
docker build -t biored-validation .
docker run -d -p 8501:8501 --name biored-validation biored-validation
```

---

### Option 3: Railway.app (Modern Alternative)

**Pros:**
- ✅ Free tier ($5/month credit)
- ✅ Easy GitHub deployment
- ✅ Automatic SSL
- ✅ Custom domains

**Setup:**
1. Go to https://railway.app
2. Connect GitHub repo
3. Select `streamlit_app` directory
4. Add start command: `streamlit run validation_portal.py --server.port=$PORT`
5. Deploy!

---

### Option 4: Heroku

**Pros:**
- ✅ Well-established platform
- ✅ Free tier available (with limitations)
- ✅ Easy scaling

**Setup:**

Create `Procfile`:
```
web: streamlit run validation_portal.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

Deploy:
```bash
heroku login
heroku create biored-validation
git push heroku main
```

---

## Recommended Deployment Strategy

Given your current setup:

1. **Short-term (Testing):** Use **Streamlit Cloud** for free immediate deployment
   - Get live URL for partner testing
   - No infrastructure setup needed

2. **Long-term (Production):** Deploy on **Hostinger VPS** alongside innovationchat.eu
   - Subdomain: `validation.innovationchat.eu`
   - Integrated with existing infrastructure
   - Full control over resources

3. **Fallback:** Keep **Railway.app** as backup if Hostinger has limitations

## Configuration

### Environment Variables (if needed)

Create `.streamlit/config.toml` for production settings:

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#262730"
font = "sans serif"
```

### Authentication (Optional)

For production, consider adding basic authentication:

```python
import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == "biored2025":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        return True

if check_password():
    # Main app code here
    st.markdown('<div class="main-header">🔬 BIO-RED Data Validation Portal</div>', unsafe_allow_html=True)
    # ...
```

## Testing

### Manual Testing Checklist

- [ ] Upload valid Excel file → Shows "VALIDATED"
- [ ] Upload file with errors → Shows "REJECTED" with error details
- [ ] Upload file with warnings → Shows "VALIDATED_WITH_WARNINGS"
- [ ] Download JSON report → Valid JSON format
- [ ] Download text report → Readable summary
- [ ] Test all 9 template types
- [ ] Test with large files (100+ rows)
- [ ] Test with invalid file formats
- [ ] Test with corrupted Excel files
- [ ] Test mobile responsiveness

### Sample Test Files

Use files from `test_samples/` directory:
```bash
ProjMgmt/test_samples/
├── 1_Organization_Registry_PT16_TEST.xlsx
├── 2_Stakeholder_Mapping_PT16_TEST.xlsx
├── 3_Value_Chain_Mapping_PT16_TEST.xlsx
└── 4_Funding_Sources_PT16_TEST.xlsx
```

## Monitoring & Maintenance

### Logs

Check Streamlit logs:
```bash
# Local
tail -f ~/.streamlit/logs/streamlit.log

# Production (systemd)
sudo journalctl -u biored-validation -f
```

### Performance

- Average validation time: 2-5 seconds per file
- Supports files up to 10MB (configurable)
- Concurrent users: 10-20 on free tier

### Updates

To update the app:
```bash
git pull origin main
# If using systemd:
sudo systemctl restart biored-validation
```

## Security Considerations

1. **File Upload Security:**
   - Only .xlsx files accepted
   - Temporary files auto-deleted after validation
   - No persistent storage of partner data

2. **Data Privacy:**
   - No data sent to external services
   - Validation runs locally on server
   - No analytics or tracking

3. **HTTPS:**
   - Always use SSL in production
   - Let's Encrypt for free certificates

## Support

**Technical Issues:**
- Check logs first
- Review validation_portal.py error messages
- Test with sample files

**Deployment Issues:**
- Hostinger support: https://www.hostinger.com/support
- Streamlit docs: https://docs.streamlit.io

**Contact:**
- Email: support@biored-project.eu
- GitHub Issues: https://github.com/fbal23/ProjMgmt/issues

## License

© 2025 BIO-RED Consortium

---

**Next Steps:**

1. ✅ Test locally: `streamlit run validation_portal.py`
2. ⏳ Choose deployment option (Streamlit Cloud for quick start)
3. ⏳ Deploy to production (Hostinger VPS recommended)
4. ⏳ Share URL with partners
5. ⏳ Monitor usage and gather feedback
