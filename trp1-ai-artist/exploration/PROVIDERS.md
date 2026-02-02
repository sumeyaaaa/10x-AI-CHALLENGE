# Provider Capabilities

## Overview

The framework supports multiple providers for music, video, and image generation. Each provider has unique capabilities, strengths, and limitations.

## Music Providers

### 1. Lyria (Google)

**Provider Name:** `lyria`  
**Implementation:** `GoogleLyriaProvider`  
**API:** Google Gemini API (Lyria RealTime)

**Capabilities:**
- ✅ Real-time streaming generation
- ✅ Fast generation (~30 seconds)
- ✅ BPM and temperature control
- ✅ Weighted prompt support
- ❌ **No vocals** (instrumental only)
- ❌ No reference audio support

**Best For:**
- Quick instrumental music generation
- Background music for videos
- Real-time music creation

**Example:**
```bash
uv run ai-content music --style jazz --provider lyria --duration 30
```

**Technical Details:**
- Uses WebSocket streaming for real-time generation
- Experimental API (may change)
- Requires `GEMINI_API_KEY`

---

### 2. MiniMax (via AIMLAPI)

**Provider Name:** `minimax`  
**Implementation:** `MiniMaxMusicProvider`  
**API:** AIMLAPI.com (MiniMax Music 2.0)

**Capabilities:**
- ✅ **Vocals support** (with lyrics)
- ✅ Reference audio for style transfer
- ✅ High-quality output
- ✅ Non-English vocal support
- ❌ **Not real-time** (5-15 minutes generation time)
- ❌ Requires polling for status

**Best For:**
- Songs with vocals
- Style transfer from reference audio
- Professional-quality music

**Example:**
```bash
uv run ai-content music --prompt "Lo-fi hip-hop" --provider minimax --lyrics lyrics.txt
```

**Technical Details:**
- Uses HTTP API with async polling
- Job-based generation (returns immediately with job ID)
- Requires `AIMLAPI_KEY`
- Use `ai-content music-status <job_id>` to check progress

---

## Video Providers

### 1. Veo (Google)

**Provider Name:** `veo`  
**Implementation:** `GoogleVeoProvider`  
**API:** Google Gemini API (Veo 3.1)

**Capabilities:**
- ✅ Text-to-video generation
- ✅ **Image-to-video** (animate first frame)
- ✅ Fast generation (~30 seconds typical)
- ✅ Multiple aspect ratios (16:9, 9:16, 1:1, 21:9)
- ✅ Max duration: 8 seconds

**Best For:**
- Quick video iterations
- Image-to-video animations
- Fast prototyping

**Example:**
```bash
uv run ai-content video --style nature --provider veo --duration 5
```

**Technical Details:**
- Uses async polling for completion
- Supports first frame URL for image-to-video
- Requires `GEMINI_API_KEY`

---

### 2. KlingAI

**Provider Name:** `kling`  
**Implementation:** `KlingDirectProvider`  
**API:** KlingAI Direct API

**Capabilities:**
- ✅ **Highest quality** video generation
- ✅ **Image-to-video** support
- ✅ v2.1-master model
- ✅ Max duration: 10 seconds
- ❌ **Slow generation** (5-14 minutes)
- ❌ Requires JWT authentication

**Best For:**
- Final production videos
- High-quality renders
- When quality > speed

**Example:**
```bash
uv run ai-content video --prompt "Dragon soaring" --provider kling --aspect 16:9
```

**Technical Details:**
- Uses JWT token authentication
- Requires `KLINGAI_API_KEY` and `KLINGAI_SECRET_KEY`
- Long polling for completion

---

## Image Providers

### Imagen (Google)

**Provider Name:** `imagen`  
**Implementation:** `GoogleImagenProvider`  
**API:** Google Gemini API (Imagen)

**Capabilities:**
- ✅ High-quality photorealistic images
- ✅ Multiple aspect ratios
- ✅ Batch generation support

**Best For:**
- Keyframe generation for video pipelines
- Standalone image creation

**Example:**
```python
from ai_content import ProviderRegistry

provider = ProviderRegistry.get_image("imagen")
result = await provider.generate("sunset over ocean, 8K")
```

---

## Provider Comparison

### Music Providers

| Feature | Lyria | MiniMax |
|---------|-------|---------|
| **Speed** | Fast (~30s) | Slow (5-15 min) |
| **Vocals** | ❌ No | ✅ Yes |
| **Real-time** | ✅ Yes | ❌ No |
| **Reference Audio** | ❌ No | ✅ Yes |
| **Quality** | Good | Excellent |
| **Best Use Case** | Quick instrumentals | Songs with vocals |

### Video Providers

| Feature | Veo | Kling |
|---------|-----|-------|
| **Speed** | Fast (~30s) | Slow (5-14 min) |
| **Quality** | Good | **Highest** |
| **Image-to-Video** | ✅ Yes | ✅ Yes |
| **Max Duration** | 8 seconds | 10 seconds |
| **Best Use Case** | Quick iterations | Final production |

## Provider Selection Guide

### For Music:

**Choose Lyria if:**
- You need instrumental music quickly
- Real-time generation is important
- You're creating background music

**Choose MiniMax if:**
- You need vocals/lyrics
- You want style transfer from reference audio
- Quality > speed
- You can wait 5-15 minutes

### For Video:

**Choose Veo if:**
- You need quick iterations
- You're prototyping
- Speed is important

**Choose Kling if:**
- You need the highest quality
- This is for final production
- You can wait 5-14 minutes

## Adding a New Provider

To add a new provider:

1. **Create provider class** in `providers/<name>/`:
```python
@ProviderRegistry.register_music("my_provider")
class MyMusicProvider:
    name = "my_provider"
    supports_vocals = True
    supports_realtime = False
    
    async def generate(self, prompt: str, **kwargs) -> GenerationResult:
        # Implementation
        pass
```

2. **Import in `providers/__init__.py`** to trigger registration

3. **Add settings** in `config/settings.py` if needed

4. **Update CLI** if provider needs special options

The registry pattern makes this extensible without modifying core code!

