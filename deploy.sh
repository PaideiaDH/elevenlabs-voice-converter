#!/bin/bash

# ElevenLabs Voice Converter Deployment Script

set -e

echo "🎤 ElevenLabs Voice Converter - Deployment Script"
echo "=================================================="

# Check if API key is set
if [ -z "$ELEVENLABS_API_KEY" ]; then
    echo "❌ ELEVENLABS_API_KEY environment variable not set"
    echo "Please set your API key:"
    echo "export ELEVENLABS_API_KEY=your_api_key_here"
    exit 1
fi

echo "✅ API key is set"

# Function to deploy with Docker
deploy_docker() {
    echo "🐳 Deploying with Docker..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed"
        exit 1
    fi
    
    # Check if docker-compose is installed
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose is not installed"
        exit 1
    fi
    
    echo "✅ Docker and Docker Compose found"
    
    # Build and run
    docker-compose up --build -d
    
    echo "✅ App deployed with Docker!"
    echo "🌐 Access the app at: http://localhost:8501"
    echo "📊 View logs: docker-compose logs -f"
    echo "🛑 Stop: docker-compose down"
}

# Function to deploy locally
deploy_local() {
    echo "💻 Deploying locally..."
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 is not installed"
        exit 1
    fi
    
    # Install dependencies
    echo "📦 Installing dependencies..."
    pip3 install -r requirements.txt
    
    # Run the app
    echo "🚀 Starting Streamlit app..."
    streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
}

# Function to deploy to Streamlit Cloud
deploy_streamlit_cloud() {
    echo "☁️  Deploying to Streamlit Cloud..."
    
    # Check if git is installed
    if ! command -v git &> /dev/null; then
        echo "❌ Git is not installed"
        exit 1
    fi
    
    echo "📋 Steps to deploy to Streamlit Cloud:"
    echo "1. Push your code to GitHub:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    echo "   git remote add origin https://github.com/yourusername/elevenlabs-voice-converter.git"
    echo "   git push -u origin main"
    echo ""
    echo "2. Go to https://share.streamlit.io"
    echo "3. Connect your GitHub account"
    echo "4. Select your repository"
    echo "5. Set environment variable: ELEVENLABS_API_KEY"
    echo "6. Deploy!"
    echo ""
    echo "🌐 Your app will be available at: https://your-app-name.streamlit.app"
}

# Main deployment logic
case "${1:-docker}" in
    "docker")
        deploy_docker
        ;;
    "local")
        deploy_local
        ;;
    "cloud")
        deploy_streamlit_cloud
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [docker|local|cloud]"
        echo ""
        echo "Deployment options:"
        echo "  docker  - Deploy using Docker (default)"
        echo "  local   - Deploy locally with Python"
        echo "  cloud   - Instructions for Streamlit Cloud"
        echo "  help    - Show this help message"
        echo ""
        echo "Environment variables:"
        echo "  ELEVENLABS_API_KEY - Your ElevenLabs API key (required)"
        ;;
    *)
        echo "❌ Unknown deployment method: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
