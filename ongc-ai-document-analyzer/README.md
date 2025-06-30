# ONGC Monthly Gas Production Dashboard

![ONGC Logo](ongc_logo.png)

### Offline Desktop Application

## Overview
This is a standalone offline desktop application for analyzing ONGC gas production documents. The application features AI-powered summarization, smart search functionality, and comprehensive document analysis capabilities.

## Features
- **Offline Operation**: Works completely offline without internet connection
- **AI Summarization**: Uses BART-Large-CNN model for intelligent document summarization
- **Smart Search**: Advanced search with contextual results
- **Professional Tables**: Clean, formatted display of tabular data
- **Perforation Analysis**: Specialized analysis for perforation and testing data
- **Dark/Light Theme**: Toggle between themes for better visibility
- **Document Management**: Open documents externally or browse folders

## Installation & Setup

**Easy Setup for Anyone (No Technical Knowledge Required)**

**Option 1: Automated Setup (Recommended)**
1. Download the entire project from GitHub
2. Double-click `setup.bat` - This creates everything you need automatically!
3. Wait for installation to complete (2-3 minutes)
4. Double-click `run_app.bat` to start the application

**Why no .venv folder included?**
- The virtual environment (.venv) contains 25,000+ files (300+ MB)
- It's platform-specific (Windows/Mac/Linux differences)
- GitHub has file size limits
- The `setup.bat` creates it automatically in 2 minutes!

### Quick Start
1. Double-click `run_app.bat` to automatically install dependencies and start the app
2. The application will create a `data_folder` if it doesn't exist
3. Add your Word documents to the appropriate field folders
4. Click "Refresh Data" to load new documents

### Manual Installation
1. Ensure Python 3.7+ is installed
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python t.py`

### First-Time Setup
1. The app will automatically create a `data_folder` directory
2. Organize your Word documents in the following structure:
   ```
   data_folder/
   ├── Field_Name_1/
   │   ├── Well_1.docx
   │   ├── Well_2.docx
   │   └── ...
   ├── Field_Name_2/
   │   ├── Well_A.docx
   │   ├── Well_B.docx
   │   └── ...
   ```
3. Click "Refresh Data" to scan for documents

## Usage

### Loading Documents
1. Select a **Field** from the dropdown
2. Select a **Well Name** from the dropdown
3. Choose a **Specific Term** (default: Perforation)
4. Click **Show Info** to analyze the document

### Search Functionality
1. Load a document first
2. Enter search terms in the "Smart Search" box
3. Click "Search & Summarize" for AI-powered results
4. Use "Clear" to reset search results

### Additional Features
- **Refresh Data**: Scan for new documents in data_folder
- **Clear/Reset**: Clear all displayed content
- **Open in Word**: Open the current document in Microsoft Word
- **Open Folder**: Open the document's folder in Windows Explorer
- **App Info**: View application information
- **Dark Mode**: Toggle between light and dark themes

## AI Features

### Document Summarization
- Automatically extracts key information from documents
- Generates comprehensive bullet-point summaries
- Categorizes findings by technical areas
- Provides statistical analysis of document content

### Smart Search
- Context-aware search results
- Automatic highlighting of relevant terms
- Intelligent excerpt generation
- Multi-paragraph analysis

## Technical Requirements

### System Requirements
- Windows 10/11 (recommended)
- Python 3.7 or higher
- 4GB RAM minimum (8GB recommended for AI features)
- 2GB free disk space

### Dependencies
- `python-docx`: Word document processing
- `Pillow`: Image handling
- `transformers`: AI model support
- `torch`: Machine learning backend
- `tokenizers`: Text processing

## Data Security
- **Fully Offline**: No data sent to external servers
- **Local Processing**: All analysis performed on your machine
- **Private Documents**: Your documents remain on your local system

## Model Download Location
- The BART-Large-CNN AI model is automatically downloaded and stored in the local `model_cache` folder inside this project directory.
- This ensures all model files remain with the application for easy deployment and offline use.
- If you delete the `model_cache` folder, the model will be re-downloaded the next time you use the AI features.

## Troubleshooting

### Common Issues

**"Missing Dependencies" Error**
- Run `pip install -r requirements.txt`
- Ensure Python is properly installed

**"Data Folder Not Found" Warning**
- The app will create the folder automatically
- Add your documents and click "Refresh Data"

**AI Model Loading Issues**
- Ensure stable internet connection for first-time model download
- Once downloaded, the model works offline
- Requires approximately 1.5GB for model files

**Document Not Loading**
- Ensure files are .docx format (not .doc)
- Check file permissions
- Verify document is not corrupted

### Performance Tips
- Close other applications to free up memory for AI processing
- Use SSD storage for faster document loading
- Keep document folders organized for quick scanning

## Support
For technical issues or questions, check the application logs in the console window for detailed error messages.

## Version Information
- **Version**: 1.0
- **AI Model**: BART-Large-CNN
- **Last Updated**: December 2024
- **Platform**: Windows Desktop

---
**Note**: This application is designed for offline use with ONGC production documents. All processing is performed locally on your machine for maximum security and privacy.
