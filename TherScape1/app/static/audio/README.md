# Forest Audio Setup Instructions

## 📁 File Placement

Place your downloaded forest sounds MP3 file in this directory with the exact name:

```
forest-sounds.mp3
```

## 🎵 Recommended Audio Settings

For the best therapeutic experience, your forest sounds audio file should have:

- **Format**: MP3 (most compatible)
- **Duration**: 10+ minutes (for seamless looping)
- **Quality**: 128kbps or higher
- **Volume**: Normalized/consistent level
- **Content**: Ambient forest sounds (birds, wind, leaves, water)

## 🌲 Suggested Forest Sound Sources

1. **YouTube to MP3 Conversion**:

   - Use the provided link: https://www.youtube.com/watch?v=xNN7iTA57jM
   - Convert using online tools like youtube-mp3.org or 4K Video Downloader

2. **Free Sound Libraries**:

   - Freesound.org (search: "forest ambience")
   - Zapsplat.com (free with registration)
   - BBC Sound Effects Library

3. **Premium Sources**:
   - Epidemic Sound
   - AudioJungle
   - Pond5

## 🔧 File Naming Requirements

The file MUST be named exactly: `forest-sounds.mp3`

If you want to use a different filename, update line 15 in:
`/static/js/forest-audio.js`

```javascript
this.audio.src = "/static/audio/your-filename.mp3";
```

## 🎛️ Audio Player Features

Once the file is placed correctly, the forest audio player will provide:

- ✅ **Play/Pause Toggle**: Click the tree icon
- ✅ **Volume Control**: Hover to reveal slider
- ✅ **Auto-Loop**: Seamless continuous playback
- ✅ **Keyboard Shortcut**: Ctrl+M to toggle
- ✅ **Visual Feedback**: Sound waves and status messages
- ✅ **Mobile Support**: Responsive design

## 🚀 Testing

1. Place `forest-sounds.mp3` in this folder
2. Restart your Flask application
3. Click the tree icon in the bottom-right corner
4. You should see "Forest sounds playing" status message

## 🐛 Troubleshooting

**If audio doesn't play:**

1. Check file name is exactly `forest-sounds.mp3`
2. Ensure file format is MP3
3. Check browser console for error messages
4. Try a different browser (Chrome/Firefox recommended)
5. Verify file permissions are readable

**Browser Autoplay Restrictions:**

- Some browsers block autoplay until user interaction
- First click might show "Click to enable forest sounds"
- This is normal - just click the button again

## 📱 Browser Compatibility

✅ **Fully Supported:**

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

⚠️ **Limited Support:**

- Internet Explorer (not recommended)
- Older mobile browsers

---

**Need Help?** Check the browser console (F12) for error messages or contact the development team.
