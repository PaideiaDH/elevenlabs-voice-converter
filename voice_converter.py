#!/usr/bin/env python3
"""
Voice Converter App
Converts voiceover files to different voices using ElevenLabs Speech-to-Speech API
"""

import os
import json
import requests
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv
from tqdm import tqdm
import time

# Load environment variables
load_dotenv()

class VoiceConverter:
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the VoiceConverter with API key
        
        Args:
            api_key: ElevenLabs API key. If not provided, will try to get from environment
        """
        self.api_key = api_key or os.getenv('ELEVENLABS_API_KEY')
        if not self.api_key:
            raise ValueError("API key is required. Set ELEVENLABS_API_KEY environment variable or pass it to constructor.")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "xi-api-key": self.api_key
        }
        
        # Cache for voices
        self._voices_cache = None
    
    def get_voices(self) -> List[Dict]:
        """
        Get available voices from ElevenLabs API
        
        Returns:
            List of voice dictionaries
        """
        if self._voices_cache is None:
            response = requests.get(f"{self.base_url}/voices", headers=self.headers)
            response.raise_for_status()
            self._voices_cache = response.json()["voices"]
        
        return self._voices_cache
    
    def list_voices(self) -> None:
        """
        Print available voices in a formatted way
        """
        voices = self.get_voices()
        print(f"\nAvailable voices ({len(voices)} total):")
        print("-" * 80)
        
        for i, voice in enumerate(voices, 1):
            print(f"{i:2d}. {voice['name']} (ID: {voice['voice_id']})")
            if voice.get('description'):
                print(f"     Description: {voice['description']}")
            print()
    
    def convert_voice(self, 
                     input_file: str, 
                     voice_id: str, 
                     output_file: str,
                     model_id: str = "eleven_multilingual_sts_v2",
                     output_format: str = "mp3_44100_128",
                     remove_background_noise: bool = False) -> bool:
        """
        Convert a single audio file to a different voice
        
        Args:
            input_file: Path to input audio file
            voice_id: ElevenLabs voice ID to convert to
            output_file: Path for output audio file
            model_id: Model to use for conversion
            output_format: Output audio format
            remove_background_noise: Whether to remove background noise
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare the request
            url = f"{self.base_url}/speech-to-speech/{voice_id}"
            
            params = {
                "model_id": model_id,
                "output_format": output_format,
                "remove_background_noise": str(remove_background_noise).lower()
            }
            
            # Prepare the file upload
            with open(input_file, 'rb') as audio_file:
                files = {
                    'audio': (os.path.basename(input_file), audio_file, 'audio/mpeg')
                }
                
                response = requests.post(url, headers=self.headers, params=params, files=files)
                response.raise_for_status()
            
            # Save the converted audio
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error converting {input_file}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error converting {input_file}: {e}")
            return False
    
    def batch_convert(self, 
                     input_folder: str, 
                     output_folder: str, 
                     voice_ids: List[str],
                     supported_formats: List[str] = None) -> Dict[str, List[str]]:
        """
        Convert all audio files in a folder to multiple voices
        
        Args:
            input_folder: Folder containing input audio files
            output_folder: Folder to save converted audio files
            voice_ids: List of voice IDs to convert to
            supported_formats: List of supported audio file extensions
            
        Returns:
            Dictionary with results: {'success': [...], 'failed': [...]}
        """
        if supported_formats is None:
            supported_formats = ['.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg']
        
        input_path = Path(input_folder)
        output_path = Path(output_folder)
        
        # Create output folder if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Get all audio files
        audio_files = []
        for ext in supported_formats:
            audio_files.extend(input_path.glob(f"*{ext}"))
            audio_files.extend(input_path.glob(f"*{ext.upper()}"))
        
        if not audio_files:
            print(f"No audio files found in {input_folder}")
            return {'success': [], 'failed': []}
        
        print(f"Found {len(audio_files)} audio files to convert")
        print(f"Converting to {len(voice_ids)} voices...")
        
        # Get voice names for better output
        voices = self.get_voices()
        voice_names = {v['voice_id']: v['name'] for v in voices}
        
        success_files = []
        failed_files = []
        
        # Process each file
        for audio_file in tqdm(audio_files, desc="Converting files"):
            file_success = True
            
            for voice_id in voice_ids:
                voice_name = voice_names.get(voice_id, voice_id)
                
                # Create output filename
                output_filename = f"{audio_file.stem}_{voice_name}_{voice_id}{audio_file.suffix}"
                output_file = output_path / output_filename
                
                # Convert the file
                if not self.convert_voice(
                    str(audio_file), 
                    voice_id, 
                    str(output_file)
                ):
                    file_success = False
                    failed_files.append(f"{audio_file.name} -> {voice_name}")
                
                # Small delay to avoid rate limiting
                time.sleep(0.1)
            
            if file_success:
                success_files.append(audio_file.name)
        
        return {'success': success_files, 'failed': failed_files}


def main():
    """Main function to run the voice converter"""
    print("🎤 ElevenLabs Voice Converter")
    print("=" * 40)
    
    # Initialize converter
    try:
        converter = VoiceConverter()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set your ELEVENLABS_API_KEY environment variable or create a .env file")
        return
    
    # Show available voices
    converter.list_voices()
    
    # Get user input
    input_folder = input("\nEnter the path to your input folder: ").strip()
    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist")
        return
    
    output_folder = input("Enter the path for output folder: ").strip()
    
    # Get voice IDs
    print("\nEnter voice IDs to convert to (comma-separated):")
    voice_ids_input = input("Voice IDs: ").strip()
    voice_ids = [vid.strip() for vid in voice_ids_input.split(',') if vid.strip()]
    
    if not voice_ids:
        print("Error: No voice IDs provided")
        return
    
    # Validate voice IDs
    available_voices = {v['voice_id'] for v in converter.get_voices()}
    invalid_voices = [vid for vid in voice_ids if vid not in available_voices]
    if invalid_voices:
        print(f"Warning: Invalid voice IDs: {invalid_voices}")
        voice_ids = [vid for vid in voice_ids if vid in available_voices]
        if not voice_ids:
            print("Error: No valid voice IDs provided")
            return
    
    # Start conversion
    print(f"\nStarting conversion...")
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    print(f"Target voices: {voice_ids}")
    
    results = converter.batch_convert(input_folder, output_folder, voice_ids)
    
    # Show results
    print(f"\nConversion complete!")
    print(f"Successfully converted: {len(results['success'])} files")
    print(f"Failed conversions: {len(results['failed'])}")
    
    if results['failed']:
        print("\nFailed conversions:")
        for failed in results['failed']:
            print(f"  - {failed}")


if __name__ == "__main__":
    main()
