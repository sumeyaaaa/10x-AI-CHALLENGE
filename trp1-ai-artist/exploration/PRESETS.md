# Preset Catalog

## Overview

Presets are pre-configured style templates that provide optimized prompts, BPM settings (for music), and aspect ratios (for video). They make it easy to generate content with consistent, high-quality results.

## Music Presets

All music presets include:
- **Prompt**: Detailed style description
- **BPM**: Recommended tempo
- **Mood**: Emotional tone keyword
- **Tags**: Style classification tags

### Available Music Presets

| Preset Name | BPM | Mood | Tags | Description |
|------------|-----|------|------|-------------|
| `jazz` | 95 | nostalgic | smooth, fusion, sophisticated | Smooth jazz fusion with walking bass, brushed drums, mellow saxophone |
| `blues` | 72 | soulful | delta, raw, authentic | Delta blues with bluesy guitar arpeggio, vintage amplifier warmth |
| `ethiopian-jazz` | 85 | mystical | ethio-jazz, modal, african | Ethiopian jazz fusion with Masenqo-inspired strings, Mulatu Astatke inspired |
| `cinematic` | 100 | epic | orchestral, film-score, triumphant | Epic orchestral with sweeping strings, powerful brass, Hans Zimmer inspired |
| `electronic` | 128 | euphoric | house, edm, festival | Progressive house with driving bass, synth arpeggios, festival anthem energy |
| `ambient` | 60 | peaceful | ambient, meditative, eno | Ambient soundscape with ethereal pads, Brian Eno inspired |
| `lofi` | 85 | relaxed | lofi, chill, study | Lo-fi hip-hop with vinyl crackle, dusty drum loops, study beats |
| `rnb` | 90 | sultry | rnb, neo-soul, modern | Contemporary R&B with smooth synth pads, 808 bass, late night feel |
| `salsa` | 180 | fiery | salsa, latin, cuban | Cuban salsa dura with driving tumbao piano, Fania Records inspired |
| `bachata` | 130 | romantic | bachata, latin, dominican | Dominican bachata romántica with requinto guitar, Romeo Santos inspired |
| `kizomba` | 95 | sensual | kizomba, zouk, african | Angolan kizomba with deep electronic bass, Lusophone African sound |

### Using Music Presets

**Via CLI:**
```bash
uv run ai-content music --style jazz --provider lyria --duration 30
uv run ai-content music --style ethiopian-jazz --provider minimax --lyrics lyrics.txt
```

**Via Python:**
```python
from ai_content.presets import get_music_preset
from ai_content import ProviderRegistry

preset = get_music_preset("jazz")
provider = ProviderRegistry.get_music("lyria")

result = await provider.generate(
    prompt=preset.prompt,
    bpm=preset.bpm,
    duration_seconds=30
)
```

---

## Video Presets

All video presets include:
- **Prompt**: Detailed scene description
- **Aspect Ratio**: Video dimensions
- **Duration**: Recommended duration (seconds)
- **Style Keywords**: Visual style tags

### Available Video Presets

| Preset Name | Aspect Ratio | Duration | Style Keywords | Description |
|-------------|--------------|----------|----------------|-------------|
| `nature` | 16:9 | 5 | documentary, wildlife, golden-hour | Majestic lion in savanna, nature documentary style, David Attenborough aesthetic |
| `urban` | 21:9 | 5 | cyberpunk, urban, neon | Neon-lit Tokyo streets at night, Blade Runner inspired, cyberpunk aesthetic |
| `space` | 16:9 | 5 | sci-fi, space, contemplative | Astronaut in space station, Interstellar inspired, emotional and contemplative |
| `abstract` | 1:1 | 5 | abstract, commercial, satisfying | Flowing liquid metal morphing, high-end commercial quality, satisfying abstract art |
| `ocean` | 16:9 | 5 | ocean, underwater, paradise | Crystal clear turquoise ocean waves, 4K underwater cinematography |
| `fantasy` | 21:9 | 5 | fantasy, dragon, epic | Ancient dragon soaring over mountains, Lord of the Rings inspired, epic crane shot |
| `portrait` | 9:16 | 5 | portrait, fashion, beauty | Close-up portrait with striking features, fashion photography aesthetic, 4K beauty |

