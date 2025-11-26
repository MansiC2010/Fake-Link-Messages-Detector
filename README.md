# AI-Based Fake Message and Link Detection System

An intelligent machine learning system that uses AI to detect fake messages and malicious links by analyzing their characteristics. Works for ALL links and messages, not just known domains - the AI analyzes URL structure, patterns, and features to determine if something is fake or legitimate.

[![GitHub](https://img.shields.io/badge/GitHub-madhurakulkarni24-blue)](https://github.com/madhurakulkarni24/Fake-Link-detector)

**Repository:** [https://github.com/madhurakulkarni24/Fake-Link-detector](https://github.com/madhurakulkarni24/Fake-Link-detector)
[![Python](https://img.shields.io/badge/Python-3.7+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## Features

- **AI-Powered Detection**: Uses machine learning to analyze ANY link or message - not limited to known domains
- **Intelligent Analysis**: Analyzes 36 URL features and 31 message features to determine authenticity
- **Works for All Links**: Detects fake/legitimate for any URL, not just Google, Facebook, etc.
- **High Accuracy**: Ensemble ML models (Random Forest + Gradient Boosting) with 85%+ accuracy
- **Characteristic-Based**: Analyzes URL structure, patterns, entropy, keywords, and more
- **Detailed Explanations**: Provides clear reasons why a link or message is flagged as fake or legitimate
- **Detection History Database**: Automatically logs every detection (links and messages) into MySQL so you can inspect data from MySQL Workbench

## Installation

### Automatic Setup (Recommended)

**For Windows:**

1. **Using Command Prompt:**
   ```bash
   setup.bat
   ```

2. **Using PowerShell:**
   ```powershell
   .\setup.ps1
   ```

3. **Using Python (Cross-platform):**
   ```bash
   python setup.py
   ```

This will automatically:
- Create a virtual environment (`venv`)
- Install all required dependencies
- Set up the project structure

### Manual Setup

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   
   **Windows (Command Prompt):**
   ```bash
   venv\Scripts\activate
   ```
   
   **Windows (PowerShell):**
   ```powershell
   venv\Scripts\Activate.ps1
   ```
   
   **Linux/Mac:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Quick Activation Scripts

After setup, you can use the quick activation scripts:

**Windows Command Prompt:**
```bash
activate_env.bat
```

**Windows PowerShell:**
```powershell
.\activate_env.ps1
```

## Quick Start

### Configure MySQL (required for detection history)

Set these environment variables before running the app. **Do not append `:3306` to the host**—use `MYSQL_PORT` for the port number.

**PowerShell:**
```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_PORT="3306"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="root"
$env:MYSQL_DATABASE="fake_detection_db"
```

**Command Prompt:**
```bash
set MYSQL_HOST=localhost
set MYSQL_PORT=3306
set MYSQL_USER=root
set MYSQL_PASSWORD=root
set MYSQL_DATABASE=fake_detection_db
```

### Option 1: Web Interface (Recommended - Beautiful UI!)

1. **Train the models** (first time only):
   ```bash
   python train_models.py
   ```

2. **Start the web interface**:
   ```bash
   python run_ui.py
   ```
   Or use: `start_ui.bat` (Windows CMD) or `start_ui.ps1` (PowerShell)

3. **Open your browser**: http://localhost:5000
4. **Every detection is saved to MySQL automatically**

### Option 2: Command Line

1. **Train the models**:
   ```bash
   python train_models.py
   ```

2. **Run simple detection**:
   ```bash
   python simple_detect.py
   ```

3. **Or use command line tool**:
   ```bash
   python quick_detect.py link "https://example.com"
   python quick_detect.py message "Your message here"
   ```

## Usage

### Using the Detector in Your Code

```python
from fake_detector import FakeDetector

# Initialize detector
detector = FakeDetector()

# Detect fake URL
url_result = detector.detect_url('http://bit.ly/suspicious-link')
print(f"Is Fake: {url_result['is_fake']}")
print(f"Confidence: {url_result['confidence']:.1%}")
for reason in url_result['reasons']:
    print(f"  - {reason}")

# Detect fake message
message_result = detector.detect_message('URGENT! Click here NOW to verify!')
print(f"Is Fake: {message_result['is_fake']}")
print(f"Confidence: {message_result['confidence']:.1%}")
for reason in message_result['reasons']:
    print(f"  - {reason}")
```

### Analytics Dashboard (Graphs)

1. Configure MySQL env vars (see above).
2. Run `python run_ui.py` and open http://localhost:5000.
3. Scroll to **Detection Analytics**.
4. Pick a dataset (Fake Links / Legitimate Links / Fake Messages / Legitimate Messages).
5. Choose a chart type (Bar, Histogram, Scatter, Pie, Box, Line).
6. Click **Generate Graph** – the server uses Matplotlib + Seaborn to render a chart based on live MySQL data.

## Detection Database (MySQL Workbench Ready)

- All detections (links + messages) are automatically stored in a **MySQL database** so you can inspect them directly in MySQL Workbench.
- The database and tables are auto-created on first run (default database name: `fake_detection_db`).
- Configure the MySQL connection using environment variables **before** running the app or CLI:

| Variable          | Default Value            |
|-------------------|-------------------------|
| `MYSQL_HOST`      | `localhost`             |
| `MYSQL_PORT`      | `3306`                  |
| `MYSQL_USER`      | `root`                  |
| `MYSQL_PASSWORD`  | `password`              |
| `MYSQL_DATABASE`  | `fake_detection_db`     |

**Example (PowerShell):**
```powershell
$env:MYSQL_HOST="localhost"
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="yourStrongPassword"
$env:MYSQL_DATABASE="fake_detection_db"
```

**Example (Linux/macOS):**
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=yourStrongPassword
export MYSQL_DATABASE=fake_detection_db
```

### View data in MySQL Workbench
1. Open MySQL Workbench, connect to your server.
2. Select the database (default `fake_detection_db`).
3. Run:
   ```sql
   SELECT * FROM detections ORDER BY created_at DESC;
   ```
4. Every detection (from web UI or CLI) will be visible with type, content, status, reasons, confidence, and timestamp.

## How It Works

### URL Detection Features

The system analyzes URLs for:

- **Domain Analysis**: TLD legitimacy, domain length, IP addresses
- **URL Structure**: Length, path depth, query parameters
- **Suspicious Patterns**: Short URL services, suspicious keywords
- **Security Indicators**: HTTPS usage, encryption
- **Entropy Analysis**: Randomness measurement (obfuscated URLs)
- **Character Analysis**: Special characters, ratios, patterns

### Message Detection Features

The system analyzes messages for:

- **Linguistic Patterns**: Suspicious phrases, urgency language
- **Content Analysis**: Financial keywords, authority impersonation
- **Structure Analysis**: Capitalization, punctuation, repetition
- **URL Presence**: Embedded links in messages
- **Spam Indicators**: Typo patterns, word repetition
- **Entropy**: Text randomness measurement

### Machine Learning Models

- **Ensemble Approach**: Combines Random Forest and Gradient Boosting classifiers
- **Voting Classifier**: Uses soft voting for probability-based predictions
- **Feature Scaling**: StandardScaler for optimal model performance
- **High Accuracy**: Trained on diverse synthetic datasets

## Example Output

### URL Detection

```
URL: http://bit.ly/verify-account-now

Status: 🚨 FAKE
Confidence: 95.2%

Reasons:
  1. Detected as FAKE with 95.2% confidence.
  2. ⚠️ Contains a URL shortener (bit.ly, tinyurl, etc.) which can hide malicious destinations.
  3. ⚠️ Contains 3 suspicious keywords (verify, click, account, etc.).
  4. ⚠️ Does not use HTTPS encryption, which is a security risk.
```

### Message Detection

```
Message: URGENT! Your account has been SUSPENDED! Click here NOW to verify!

Status: 🚨 FAKE
Confidence: 98.5%

Reasons:
  1. Detected as FAKE with 98.5% confidence.
  2. ⚠️ Contains 2 suspicious phrase(s) like 'click here', 'act now', 'verify account'.
  3. ⚠️ Uses urgency language (2 urgency words) to pressure quick action.
  4. ⚠️ Contains 1 URL(s) - be cautious of links in unsolicited messages.
  5. ⚠️ Excessive use of capital letters, a common spam/scam tactic.
  6. ⚠️ Contains 3 exclamation marks, indicating aggressive/pushy language.
```

## Project Structure

```
.
├── fake_detector.py          # Main AI detection module
├── url_feature_extractor.py  # URL feature extraction
├── message_feature_extractor.py  # Message feature extraction
├── train_models.py           # Training script
├── demo.py                   # Demo and interactive script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── models/                   # Saved ML models (created after training)
    ├── url_model.pkl
    ├── url_scaler.pkl
    ├── message_model.pkl
    └── message_scaler.pkl
```

## Model Accuracy

The models are trained using ensemble methods for high accuracy:

- **URL Model**: Typically achieves 90%+ accuracy
- **Message Model**: Typically achieves 95%+ accuracy

*Note: Actual accuracy may vary based on training data. For production use, train on larger, real-world datasets.*

## Why Links/Messages Are Flagged as Fake

The system provides detailed explanations including:

### For URLs:
- URL shorteners (bit.ly, tinyurl, etc.)
- Suspicious top-level domains (.tk, .ml, .ga)
- IP addresses instead of domain names
- Suspicious keywords (verify, click, account)
- Missing HTTPS encryption
- High entropy (random/obfuscated characters)
- Unusual URL length or structure

### For Messages:
- Suspicious phrases (click here, act now, verify account)
- Urgency language (urgent, immediate, now)
- Financial keywords (bank, payment, account)
- Authority impersonation (IRS, FBI, police)
- Excessive capitalization or punctuation
- Embedded URLs
- Word repetition patterns

## Extending the System

### Adding More Training Data

Edit `train_models.py` to add more legitimate and fake examples:

```python
legitimate_urls.append('https://your-legitimate-url.com')
fake_urls.append('http://suspicious-url.tk')
```

### Customizing Features

Modify `url_feature_extractor.py` or `message_feature_extractor.py` to add new detection features.

### Improving Accuracy

- Add more diverse training data
- Fine-tune hyperparameters in `fake_detector.py`
- Use larger datasets for training
- Implement additional feature engineering

## Limitations

- Current models are trained on synthetic data. For production use, train on real-world datasets.
- Detection accuracy depends on the quality and diversity of training data.
- New attack patterns may require model retraining.
- The system provides probabilistic predictions, not absolute guarantees.

## Security Note

This tool is designed to assist in identifying potentially fake content but should not be the sole basis for security decisions. Always use multiple verification methods and exercise caution with suspicious content.

## License

This project is provided as-is for educational and research purposes.

## Contributing

Feel free to extend this project by:
- Adding more sophisticated feature extraction
- Implementing additional ML models
- Creating a web interface
- Adding API endpoints
- Improving training data diversity

## Contact

For questions or improvements, please refer to the project documentation or create an issue.

