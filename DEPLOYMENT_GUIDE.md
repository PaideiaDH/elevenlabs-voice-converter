# 🚀 ElevenLabs Voice Converter - Deployment Guide

This guide shows you how to deploy the voice converter as a web app that your employees can use without installing Python.

## 🎯 Overview

The Streamlit web app provides a user-friendly interface where employees can:
- Upload voice files through their browser
- Select target voices from a dropdown
- Convert files with one click
- Download results as individual files or a ZIP

## 📋 Prerequisites

- Python 3.7 or higher
- ElevenLabs API key
- Internet connection

## 🛠️ Local Deployment (Development)

### Option 1: Quick Start
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export ELEVENLABS_API_KEY=your_api_key_here

# 3. Run the app
streamlit run streamlit_app.py
```

### Option 2: Using the run script
```bash
python3 run_streamlit.py
```

The app will open at: http://localhost:8501

## 🌐 Production Deployment

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/elevenlabs-voice-converter.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set environment variable: `ELEVENLABS_API_KEY`
   - Deploy!

### Option 2: Heroku

1. **Create `Procfile`:**
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create `setup.sh`:**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS=false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy:**
   ```bash
   heroku create your-app-name
   heroku config:set ELEVENLABS_API_KEY=your_api_key
   git push heroku main
   ```

### Option 3: Docker (Most Portable)

1. **Create `Dockerfile`:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Create `docker-compose.yml`:**
   ```yaml
   version: '3.8'
   services:
     voice-converter:
       build: .
       ports:
         - "8501:8501"
       environment:
         - ELEVENLABS_API_KEY=${ELEVENLABS_API_KEY}
       volumes:
         - ./voice_files:/app/voice_files
   ```

3. **Run with Docker:**
   ```bash
   # Set your API key
   export ELEVENLABS_API_KEY=your_api_key_here
   
   # Build and run
   docker-compose up --build
   ```

### Option 4: VPS/Cloud Server

1. **Install dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```

2. **Set up the app:**
   ```bash
   git clone https://github.com/yourusername/elevenlabs-voice-converter.git
   cd elevenlabs-voice-converter
   pip3 install -r requirements.txt
   ```

3. **Create systemd service:**
   ```bash
   sudo nano /etc/systemd/system/voice-converter.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=ElevenLabs Voice Converter
   After=network.target
   
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/elevenlabs-voice-converter
   Environment=ELEVENLABS_API_KEY=your_api_key_here
   ExecStart=/usr/bin/python3 -m streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

4. **Start the service:**
   ```bash
   sudo systemctl enable voice-converter
   sudo systemctl start voice-converter
   ```

## 🔧 Configuration

### Environment Variables
- `ELEVENLABS_API_KEY`: Your ElevenLabs API key (required)

### Streamlit Configuration
Create `~/.streamlit/config.toml`:
```toml
[server]
headless = true
port = 8501
enableCORS = false
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

## 📱 Usage for Employees

Once deployed, employees simply:

1. **Open the web app** in their browser
2. **Enter the API key** (or it's pre-configured)
3. **Upload voice files** (drag & drop or click to browse)
4. **Select target voices** from the dropdown
5. **Click "Start Conversion"**
6. **Download results** as individual files or ZIP

## 🔒 Security Considerations

- **API Key Management**: Store API keys securely, not in code
- **File Upload Limits**: Configure max upload size in Streamlit
- **HTTPS**: Use HTTPS in production
- **Rate Limiting**: Consider adding rate limiting for API calls
- **Authentication**: Add user authentication if needed

## 📊 Monitoring

### Health Check
```bash
curl http://your-app-url/health
```

### Logs
```bash
# If using systemd
sudo journalctl -u voice-converter -f

# If using Docker
docker-compose logs -f
```

## 🚨 Troubleshooting

### Common Issues

1. **"No voices available"**
   - Check API key is correct
   - Verify internet connection
   - Check ElevenLabs service status

2. **"Upload failed"**
   - Check file size limits
   - Verify file format is supported
   - Check disk space

3. **"Conversion failed"**
   - Check API quota/limits
   - Verify file format
   - Check server logs

### Performance Tips

- Use background noise removal sparingly (increases processing time)
- Limit concurrent conversions
- Monitor API usage and costs
- Consider caching voice lists

## 💰 Cost Management

- Monitor ElevenLabs API usage
- Set up billing alerts
- Consider usage quotas per user
- Optimize file sizes before upload

---

**Need help?** Check the main README.md for more detailed documentation.
