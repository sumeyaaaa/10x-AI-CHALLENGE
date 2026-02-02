# How to Enable Google Music Generation API

## Step-by-Step Guide

### 1. Go to Google Cloud Console
Visit: https://console.cloud.google.com/

### 2. Select or Create a Project
- If you have a project, select it from the dropdown
- If not, create a new project:
  - Click "Select a project" → "New Project"
  - Give it a name (e.g., "AI Content Generation")
  - Click "Create"

### 3. Enable the Music Generation API
1. Go to **APIs & Services** → **Library**
2. Search for: **"Music Generation API"** or **"Gemini API"**
3. Click on the API
4. Click **"Enable"** button

**Alternative: Direct Link**
- Go to: https://console.cloud.google.com/apis/library
- Search for "Gemini API" or "Generative Language API"
- Enable it

### 4. Verify API Key Permissions
1. Go to **APIs & Services** → **Credentials**
2. Find your API key (the one in your `.env` file)
3. Click on it to edit
4. Under **"API restrictions"**:
   - Select **"Restrict key"**
   - Check **"Generative Language API"** or **"Gemini API"**
   - Save

### 5. Check API Key Restrictions
Make sure your API key:
- ✅ Is not restricted to specific IPs (unless you're using a server)
- ✅ Has the correct API enabled
- ✅ Is not expired

### 6. Test Again
After enabling the API, wait 1-2 minutes, then try:
```bash
uv run ai-content music --style jazz --provider lyria --duration 30
```

**✅ Success Confirmed:**
- API is now working correctly
- Successfully generated 5 audio files
- Files saved in `exports/` directory

## Common Issues

**Issue:** "API key not valid"
- **Solution:** Make sure the API is enabled for your project
- **Solution:** Verify the API key is associated with the correct project

**Issue:** "Permission denied"
- **Solution:** Check API key restrictions in Credentials
- **Solution:** Ensure the API is enabled

**Issue:** API not found
- **Solution:** The API might be called "Generative Language API" instead
- **Solution:** Enable "Gemini API" which includes music generation

## Quick Check
To verify your API key works, you can test it directly:
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_API_KEY"
```

Replace `YOUR_API_KEY` with your actual key from `.env`.

---

## Video Generation API

The same API key and permissions work for video generation (Veo). However, there was a codebase issue that has been fixed:

**Fixed Issues:**
- Changed `generate_video` → `generate_videos` (correct method name)
- Removed `GenerateVideoConfig` object (doesn't exist in API)
- Pass parameters directly: `aspect_ratio` and `person_generation`

**Test Video Generation:**
```bash
uv run ai-content video --style nature --provider veo --duration 5
```

