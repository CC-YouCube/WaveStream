# WaveStream

On demand streaming and conversion service for CC: T. \
This project is currently in developed and will become the base of YC 2.0 when video streaming is supported.

## Current Api endpoints

### /img.nft

nft converter

params:
- url
- width (default: 51) 
- height (default: 19)
- dither (default: false)

### /audio.dfpwm

dfpwm streaming

params:
- url

### /audio.pcm

pcm u8 wav streaming

params:
- url

## clients

### speaker.lua (integrated in CC: T)

speaker play <url> [speaker]

### [AUKit](https://github.com/MCJack123/AUKit)

#### for pcm

austream <url> type=pcm,dataType=signed,streamData=true

#### for dfpwm

austream <url> type=dfpwm,streamData=true

### YouCube

Support coming soon

### Musicify

Support coming soon maby


## Public Servers

Soon TM
