# AI Healthcare Assistant - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the AI Healthcare Assistant on localhost for development, testing, and academic purposes.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: Version 3.7 or higher
- **RAM**: 4 GB minimum, 8 GB recommended
- **Storage**: 500 MB free space
- **Browser**: Modern web browser (Chrome 80+, Firefox 75+, Safari 13+, Edge 80+)

### Recommended Requirements
- **Python**: Version 3.9 or higher
- **RAM**: 8 GB or more
- **Storage**: 1 GB free space
- **Network**: Internet connection for initial setup only

## Pre-Installation Setup

### 1. Verify Python Installation

**Windows:**
```cmd
python --version
pip --version
```

**macOS/Linux:**
```bash
python3 --version
pip3 --version
```

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Use Homebrew: `brew install python3`
- **Linux**: Use package manager: `sudo apt-get install python3 python3-pip`

### 2. Create Project Directory

```bash
# Create and navigate to project directory
mkdir ai-healthcare-assistant
cd ai-healthcare-assistant
```

### 3. Set Up Virtual Environment (Recommended)

**Windows:**
```cmd
python -m venv healthcare_env
healthcare_env\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv healthcare_env
source healthcare_env/bin/activate
```

## Installation Steps

### Step 1: Download Project Files

If you have the project as a ZIP file:
```bash
# Extract ZIP file to current directory
unzip ai-healthcare-assistant.zip
cd ai-healthcare-assistant
```

If you have access to a Git repository:
```bash
git clone <repository-url>
cd ai-healthcare-assistant
```

### Step 2: Install Python Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

**If you encounter permission errors on macOS/Linux:**
```bash
pip install --user -r requirements.txt
```

### Step 3: Verify Installation

```bash
# Check if key packages are installed
python -c "import flask, sklearn, pandas; print('All packages installed successfully')"
```

### Step 4: Initialize Database

```bash
# Initialize the SQLite database with schema and sample data
python -c "from modules.database_manager import get_db_manager; get_db_manager().initialize_database()"
```

### Step 5: Train Machine Learning Model

```bash
# Train and save the disease prediction model
python train_model.py
```

**Expected output:**
```
Training disease prediction model...
Model trained successfully with accuracy: 0.XX
Model saved to models/disease_model.pkl
```

### Step 6: Verify Installation

Run the setup verification script to ensure everything is properly configured:

```bash
python verify_setup.py
```

This script will check:
- Python version compatibility
- Required package installation
- Project file structure
- Database connectivity
- ML model availability
- Flask app functionality

### Step 7: Verify File Structure

Ensure your directory structure looks like this:
```
ai-healthcare-assistant/
├── app.py
├── requirements.txt
├── train_model.py
├── README.md
├── data/
│   ├── healthcare.db
│   ├── doctors.csv
│   ├── hospitals.csv
│   └── symptoms_diseases.csv
├── models/
│   └── disease_model.pkl
├── modules/
│   ├── __init__.py
│   ├── database_manager.py
│   ├── prediction_engine.py
│   └── [other module files]
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   └── [other template files]
└── static/
    ├── css/
    ├── js/
    └── images/
```

## Starting the Application

### Method 1: Direct Python Execution

```bash
# Start the Flask development server
python app.py
```

### Method 2: Using Flask Command

```bash
# Set Flask environment variables
export FLASK_APP=app.py
export FLASK_ENV=development

# Start Flask server
flask run
```

**Windows (Command Prompt):**
```cmd
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

### Expected Startup Output

```
Starting AI Healthcare Assistant...
Server will run on http://127.0.0.1:5000/
Press Ctrl+C to stop the server
 * Running on http://127.0.0.1:5000
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
```

## Accessing the Application

1. **Open your web browser**
2. **Navigate to**: `http://127.0.0.1:5000/` or `http://localhost:5000/`
3. **You should see**: The AI Healthcare Assistant dashboard

### First-Time Setup Verification

1. **Dashboard Loading**: Verify the main dashboard loads with navigation menu
2. **Symptom Checker**: Test symptom input and prediction functionality
3. **Database Connection**: Check that medical history page loads (may be empty initially)
4. **Static Files**: Ensure CSS styling and JavaScript functionality work properly

## Configuration Options

### Environment Variables

Create a `.env` file in the project root for custom configuration:

```bash
# .env file
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
DATABASE_PATH=data/healthcare.db
MODEL_PATH=models/disease_model.pkl
```

### Application Configuration

Edit `app.py` to modify configuration:

```python
# Configuration options
app.config['DEBUG'] = True          # Enable debug mode
app.config['HOST'] = '127.0.0.1'    # Server host
app.config['PORT'] = 5000           # Server port
```

### Database Configuration

The application uses SQLite by default. To use a different database location:

```python
# In modules/database_manager.py
DATABASE_PATH = 'custom/path/to/database.db'
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or use a different port
python app.py --port 5001
```

#### 2. Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'flask'`

**Solution**:
```bash
# Ensure virtual environment is activated
source healthcare_env/bin/activate  # macOS/Linux
healthcare_env\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### 3. Database Connection Errors

**Error**: `sqlite3.OperationalError: no such table`

**Solution**:
```bash
# Delete existing database and reinitialize
rm data/healthcare.db
python -c "from modules.database_manager import get_db_manager; get_db_manager().initialize_database()"
```

#### 4. Machine Learning Model Errors

**Error**: `FileNotFoundError: models/disease_model.pkl`

**Solution**:
```bash
# Retrain the model
python train_model.py

