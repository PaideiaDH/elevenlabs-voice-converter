# ElevenLabs Voice Converter

A Python application that converts voiceover files to different voices using ElevenLabs' Speech-to-Speech API. This tool allows you to batch process audio files in a folder and convert them to multiple target voices while maintaining the original emotion, timing, and delivery.

## Features

- 🎤 **Batch Processing**: Convert multiple audio files at once
- 🎭 **Multiple Voices**: Convert each file to multiple target voices
- 🎵 **Multiple Formats**: Supports MP3, WAV, M4A, FLAC, AAC, OGG
- 📊 **Progress Tracking**: Real-time progress bar and detailed results
- 🔧 **Configurable**: Customizable output formats and models
- 🎯 **Voice Validation**: Automatically validates voice IDs against available voices

## Prerequisites

- Python 3.7 or higher
- ElevenLabs API key (get one from [ElevenLabs](https://elevenlabs.io/speech-to-speech))

## Installation

1. **Clone or download this repository**

2. **Set up a virtual environment (recommended)**:
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   
   # Install dependencies
   pip install -r requirements.txt
   ```

   **Quick activation script** (macOS/Linux):
   ```bash
   ./activate_venv.sh
   ```

3. **Set up your API key**:
   - Create a `.env` file in the project directory
   - Add your ElevenLabs API key:
     ```
     ELEVENLABS_API_KEY=your_actual_api_key_here
     ```
   - Or set it as an environment variable:
     ```bash
     export ELEVENLABS_API_KEY=your_actual_api_key_here
     ```

## Usage

### Interactive Mode

Run the application and follow the prompts:

```bash
python voice_converter.py
```

The app will:
1. Show all available voices from your ElevenLabs account
2. Ask for your input folder path
3. Ask for your output folder path
4. Ask for voice IDs to convert to (comma-separated)
5. Process all audio files and show results

### Programmatic Usage

You can also use the `VoiceConverter` class in your own scripts:

```python
from voice_converter import VoiceConverter

# Initialize with API key
converter = VoiceConverter(api_key="your_api_key")

# List available voices
converter.list_voices()

# Convert a single file
success = converter.convert_voice(
    input_file="path/to/input.mp3",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    output_file="path/to/output.mp3"
)

# Batch convert multiple files
results = converter.batch_convert(
    input_folder="path/to/input/folder",
    output_folder="path/to/output/folder",
    voice_ids=["voice_id_1", "voice_id_2", "voice_id_3"]
)
```

## API Reference

Based on the [ElevenLabs Speech-to-Speech API documentation](https://elevenlabs.io/docs/api-reference/speech-to-speech/convert), this app uses the following endpoint:

- **Endpoint**: `POST /v1/speech-to-speech/:voice_id`
- **Purpose**: Transform audio from one voice to another while maintaining emotion, timing, and delivery

### Supported Parameters

- `model_id`: Model to use (default: "eleven_multilingual_sts_v2")
- `output_format`: Output audio format (default: "mp3_44100_128")
- `remove_background_noise`: Remove background noise (default: false)
- `voice_settings`: Override voice settings (optional)
- `seed`: Deterministic sampling seed (optional)

### Supported Audio Formats

**Input Formats**: MP3, WAV, M4A, FLAC, AAC, OGG
**Output Formats**: Various MP3 configurations (see ElevenLabs API docs for full list)

## File Naming Convention

Converted files are named using the pattern:
```
{original_filename}_{voice_name}_{voice_id}.{extension}
```

Example: `my_voiceover_Rachel_JBFqnCBsd6RMkjVDRZzb.mp3`

## Error Handling

The application includes comprehensive error handling:
- Invalid API keys
- Network connectivity issues
- Invalid voice IDs
- File access problems
- Rate limiting (with automatic delays)

## Rate Limiting

The app includes a small delay (0.1 seconds) between API calls to avoid rate limiting. For high-volume usage, consider implementing additional rate limiting strategies.

## Troubleshooting

### Common Issues

1. **"API key is required" error**:
   - Make sure you've set the `ELEVENLABS_API_KEY` environment variable
   - Or create a `.env` file with your API key

2. **"No audio files found"**:
   - Check that your input folder contains supported audio files
   - Supported formats: .mp3, .wav, .m4a, .flac, .aac, .ogg

3. **"Invalid voice IDs"**:
   - Use the `list_voices()` method to see available voice IDs
   - Make sure you're using the correct voice ID format

4. **Network errors**:
   - Check your internet connection
   - Verify your ElevenLabs API key is valid
   - Check ElevenLabs service status

### Getting Help

- Check the [ElevenLabs API documentation](https://elevenlabs.io/docs/api-reference/speech-to-speech/convert)
- Verify your API key at [ElevenLabs dashboard](https://elevenlabs.io/speech-to-speech)
- Check your account's usage limits and subscription tier

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
