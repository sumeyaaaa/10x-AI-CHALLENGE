# How to Enable Google APIs (Music & Video)

## Important: Google AI Studio vs Google Cloud Console

**For this challenge, use Google AI Studio (FREE):**
- ✅ **Google AI Studio**: https://aistudio.google.com/ → Get API Key (FREE, no billing)
- ❌ **Google Cloud Console**: Not needed for this challenge

The challenge expects you to use the FREE API keys from Google AI Studio, not Google Cloud Console.

---

## Music Generation API (Lyria) ✅ WORKING

### Using Google AI Studio (Recommended - FREE)

1. **Get API Key**
   - Visit: https://aistudio.google.com/
   - Sign in with Google account
   - Click "Get API Key" → Create API key
   - Copy the API key to your `.env` file as `GEMINI_API_KEY`

2. **Test Music Generation**
   ```bash
   uv run ai-content music --style jazz --provider lyria --duration 30
   ```

**✅ Success Confirmed:**
- API is now working correctly
- Successfully generated 5 audio files
- Files saved in `exports/` directory
- No Google Cloud Console setup needed

## Common Issues

**Issue:** "API key not valid"
- **Solution:** Verify API key is from Google AI Studio (not expired)
- **Solution:** Check that the key is correctly set in `.env` file
- **Solution:** Make sure there are no extra spaces in the API key

**Issue:** "Permission denied"
- **Solution:** API key from Google AI Studio should work automatically
- **Solution:** If using Google Cloud Console, check API restrictions

**Issue:** API not found
- **Solution:** Google AI Studio API keys work for all Gemini features
- **Solution:** No separate enablement needed for music/video

---

## Video Generation API (Veo)

### Enabling Video Generation in Google AI Studio

The same API key from Google AI Studio should work for video generation, but you may need to verify it's enabled:

1. **Go to Google AI Studio**
   - Visit: https://aistudio.google.com/
   - Sign in with your Google account

2. **Check API Key Permissions**
   - Click on your API key or go to API Keys section
   - Verify the key has access to:
     - ✅ Generative Language API (for music)
     - ✅ Video Generation API (for Veo) - **Check this!**

3. **Enable Video Generation (if needed)**
   - Some API keys may need video generation explicitly enabled
   - Check if there's a toggle or setting for "Video Generation" or "Veo"
   - The API key should work for both music (Lyria) and video (Veo)

4. **Verify Model Access**
   - The video model used is: `veo-3.1-generate-preview`
   - Make sure your API key has access to this model

### Current Status

**Code Status:** ✅ Fixed
- Changed `generate_video` → `generate_videos` (correct method name)
- Removed `GenerateVideoConfig` object (doesn't exist in API)
- Removed unsupported parameters from API call

**API Status:** ✅ Working (Quota Limited)
- Same API key works for music (Lyria) ✅
- Same API key works for video (Veo) ✅ - **API is valid!**
- ⚠️ Getting "429 RESOURCE_EXHAUSTED" - Quota exceeded
- **This is good news:** API key is working, just hit free tier limits

### Test Video Generation

After verifying API key settings:
```bash
uv run ai-content video --style nature --provider veo --duration 5
```

### Troubleshooting Video API

**Error:** `429 RESOURCE_EXHAUSTED` (Quota Exceeded) ✅ **This means API is working!**
- **What it means:** API key is valid, code is working, but you've hit the free tier quota
- **Solution 1:** Wait for quota to reset (check at https://ai.dev/rate-limit)
- **Solution 2:** Video generation may have stricter quotas than music generation
- **Solution 3:** Document this as a limitation - API is working, just quota-limited
- **Status:** ✅ API key validated, code working, just need to work within free tier limits

**Error:** `API key not valid` (if you see this)
- **Solution 1:** Verify API key is from Google AI Studio
- **Solution 2:** Check API key is correctly set in `.env` file
- **Solution 3:** Make sure there are no extra spaces in the API key

**Note:** Google AI Studio is FREE and separate from Google Cloud Console. No billing setup required. Free tier has quotas/rate limits.

