# YarnGPT SDK Examples

This directory contains example scripts demonstrating how to use the YarnGPT SDK.

## Running Examples

First, set your API key as an environment variable:

### Windows (PowerShell)
```powershell
$env:YARNGPT_API_KEY="your_api_key_here"
```

### Windows (CMD)
```cmd
set YARNGPT_API_KEY=your_api_key_here
```

### Linux/Mac
```bash
export YARNGPT_API_KEY="your_api_key_here"
```

Then run any example:

```bash
python examples/basic_usage.py
python examples/context_manager.py
python examples/error_handling.py
python examples/all_voices.py
```

## Examples Overview

- **basic_usage.py** - Demonstrates basic text-to-speech conversion with different voices and formats
- **context_manager.py** - Shows proper resource management using context managers
- **error_handling.py** - Examples of handling various error scenarios
- **all_voices.py** - Generates samples using all 16 available voices
