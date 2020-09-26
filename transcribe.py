#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for async
batch processing.

Example usage:
    python transcribe_async.py resources/audio.raw
    python transcribe_async.py gs://cloud-samples-tests/speech/vr.flac
"""

import argparse
import collections
import io
from typing import List, Tuple

from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account


def transcribe_gcs(gcs_uri, key_path):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    credentials = service_account.Credentials.from_service_account_file(
        key_path, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = speech.SpeechClient(credentials=credentials)

    audio = speech.types.RecognitionAudio(uri=gcs_uri)
    config = speech.types.RecognitionConfig(
        language_code='en-US',
        enable_automatic_punctuation=True,
        enable_speaker_diarization=True,
        diarization_speaker_count=4)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result()

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result
    result = response.results[-1]

    words_info = result.alternatives[0].words

    # Printing out the output:
    for speaker, sentence in align_words(words_info):
        print(f"User {speaker}: {sentence}")


def align_words(words_info) -> List[Tuple[int, str]]:
    sentences: List[Tuple[List[int], List[str]]] = []
    sentence: Tuple[List[int], List[str]] = ([], [])

    for word_info in words_info:
        speaker_tag, word = sentence
        speaker_tag.append(word_info.speaker_tag)
        word.append(word_info.word)

        if any(letter in word_info.word for letter in (".", "?")):
            sentences.append(sentence)
            sentence = ([], [])

    return [(collections.Counter(speaker_tag).most_common()[0][0], " ".join(word)) for speaker_tag, word in sentences]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    parser.add_argument(
        'key_path', help='Path of Credentials')
    args = parser.parse_args()
    assert args.path.startswith('gs://')
    transcribe_gcs(args.path, args.key_path)