### Using Video Presets

**Via CLI:**
```bash
uv run ai-content video --style nature --provider veo --duration 5
uv run ai-content video --style space --provider kling --aspect 16:9
```

**Via Python:**
```python
from ai_content.presets import get_video_preset
from ai_content import ProviderRegistry

preset = get_video_preset("nature")
provider = ProviderRegistry.get_video("veo")

result = await provider.generate(
    prompt=preset.prompt,
    aspect_ratio=preset.aspect_ratio,
    duration_seconds=preset.duration
)
```

---

## Preset System Architecture

### Data Structure

**Music Preset:**
```python
@dataclass(frozen=True)
class MusicPreset:
    name: str           # Unique identifier
    prompt: str         # Style description
    bpm: int           # Beats per minute
    mood: str          # Emotional tone
    tags: list[str]    # Style tags
```

**Video Preset:**
```python
@dataclass(frozen=True)
class VideoPreset:
    name: str              # Unique identifier
    prompt: str            # Scene description
    aspect_ratio: str      # Video dimensions
    duration: int          # Recommended duration
    style_keywords: list[str]  # Visual style tags
```

### Preset Registry

Presets are stored in dictionaries:
- **Music**: `MUSIC_PRESETS` in `presets/music.py`
- **Video**: `VIDEO_PRESETS` in `presets/video.py`

### Access Functions

```python
# Get a preset
from ai_content.presets import get_music_preset, get_video_preset

jazz_preset = get_music_preset("jazz")
nature_preset = get_video_preset("nature")

# List all presets
from ai_content.presets import list_music_presets, list_video_presets

all_music = list_music_presets()  # Returns: ['jazz', 'blues', ...]
all_video = list_video_presets()  # Returns: ['nature', 'urban', ...]
```

---

## How to Add a New Preset

### Adding a Music Preset

1. **Define the preset** in `src/ai_content/presets/music.py`:

```python
MY_NEW_PRESET = MusicPreset(
    name="my-new-style",
    prompt="""[My Style Description]
[Instrument details]
[Atmospheric elements]
Mood and inspiration""",
    bpm=120,
    mood="energetic",
    tags=["genre", "subgenre", "characteristic"],
)

# Add to registry
MUSIC_PRESETS: dict[str, MusicPreset] = {
    preset.name: preset
    for preset in [
        JAZZ,
        BLUES,
        # ... existing presets ...
        MY_NEW_PRESET,  # Add here
    ]
}
```

2. **Use it:**
```bash
uv run ai-content music --style my-new-style --provider lyria
```

### Adding a Video Preset

1. **Define the preset** in `src/ai_content/presets/video.py`:

```python
MY_NEW_VIDEO = VideoPreset(
    name="my-video-style",
    prompt="""Detailed scene description,
cinematic elements,
visual style references,
technical specifications""",
    aspect_ratio="16:9",
    duration=5,
    style_keywords=["keyword1", "keyword2"],
)

# Add to registry
VIDEO_PRESETS: dict[str, VideoPreset] = {
    preset.name: preset
    for preset in [
        NATURE,
        URBAN,
        # ... existing presets ...
        MY_NEW_VIDEO,  # Add here
    ]
}
```

2. **Use it:**
```bash
uv run ai-content video --style my-video-style --provider veo
```

---

## Preset Best Practices

1. **Use Presets First**: Start with presets before crafting custom prompts - they're optimized for good results
2. **Combine with Custom Prompts**: You can override preset prompts with `--prompt` if needed
3. **Experiment with BPM**: Music presets suggest BPM, but you can adjust with `--bpm`
4. **Aspect Ratios**: Video presets have recommended aspect ratios, but you can override with `--aspect`

---

## Listing Presets via CLI

```bash
# List all music presets
uv run ai-content list-presets

# List all providers
uv run ai-content list-providers
```

The CLI will show presets with their BPM/mood (music) or aspect ratios (video).

