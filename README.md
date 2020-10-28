
# speech-to-text-async

https://cloud.google.com/speech-to-text?hl=ja

## Run

```sh=
pip3 install --user -r requirements.txt

python3 transcribe.py "gs://[BUCKET_NAME]/[FILE]" [CREDENTIALS_JSON]
or
python3 transcribe.py [FILE] [CREDENTIALS_JSON]
```

## stereo to mono

```sh=
sox [STEREO_AUDIO] -c 1 [OUTPUT]
```

## mp3 to wav

### Prerequirement

```sh=
sudo apt-get install libsox-fmt-mp3
```

### Convert mp3 to wav

```sh=
sox [MP3_AUDIO] -c 1 [OUTPUT]
```
