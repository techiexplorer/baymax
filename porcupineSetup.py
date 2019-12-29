import os
# This module performs conversions between Python values and C structs represented as Python bytes objects.
import struct
from datetime import datetime

import pyaudio

from porcupine import Porcupine


class Baymax:
    def __init__(self):

        # Get paths and handle sensitivity of wake-word Baymax
        self.library_path = "porcupineResources/libpv_porcupine.dll"
        self.model_file_path = "porcupineResources/porcupine_params.pv"
        self.keyword_file_paths = ["ppn/bae_max_windows_2020-01-28.ppn"]
        self.sensitivities = [0.5]

        # Init them as None
        self.baymaxPorcupine = self.audio_stream = self.audio_instance = None

        # Only Baymax is there for now
        self.num_keywords = len(self.keyword_file_paths)
        self.keyword_names = list()
        for x in self.keyword_file_paths:
            self.keyword_names.append(os.path.basename(x).replace('.ppn', '').replace('_compressed', '').split('_')[0])

    def get_baymax_porcupine(self):
        # New instance of Porcupine for Baymax
        self.baymaxPorcupine = Porcupine(
            self.library_path,
            self.model_file_path,
            keyword_file_paths=self.keyword_file_paths,
            sensitivities=self.sensitivities
        )

    def get_audio_stream(self):
        self.audio_instance = pyaudio.PyAudio()
        return self.audio_instance.open(
            rate=self.baymaxPorcupine.sample_rate,
            channels=1,
            input=True,
            format=pyaudio.paInt16,
            frames_per_buffer=self.baymaxPorcupine.frame_length,
            input_device_index=None
        )

    def start_listening_for_baymax(self):
        try:
            self.get_baymax_porcupine()
            while True:
                self.audio_stream = self.get_audio_stream()
                pcm = self.audio_stream.read(self.baymaxPorcupine.frame_length)
                pcm = struct.unpack_from("h" * self.baymaxPorcupine.frame_length, pcm)
                result = self.baymaxPorcupine.process(pcm)
                if self.num_keywords == 1 and result:
                    print(f'detected keyword Baymax {str(datetime.now())}')

        finally:
            if self.baymaxPorcupine is not None:
                self.baymaxPorcupine.delete()

            if self.audio_stream is not None:
                self.audio_stream.close()

            if self.audio_instance is not None:
                self.audio_instance.terminate()


Baymax().start_listening_for_baymax()
