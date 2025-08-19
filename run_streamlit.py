#!/usr/bin/env python3
"""
Run the ElevenLabs Voice Converter Streamlit app
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit app"""
    print("🎤 Starting ElevenLabs Voice Converter Web App...")
    print("=" * 50)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit is installed")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit==1.28.0"])
    
    # Set Streamlit configuration
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    print("🌐 Starting web server...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Run Streamlit
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ])

if __name__ == "__main__":
    main()
