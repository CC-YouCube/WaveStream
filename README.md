# WaveStream

On demand streaming and conversion service for CC: T. \
**This project is currently in development** and will become the base of YC 2.0 when video streaming is supported.

---

## Current API Endpoints

### **Image NFT Converter**

**Endpoint:** `/api/v1/img/nft`  
**Description:** Converts images to NFT format.

| Parameter | Type     | Default    | Description                                  |
|-----------|----------|------------|----------------------------------------------|
| url       | string   | -          | The URL of the image to convert.             |
| width     | integer  | **51**     | The desired width of the output image.       |
| height    | integer  | **19**     | The desired height of the output image.      |
| dither    | boolean  | **false**  | Enables dithering for the image.             |

### **DFPWM Streaming**

**Endpoint:** `/api/v1/audio/dfpwm`  
**Description:** Streams audio in DFPWM format.

| Parameter | Type     | Default  | Description                                         |
|-----------|----------|----------|-----------------------------------------------------|
| url       | string   | -        | The URL to extract from or an youtube search quarry |

### **PCM U8 WAV Streaming**

**Endpoint:** `/api/v1/audio/pcm`  
**Description:** Streams audio in PCM U8 WAV format.

| Parameter | Type     | Default  | Description                                         |
|-----------|----------|----------|-----------------------------------------------------|
| url       | string   | -        | The URL to extract from or an youtube search quarry |

---

## Server requirements

- [Python 3]
- [FFmpeg 5.1+]
- [requirements.txt]

---

## Displaying nft

### [cc.image.nft]

**Example soon™**

### [Pixelbox Lite] / [Pixelbox Modules]

**Example soon™**

---

## Audio Clients

### [Speaker.lua] (Integrated in CC: T)

- **Command:** `speaker play <url> [speaker]`

### [AUKit]

#### For PCM

- **Command:** `austream <url> type=pcm,dataType=signed,streamData=true`

#### For DFPWM

- **Command:** `austream <url> type=dfpwm,streamData=true`

### YouCube

- **Status:** Coming soon™

### [Musicify]

- **Status:** Maybe Coming soon™

---


## Video Clients

**Coming soon™**

---

## Public Servers

- https://wavestream-w2q4.onrender.com

[Musicify]: https://github.com/knijn/musicify
[AUKit]: https://github.com/MCJack123/AUKit
[Speaker.lua]: https://github.com/cc-tweaked/CC-Tweaked/blob/mc-1.20.x/projects/core/src/main/resources/data/computercraft/lua/rom/programs/fun/speaker.lua
[cc.image.nft]: https://tweaked.cc/library/cc.image.nft.html
[Pixelbox Lite]: https://github.com/9551-Dev/pixelbox_lite
[Pixelbox Modules]: https://github.com/9551-Dev/pixelbox_modules
[Python 3]: https://www.python.org/downloads/
[FFmpeg 5.1+]: https://ffmpeg.org/
[requirements.txt]: requirements.txt
