# BIO-RED Validation Portal - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    BIO-RED VALIDATION PORTAL                │
│                  https://validation.innovationchat.eu       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      STREAMLIT WEB APP                      │
│                  (validation_portal.py)                     │
│                                                             │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │   Upload    │  │  Validation  │  │    Reporting     │  │
│  │  Component  │  │    Engine    │  │     Module       │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              VALIDATION LOGIC (Task 25.1-25.2)              │
│                  (validate_submission.py)                   │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐   │
│  │   Schema     │  │  Data Type   │  │  Completeness  │   │
│  │ Compliance   │  │  Validation  │  │    Metrics     │   │
│  └──────────────┘  └──────────────┘  └────────────────┘   │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐   │
│  │  Dropdown    │  │   Quality    │  │  Enhancement   │   │
│  │  Validation  │  │   Metrics    │  │    Targets     │   │
│  └──────────────┘  └──────────────┘  └────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    TEMPLATE SCHEMAS                         │
│                                                             │
│  1. Organization Registry   6. Interview Summary           │
│  2. Stakeholder Mapping     7. Business Case Profile       │
│  3. Value Chain Mapping     8. Trend Brief                 │
│  4. Funding Sources         9. Policy Analysis             │
│  5. Focus Group Notes                                      │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Web Interface (validation_portal.py)

**Responsibilities:**
- User interface rendering
- File upload handling
- Validation result display
- Report generation and download

**Technology:**
- Streamlit 1.28+
- Custom CSS for styling
- Responsive design

**Key Features:**
- Drag-and-drop file upload
- Real-time validation feedback
- Expandable result sections
- JSON and text report downloads

### 2. Validation Engine (validate_submission.py)

**Responsibilities:**
- Excel file parsing
- Data validation
- Error and warning generation
- Quality metrics calculation

**Technology:**
- pandas for data processing
- openpyxl for Excel handling
- Python 3.8+

**Validation Checks:**
1. Schema compliance (required fields)
2. Data type validation (numeric, URL, email)
3. Completeness metrics (95% target)
4. Dropdown value validation
5. Quality metrics (duplicates, usage)
6. Enhancement targets (Org Registry)

### 3. Template Schemas

**Definition:**
- 9 template types
- Required/optional fields
- Dropdown controlled vocabularies
- Validation rules

**Storage:**
- Embedded in validate_submission.py
- TEMPLATE_SCHEMAS dictionary

## Data Flow

```
Partner                    Streamlit App              Validation Engine
   │                            │                           │
   │──1. Select Region─────────▶│                           │
   │                            │                           │
   │──2. Select Template────────▶│                           │
   │                            │                           │
   │──3. Upload Excel File──────▶│                           │
   │                            │                           │
   │                            │──4. Save Temp File────────▶│
   │                            │                           │
   │                            │──5. Validate File─────────▶│
   │                            │                           │
   │                            │                ┌──────────┴────────┐
   │                            │                │ Parse Excel       │
   │                            │                │ Check Schema      │
   │                            │                │ Validate Data     │
   │                            │                │ Calculate Metrics │
   │                            │                └──────────┬────────┘
   │                            │                           │
   │                            │◀──6. Return Report────────│
   │                            │                           │
   │          ┌─────────────────┴──────────────┐            │
   │          │ Format Results                 │            │
   │          │ Generate Visual Display        │            │
   │          │ Create Download Reports        │            │
   │          └─────────────────┬──────────────┘            │
   │                            │                           │
   │◀──7. Display Results───────│                           │
   │                            │                           │
   │──8. Download Report────────▶│                           │
   │                            │                           │
   │◀──9. JSON/Text File────────│                           │
   │                            │                           │
   │                            │──10. Delete Temp──────────▶│
   │                            │                           │
```

## Deployment Architecture

### Streamlit Cloud (Testing)

```
GitHub Repository (fbal23/ProjMgmt)
         │
         ▼
Streamlit Cloud Platform
         │
         ├── Auto-deploy on git push
         ├── Python environment setup
         ├── Dependency installation
         └── App hosting
         │
         ▼
https://[app-name].streamlit.app
         │
         ▼
   Partner Access
```

### Hostinger VPS (Production)

```
Hostinger VPS Server
         │
         ├── Python 3.8+ Environment
         ├── Virtual Environment (venv)
         ├── Streamlit Service (systemd)
         │   └── Port 8501 (local)
         │
         ▼
Nginx Reverse Proxy
         │
         ├── SSL/TLS (Let's Encrypt)
         ├── Domain: validation.innovationchat.eu
         └── Proxy to localhost:8501
         │
         ▼
Internet (HTTPS)
         │
         ▼
   Partner Access
```

