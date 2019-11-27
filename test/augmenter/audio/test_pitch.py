import unittest
import os
import numpy as np
from dotenv import load_dotenv

import nlpaug.augmenter.audio as naa
from nlpaug.util import AudioLoader


class TestPitch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        env_config_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', '..', '..', '.env'))
        load_dotenv(env_config_path)
        # https://freewavesamples.com/yamaha-v50-rock-beat-120-bpm
        cls.sample_wav_file = os.path.join(
            os.environ.get("TEST_DIR"), 'res', 'audio', 'Yamaha-V50-Rock-Beat-120bpm.wav'
        )
        cls.audio, cls.sampling_rate = AudioLoader.load_audio(cls.sample_wav_file)

    def test_substitute(self):
        aug = naa.PitchAug(sampling_rate=self.sampling_rate)
        augmented_audio = aug.augment(self.audio)

        self.assertFalse(np.array_equal(self.audio, augmented_audio))
        self.assertEqual(len(self.audio), len(augmented_audio))

    def test_coverage(self):
        zone = (0.3, 0.7)
        coverage = 0.1
        decimal = 8

        aug = naa.MaskAug(sampling_rate=self.sampling_rate, zone=zone, coverage=coverage)
        aug.model.stateless = False
        augmented_audio = aug.augment(self.audio)
        reconstruct_augmented_audio = np.concatenate(
            (self.audio[:aug.model.start_pos], aug.model.aug_data, self.audio[aug.model.end_pos:])
            , axis=0).astype(np.float32)

        augmented_audio = np.round(augmented_audio, decimals=decimal)
        reconstruct_augmented_audio = np.round(reconstruct_augmented_audio, decimals=decimal)

        self.assertTrue(np.array_equal(augmented_audio, reconstruct_augmented_audio))
        self.assertTrue(len(aug.model.aug_data), int(len(self.audio) * (zone[1] - zone[0]) * coverage))

    def test_zone(self):
        zone = (0, 1)
        coverage = 1.
        decimal = 8

        aug = naa.MaskAug(sampling_rate=self.sampling_rate, zone=zone, coverage=coverage)
        aug.model.stateless = False
        augmented_audio = aug.augment(self.audio)
        reconstruct_augmented_audio = np.concatenate(
            (self.audio[:aug.model.start_pos], aug.model.aug_data, self.audio[aug.model.end_pos:])
            , axis=0).astype(np.float32)

        augmented_audio = np.round(augmented_audio, decimals=decimal)
        reconstruct_augmented_audio = np.round(reconstruct_augmented_audio, decimals=decimal)

        self.assertTrue(np.array_equal(augmented_audio, reconstruct_augmented_audio))
        self.assertTrue(len(aug.model.aug_data), int(len(self.audio) * (zone[1] - zone[0]) * coverage))