# Verify model file exists
ls -la models/disease_model.pkl
```

#### 5. Permission Errors

**Error**: `Permission denied`

**Solution**:
```bash
# Fix file permissions
chmod +x app.py
chmod -R 755 static/
chmod -R 755 templates/

# Or run with sudo (not recommended)
sudo python app.py
```

#### 6. Browser Compatibility Issues

**Symptoms**: Features not working, JavaScript errors

**Solution**:
- Use a modern browser (Chrome 80+, Firefox 75+, Safari 13+)
- Enable JavaScript in browser settings
- Clear browser cache and cookies
- Disable browser extensions that might interfere

### Performance Issues

#### Slow Application Startup

**Causes and Solutions**:
1. **Large dataset loading**: Reduce sample data size in CSV files
2. **Model loading**: Ensure model file is not corrupted, retrain if necessary
3. **Database initialization**: Check database file permissions and location

#### High Memory Usage

**Solutions**:
1. **Reduce model complexity**: Use simpler ML algorithms in `train_model.py`
2. **Limit data retention**: Implement data cleanup in database manager
3. **Optimize queries**: Add database indexes for frequently accessed data

### Network Issues

#### Cannot Access from Other Devices

**To allow access from other devices on the same network**:

```python
# In app.py, change host configuration
app.run(host='0.0.0.0', port=5000, debug=True)
```

**Security Warning**: Only do this in trusted networks for development purposes.

## Development Mode vs Production

### Development Mode (Current Setup)

- Debug mode enabled
- Detailed error messages
- Auto-reload on code changes
- Single-threaded server
- SQLite database

### Production Considerations

**Note**: This application is designed for academic/development use only. For production deployment, consider:

1. **Web Server**: Use Gunicorn or uWSGI instead of Flask development server
2. **Database**: Migrate to PostgreSQL or MySQL for better performance
3. **Security**: Implement proper authentication and authorization
4. **Monitoring**: Add logging and monitoring solutions
5. **Scalability**: Implement load balancing and caching

## Backup and Data Management

### Creating Backups

```bash
# Backup database
cp data/healthcare.db data/healthcare_backup_$(date +%Y%m%d).db

# Backup entire project
tar -czf healthcare_backup_$(date +%Y%m%d).tar.gz .
```

### Restoring from Backup

```bash
# Restore database
cp data/healthcare_backup_YYYYMMDD.db data/healthcare.db

# Restart application
python app.py
```

### Data Cleanup

```bash
# Clear all user data (keep schema)
python -c "
from modules.database_manager import get_db_manager
db = get_db_manager()
db.clear_user_data()
print('User data cleared')
"
```

## Monitoring and Logs

### Application Logs

Logs are printed to console by default. To save logs to file:

```bash
# Run with log file
python app.py > logs/app.log 2>&1

# Or use nohup for background execution
nohup python app.py > logs/app.log 2>&1 &
```

### Health Checks

Create a simple health check script:

```python
# health_check.py
import requests
import sys

try:
    response = requests.get('http://127.0.0.1:5000/', timeout=5)
    if response.status_code == 200:
        print("✓ Application is healthy")
        sys.exit(0)
    else:
        print(f"✗ Application returned status {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Health check failed: {e}")
    sys.exit(1)
```

## Updating the Application

### Updating Dependencies

```bash
# Update all packages to latest versions
pip install --upgrade -r requirements.txt

# Or update specific packages
pip install --upgrade flask scikit-learn pandas
```

### Updating Application Code

1. **Backup current installation**
2. **Download new version**
3. **Compare configuration files**
4. **Update database schema if needed**
5. **Retrain ML model if data format changed**
6. **Test functionality**

## Security Considerations

### Local Development Security

1. **Firewall**: Ensure firewall blocks external access to port 5000
2. **Network**: Only run on localhost (127.0.0.1) unless specifically needed
3. **Data**: Regularly backup and secure database files
4. **Updates**: Keep Python and dependencies updated

### Data Privacy

- All data remains on localhost
- No external network connections for core functionality
- User sessions are isolated
- No personal data is transmitted externally

## Support and Maintenance

### Regular Maintenance Tasks

1. **Weekly**: Check application logs for errors
2. **Monthly**: Update Python dependencies
3. **Quarterly**: Backup database and project files
4. **As needed**: Retrain ML model with new data

### Getting Help

1. **Check logs**: Review console output for error messages
2. **Verify setup**: Ensure all installation steps were completed
3. **Test components**: Use individual module tests to isolate issues
4. **Documentation**: Refer to README.md and API documentation

### Performance Monitoring

```bash
# Monitor resource usage
top -p $(pgrep -f "python app.py")

# Check disk usage
du -sh data/ models/ static/

# Monitor network connections
netstat -an | grep :5000
```

---

**Disclaimer**: This deployment guide is for educational and development purposes only. The application should not be used for actual medical diagnosis or treatment. Always consult qualified healthcare professionals for medical advice.