## File Structure

```
streamlit_app/
├── validation_portal.py          # Main Streamlit app (479 lines)
├── requirements.txt              # Python dependencies
├── README.md                     # Comprehensive deployment guide
├── DEPLOYMENT_QUICKSTART.md      # Quick deployment steps
├── ARCHITECTURE.md               # This file
├── TASK_25.3_COMPLETION_SUMMARY.md  # Completion summary
├── start_local.sh                # Local testing script
├── test_validation_portal.py     # Test suite
└── temp_uploads/                 # Temporary upload directory (gitignored)

Integration with:
../scripts/validate_submission.py  # Validation logic (Task 25.1-25.2)
../templates/test_samples/         # Test data files
```

## Security Considerations

### Data Privacy
- ✅ Files processed locally (no external services)
- ✅ Temporary files deleted after validation
- ✅ No persistent storage of partner data
- ✅ No analytics or tracking

### Network Security
- ✅ HTTPS required in production
- ✅ Let's Encrypt SSL certificates
- ✅ Nginx security headers

### Input Validation
- ✅ Only .xlsx files accepted
- ✅ File type verification
- ✅ Exception handling for corrupted files
- ✅ Path sanitization

### Optional Enhancements
- ⏳ Password authentication (see README)
- ⏳ Rate limiting
- ⏳ IP whitelisting (if needed)

## Performance Characteristics

### Response Times
- File upload: <1 second
- Validation: 2-5 seconds (typical)
- Report generation: <1 second

### Resource Usage
- Memory: ~200-500 MB per session
- CPU: Low (validation is I/O bound)
- Storage: Temporary only (auto-cleanup)

### Scalability
- **Streamlit Cloud Free Tier:**
  - 1 concurrent app
  - ~10-20 concurrent users
  - Adequate for 7 partners

- **Hostinger VPS:**
  - Depends on VPS specs
  - Typically 20-50 concurrent users
  - Scalable with resources

## Monitoring & Logging

### Streamlit Cloud
- Built-in dashboard
- Real-time logs
- Usage metrics
- Deployment history

### Hostinger VPS
```bash
# Service status
sudo systemctl status biored-validation

# Live logs
sudo journalctl -u biored-validation -f

# Application logs
~/.streamlit/logs/streamlit.log
```

### Key Metrics to Monitor
- Upload success rate
- Validation completion rate
- Average validation time
- Error frequency by type
- Partner usage patterns

## Integration Points

### Upstream (Input)
- **Partner Portal** (partner-portal.html)
  - Links to validation portal
  - Template downloads
  - Task information

### Downstream (Output)
- **Validation Reports**
  - JSON format (machine-readable)
  - Text format (human-readable)
  - Stored temporarily, downloaded by partner

- **Submission Workflow**
  - Pre-validated files submitted
  - Coordinator receives quality data
  - Faster approval process

## Technology Stack

```
Frontend (UI):
├── Streamlit 1.28+
├── Custom CSS
├── HTML/Markdown rendering
└── Responsive design

Backend (Processing):
├── Python 3.8+
├── pandas 2.0+
├── openpyxl 3.1+
└── validate_submission.py

Infrastructure:
├── Streamlit Cloud (testing)
├── Hostinger VPS (production)
├── Nginx (reverse proxy)
└── Let's Encrypt (SSL)

Development:
├── Git (version control)
├── GitHub (repository)
├── pytest (testing)
└── Task Master AI (project management)
```

## Error Handling Strategy

### User-Friendly Errors
```python
try:
    validate_file(uploaded_file)
except FileNotFoundError:
    → "File not found. Please upload a valid Excel file."
except ValueError:
    → "Invalid template type. Please check your file."
except Exception as e:
    → "Validation error: [specific message]"
    → "Contact support@biored-project.eu"
```

### Logging
- INFO: Successful validations
- WARNING: Validation warnings
- ERROR: Validation failures
- CRITICAL: System errors

## Future Enhancements (Optional)

### Phase 2 Features
- [ ] Batch validation (multiple files)
- [ ] Validation history tracking
- [ ] Partner-specific dashboards
- [ ] Email notification integration (Task 43-44)
- [ ] AI assistant integration (Task 45-47)

### Technical Improvements
- [ ] Caching for faster repeat validations
- [ ] Parallel processing for large files
- [ ] API endpoint for programmatic access
- [ ] Database storage of validation history

---

**Architecture Version:** 1.0
**Last Updated:** 2025-11-08
**Task:** 25.3 - Build partner-facing web interface
**Status:** ✅ COMPLETED
