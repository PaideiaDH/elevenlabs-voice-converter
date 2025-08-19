#!/usr/bin/env python3
"""
ElevenLabs Voice Converter - Streamlit Web App
A user-friendly web interface for converting voice files
"""

import streamlit as st
import os
import tempfile
import zipfile
from pathlib import Path
import time
from voice_converter import VoiceConverter
import io

# Page configuration
st.set_page_config(
    page_title="ElevenLabs Voice Converter",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .voice-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        correct_password = os.environ.get("STREAMLIT_SERVER_PASSWORD", "paideia2024")
        if st.session_state["password"] == correct_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for username + password
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct
        return True

@st.cache_resource
def get_voice_converter():
    """Get cached voice converter instance"""
    try:
        return VoiceConverter()
    except Exception as e:
        st.error(f"Failed to initialize voice converter: {e}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_voices():
    """Get cached list of voices"""
    converter = get_voice_converter()
    if converter:
        try:
            return converter.get_voices()
        except Exception as e:
            st.error(f"Failed to fetch voices: {e}")
            return []
    return []

def create_zip_download(files_dict, zip_name="converted_voices.zip"):
    """Create a zip file for download"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path, file_data in files_dict.items():
            zip_file.writestr(file_path, file_data)
    
    zip_buffer.seek(0)
    return zip_buffer

def main():
    """Main Streamlit app"""
    
    # Password protection
    if not check_password():
        st.stop()
    
    # Header
    st.markdown('<h1 class="main-header">🎤 ElevenLabs Voice Converter</h1>', unsafe_allow_html=True)
    st.markdown("### Transform your voice files to different voices using AI")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Background noise removal
        remove_noise = st.checkbox(
            "Remove background noise",
            value=True,
            help="Clean up background sounds for better voice conversion"
        )
        
        # Output format
        output_format = st.selectbox(
            "Output format",
            ["mp3_44100_128", "mp3_44100_192", "mp3_22050_32"],
            help="Higher quality = larger files"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Usage")
        st.markdown("1. Upload your voice files")
        st.markdown("2. Select target voices")
        st.markdown("3. Click Convert")
        st.markdown("4. Download results")
        
        # Logout button
        if st.button("🚪 Logout"):
            del st.session_state["password_correct"]
            st.rerun()
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Upload Files")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose voice files to convert",
            type=['mp3', 'wav', 'm4a', 'flac', 'aac', 'ogg'],
            accept_multiple_files=True,
            help="Supported formats: MP3, WAV, M4A, FLAC, AAC, OGG"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} files uploaded")
            
            # Show uploaded files
            st.subheader("Uploaded Files:")
            for file in uploaded_files:
                st.write(f"📄 {file.name} ({file.size / 1024:.1f} KB)")
    
    with col2:
        st.header("🎭 Select Voices")
        
        # Get voices
        voices = get_voices()
        
        if not voices:
            st.warning("⚠️ No voices available. Please check your API key.")
            return
        
        # Voice selection
        selected_voices = st.multiselect(
            "Choose target voices",
            options=voices,
            format_func=lambda x: f"{x['name']} ({x.get('category', 'Unknown')})",
            help="Select one or more voices to convert your files to"
        )
        
        if selected_voices:
            st.success(f"✅ {len(selected_voices)} voices selected")
            
            # Show selected voices
            st.subheader("Selected Voices:")
            for voice in selected_voices:
                with st.container():
                    st.markdown(f"""
                    <div class="voice-card">
                        <strong>{voice['name']}</strong><br>
                        <small>ID: {voice['voice_id']}</small><br>
                        <small>Category: {voice.get('category', 'Unknown')}</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Conversion section
    if uploaded_files and selected_voices:
        st.markdown("---")
        st.header("🔄 Convert Files")
        
        if st.button("🚀 Start Conversion", type="primary", use_container_width=True):
            # Initialize converter
            converter = get_voice_converter()
            if not converter:
                st.error("❌ Voice converter not available. Please check your API key.")
                return
            
            # Create progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Prepare for conversion
            total_conversions = len(uploaded_files) * len(selected_voices)
            current_conversion = 0
            converted_files = {}
            
            # Create temporary directory for processing
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Process each file
                for file in uploaded_files:
                    # Save uploaded file to temp directory
                    input_path = temp_path / file.name
                    with open(input_path, "wb") as f:
                        f.write(file.getbuffer())
                    
                    # Convert to each selected voice
                    for voice in selected_voices:
                        current_conversion += 1
                        progress = current_conversion / total_conversions
                        
                        # Update progress
                        status_text.text(f"Converting {file.name} to {voice['name']}... ({current_conversion}/{total_conversions})")
                        progress_bar.progress(progress)
                        
                        try:
                            # Generate output filename
                            output_filename = f"{Path(file.name).stem}_{voice['name']}.mp3"
                            output_path = temp_path / output_filename
                            
                            # Convert the file
                            success = converter.convert_voice(
                                input_file=str(input_path),
                                voice_id=voice['voice_id'],
                                output_file=str(output_path),
                                remove_background_noise=remove_noise,
                                output_format=output_format
                            )
                            
                            if success and output_path.exists():
                                # Read the converted file
                                with open(output_path, "rb") as f:
                                    file_data = f.read()
                                
                                # Store for download
                                converted_files[output_filename] = file_data
                            
                        except Exception as e:
                            st.error(f"Error converting {file.name} to {voice['name']}: {e}")
                
                # Final progress update
                progress_bar.progress(1.0)
                status_text.text("✅ Conversion complete!")
                
                # Show results
                if converted_files:
                    st.success(f"🎉 Successfully converted {len(converted_files)} files!")
                    
                    # Create download section
                    st.markdown("---")
                    st.header("📥 Download Results")
                    
                    # Show converted files
                    st.subheader("Converted Files:")
                    for filename in converted_files.keys():
                        st.write(f"✅ {filename}")
                    
                    # Create zip file for download
                    zip_buffer = create_zip_download(converted_files)
                    
                    # Download button
                    st.download_button(
                        label="📦 Download All Files (ZIP)",
                        data=zip_buffer.getvalue(),
                        file_name="converted_voices.zip",
                        mime="application/zip",
                        use_container_width=True
                    )
                    
                    # Individual file downloads
                    st.subheader("Download Individual Files:")
                    for filename, file_data in converted_files.items():
                        st.download_button(
                            label=f"📄 {filename}",
                            data=file_data,
                            file_name=filename,
                            mime="audio/mpeg"
                        )
                else:
                    st.error("❌ No files were successfully converted.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        Powered by ElevenLabs Speech-to-Speech API | 
        <a href='https://elevenlabs.io' target='_blank'>Get your API key</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
