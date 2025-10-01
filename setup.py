#!/usr/bin/env python3

import os
import sys
import subprocess
import nltk

def install_requirements():
    """Install all required packages"""
    print("📦 Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def download_nltk_data():
    """Download required NLTK data"""
    print("📚 Downloading NLTK data...")
    nltk_data = [
        'punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger',
        'maxent_ne_chunker', 'words'
    ]
    
    for data in nltk_data:
        try:
            nltk.download(data, quiet=True)
            print(f"  ✅ {data}")
        except Exception as e:
            print(f"  ❌ {data}: {e}")

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directory structure...")
    directories = [
        'models/trained',
        'data/knowledge_base',
        'data/training_sets',
        'logs',
        'src/core',
        'src/analytics',
        'src/data',
        'src/utils',
        'tests'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ {directory}")

def setup_spacy_model():
    """Download spaCy model"""
    print("🔧 Setting up spaCy model...")
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("  ✅ en_core_web_sm")
    except Exception as e:
        print(f"  ❌ spaCy model: {e}")

def main():
    """Main setup function"""
    print("🚀 Setting up Advanced Nexus Truth Verifier...")
    print("=" * 50)
    
    try:
        install_requirements()
        download_nltk_data()
        create_directories()
        setup_spacy_model()
        
        print("\n🎉 Setup completed successfully!")
        print("\nTo run the application:")
        print("  streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()