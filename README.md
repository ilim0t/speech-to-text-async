
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