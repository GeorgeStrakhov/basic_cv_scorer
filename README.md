# CV Scoring System

This system automatically scores CVs/resumes using AI, evaluating them on creativity, experience, and education. The system can process both PDF and DOCX files.

## Table of Contents
- [Prerequisites Installation](#prerequisites-installation)
- [Project Setup](#project-setup)
- [Configuration](#configuration)
- [Usage](#usage)
- [Understanding Results](#understanding-results)
- [Troubleshooting](#troubleshooting)

## Prerequisites Installation

### 1. Install Git
1. Visit [Git Downloads](https://git-scm.com/downloads)
2. Download and install Git for your operating system:
   - **Windows**: Click the Windows download and follow the installer
   - **Mac**: Use the macOS installer or run `brew install git` if you have Homebrew
   - **Linux**: Run `sudo apt-get install git` (Ubuntu/Debian) or `sudo yum install git` (Fedora)

### 2. Install Python
1. Visit [Python Downloads](https://python.org/downloads)
2. Download and install Python 3.10 or newer
3. During installation on Windows, make sure to check "Add Python to PATH"
4. Verify installation by opening a terminal/command prompt and typing:
   ```bash
   python --version
   ```
   You should see something like `Python 3.10.x`

### 3. Install uv (Python Package Manager)
1. Open a terminal/command prompt
2. Install uv by running:
   ```bash
   # Windows (PowerShell, run as Administrator)
   curl.exe -L https://github.com/astral-sh/uv/releases/latest/download/uv-windows-x64.zip -o uv.zip
   Expand-Archive uv.zip
   Move-Item uv/uv.exe C:\Windows\System32\

   # Mac/Linux
   curl -LsSf https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh | sh
   ```

## Project Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd cv-scoring-system
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   
   uv pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the project root directory:
   ```bash
   # Windows
   copy .env.example .env
   # Mac/Linux
   cp .env.example .env
   ```

2. Open the `.env` file in a text editor and add your API credentials:
   ```
   OPENAI_CUSTOM_API_KEY=your_api_key_here
   OPENAI_CUSTOM_API_BASE=your_api_base_url_here
   ```

## Usage

### Preparing CVs for Scoring

1. Create a `submissions` folder in the project directory if it doesn't exist:
   ```bash
   mkdir submissions
   ```

2. Copy your CV files (PDF or DOCX format) into the `submissions` folder
   - Supported formats: `.pdf`, `.docx`
   - Make sure file names don't contain special characters
   - Example files:
     ```
     submissions/
     ├── john_doe_cv.pdf
     ├── jane_smith_resume.docx
     └── candidate_resume.pdf
     ```

### Running the Scorer

1. Make sure your virtual environment is activated:
   ```bash
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```

2. Run the scoring script:
   ```bash
   python cv_scorer.py
   ```

3. The script will:
   - Process all new CVs in the submissions folder
   - Show a progress bar during processing
   - Save results automatically after each CV

## Understanding Results

Results are saved in `output/cv_scores.csv` and include:
- Filename of the CV
- Scores for different categories (creativity, experience, education)
- Additional feedback and recommendations

You can open the CSV file using:
- Microsoft Excel
- Google Sheets
- Any spreadsheet software

## Troubleshooting

### Common Issues and Solutions

1. **"Python not found" error**
   - Make sure Python is installed and added to PATH
   - Try restarting your terminal/computer

2. **"Permission denied" errors**
   - Run terminal/command prompt as administrator
   - Check file permissions in submissions folder

3. **Installation errors**
   - Make sure you have internet connection
   - Try running the commands with administrator privileges
   - Check if antivirus is blocking installations

4. **API errors**
   - Verify your API credentials in `.env` file
   - Check your internet connection
   - Ensure you have sufficient API credits

### Getting Help

If you encounter any issues:
1. Check the error message carefully
2. Look for specific error codes
3. Contact technical support with:
   - Error message
   - Operating system details
   - Steps to reproduce the issue

## Additional Notes

- The system processes CVs in batches and remembers which files it has already processed
- New CVs can be added to the submissions folder at any time
- Results are automatically appended to the existing CSV file
- Make regular backups of your output folder

For technical users: The system uses OpenAI's GPT-4 model for analysis and can be customized by modifying the scoring criteria in `scoring_config.py`.
