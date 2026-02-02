# Codebase Architecture

## Overview

The `ai-content` package is a multi-provider AI content generation framework that supports music, video, and image creation. It follows a plugin-based architecture with clear separation of concerns.

## Package Structure

```
src/ai_content/
├── core/              # Core abstractions and protocols
│   ├── provider.py    # Protocol definitions (MusicProvider, VideoProvider, ImageProvider)
│   ├── registry.py    # ProviderRegistry - decorator-based registration system
│   ├── result.py     # GenerationResult - standardized output format
│   ├── exceptions.py  # Custom exception hierarchy
│   └── job_tracker.py # SQLite-based job tracking and duplicate detection
│
├── providers/         # Provider implementations (plugin-style)
│   ├── google/       # Google Gemini APIs
│   │   ├── lyria.py  # Real-time music generation
│   │   ├── veo.py    # Video generation
│   │   └── imagen.py # Image generation
│   ├── aimlapi/      # AIMLAPI wrapper
│   │   ├── client.py # HTTP client for AIMLAPI
│   │   └── minimax.py # MiniMax Music 2.0 provider
│   └── kling/        # KlingAI direct API
│       └── direct.py # KlingAI video provider
│
├── pipelines/        # Orchestration workflows
│   ├── base.py       # PipelineResult, PipelineConfig abstractions
│   ├── music.py      # MusicPipeline - music generation workflow
│   ├── video.py      # VideoPipeline - video generation workflow
│   └── full.py       # FullContentPipeline - end-to-end music video pipeline
│
├── presets/          # Pre-configured style templates
│   ├── music.py      # Music style presets (jazz, blues, cinematic, etc.)
│   └── video.py      # Video style presets (nature, urban, space, etc.)
│
├── config/          # Configuration management
│   ├── settings.py  # Pydantic settings with environment variable loading
│   └── loader.py    # YAML config file support
│
├── cli/             # Command-line interface
│   └── main.py      # Typer-based CLI with async command handlers
│
├── integrations/    # External service integrations
│   ├── archive.py   # Archive.org search integration
│   ├── media.py     # FFmpeg media processing utilities
│   └── youtube.py   # YouTube upload functionality
│
└── utils/           # Utility modules
    ├── file_handlers.py  # File download, path generation, cleanup
    ├── lyrics_parser.py  # Structured lyrics parsing with tags
    └── retry.py          # Retry logic with exponential backoff
```

## Key Design Patterns

### 1. Provider Registry Pattern

Providers register themselves using decorators, enabling plugin-style extensibility:

```python
@ProviderRegistry.register_music("lyria")
class GoogleLyriaProvider:
    # Implementation
    pass
```

**Benefits:**
- No need to modify core code to add new providers
- Lazy instantiation (singleton pattern)
- Type-safe provider access via `ProviderRegistry.get_music("lyria")`

### 2. Protocol-Based Interfaces

Uses Python `Protocol` for structural subtyping (duck typing with type safety):

```python
@runtime_checkable
class MusicProvider(Protocol):
    supports_vocals: bool
    supports_realtime: bool
    async def generate(...) -> GenerationResult
```

**Benefits:**
- No inheritance required - any class implementing the methods works
- Type checkers can verify interface compliance
- Flexible provider implementations

### 3. Pipeline Orchestration

Pipelines coordinate multiple generation steps:

- **MusicPipeline**: Handles music generation with retry logic
- **VideoPipeline**: Handles video generation with polling
- **FullContentPipeline**: Orchestrates complete music video creation:
  1. Generate music and keyframe image (parallel)
  2. Generate video from keyframe
  3. Merge audio and video with FFmpeg
  4. Export locally (always)
  5. Optional upload to YouTube/S3

### 4. Job Tracking System

SQLite-based persistence for:
- **Duplicate Detection**: MD5 hash prevents redundant API calls
- **Status Lifecycle**: `queued` → `processing` → `completed` → `downloaded` (or `failed`)
- **Cost Management**: Track API usage across sessions
- **Async Job Handling**: For long-running generations (MiniMax takes 5-15 min)

## Data Flow

### Music Generation Flow

```
CLI Command
    ↓
CLI Handler (main.py)
    ↓
ProviderRegistry.get_music("lyria")
    ↓
GoogleLyriaProvider.generate()
    ↓
WebSocket Connection → Real-time streaming
    ↓
GenerationResult (with file_path or data)
    ↓
JobTracker.create_job() → SQLite persistence
    ↓
File saved to output directory
```

### Video Generation Flow

```
CLI Command
    ↓
CLI Handler
    ↓
ProviderRegistry.get_video("veo")
    ↓
GoogleVeoProvider.generate()
    ↓
API Call → Polling for completion
    ↓
GenerationResult
    ↓
File saved
```

## Configuration System

Uses Pydantic `BaseSettings` for type-safe configuration:

1. **Environment Variables**: `.env` file with `GEMINI_API_KEY`, `AIMLAPI_KEY`, etc.
2. **YAML Config**: Optional `configs/default.yaml` for advanced settings
3. **Settings Hierarchy**: Global → Provider-specific settings

## Error Handling

Custom exception hierarchy:
- `AIContentError` (base)
  - `ProviderError`
  - `AuthenticationError`
  - `RateLimitError`
  - `GenerationError`
  - `TimeoutError`
  - `ConfigurationError`
  - `UnsupportedOperationError`

## Async Architecture

- All providers use `async/await` for non-blocking operations
- CLI commands use `asyncio.run()` to bridge sync/async
- Supports concurrent generation (music + image in parallel)

## Extensibility Points

1. **Add New Provider**: Create class, implement Protocol, register with decorator
2. **Add New Preset**: Add to `MUSIC_PRESETS` or `VIDEO_PRESETS` dict
3. **Add New Pipeline**: Extend `PipelineConfig` and create pipeline class
4. **Add New Integration**: Create module in `integrations/`

## Dependencies

- **Typer**: CLI framework
- **Rich**: Terminal formatting and logging
- **Pydantic**: Settings and validation
- **httpx**: Async HTTP client
- **google-genai**: Google Gemini API client
- **websockets**: Real-time music streaming

