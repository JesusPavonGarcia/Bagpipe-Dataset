# Copyright 2024 The DDSP Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helper functions for running DDSP colab notebooks."""

import base64
import io
import pickle
import sounddevice as sd
import ddsp
import ddsp.training
#from google.colab import files
#from google.colab import output
from IPython import display
import note_seq
import numpy as np
from scipy.io import wavfile
import tensorflow.compat.v2 as tf

#download = files.download

DEFAULT_SAMPLE_RATE = ddsp.spectral_ops.CREPE_SAMPLE_RATE

_play_count = 0  # Used for ephemeral play().

# Alias these for backwards compatibility and ease.
specplot = ddsp.training.plotting.specplot
plot_impulse_responses = ddsp.training.plotting.plot_impulse_responses
transfer_function = ddsp.training.plotting.transfer_function


# ------------------------------------------------------------------------------
# IO
# ------------------------------------------------------------------------------
def play(array_of_floats, sample_rate=DEFAULT_SAMPLE_RATE, autoplay=False):
    """Reproduce audio en Jupyter o IPython local usando HTML."""
    # Si es batched, toma el primer elemento
    if len(array_of_floats.shape) == 2:
        array_of_floats = array_of_floats[0]

    # Normaliza y convierte a int16
    normalizer = float(np.iinfo(np.int16).max)
    array_of_ints = np.array(array_of_floats * normalizer, dtype=np.int16)

    # Convierte a WAV en memoria
    memfile = io.BytesIO()
    wavfile.write(memfile, sample_rate, array_of_ints)

    # Codifica a base64 para HTML
    audio_data = base64.b64encode(memfile.getvalue()).decode('ascii')
    memfile.close()

    # Muestra widget HTML
    html = f"""
    <audio controls {'autoplay' if autoplay else ''}>
        <source src="data:audio/wav;base64,{audio_data}" type="audio/wav">
        Tu navegador no soporta audio HTML5.
    </audio>
    """
    display.display(display.HTML(html))

def record(seconds=3, sample_rate=DEFAULT_SAMPLE_RATE, normalize_db=0.1):
    """Graba audio desde el micrófono local usando sounddevice."""
    print(f'Grabando {seconds} segundos de audio...')
    audio = sd.rec(int(seconds * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # Espera a que termine la grabación
    print('¡Grabación completada!')

    audio = np.squeeze(audio)

    if normalize_db is not None:
        audio = normalize_audio(audio, normalize_db)

    return audio

def normalize_audio(audio, target_db=0.1):
    """Normaliza el audio a un nivel específico de dB RMS."""
    rms = np.sqrt(np.mean(audio**2))
    if rms > 0:
        scalar = 10**(target_db / 20) / rms
        audio *= scalar
        audio = np.clip(audio, -1.0, 1.0)
    return audio

def audio_bytes_to_np(wav_data,
                      sample_rate=DEFAULT_SAMPLE_RATE,
                      normalize_db=0.1,
                      mono=True):
  """Convert audio file data (in bytes) into a numpy array using Pydub.

  Args:
    wav_data: A byte stream of audio data.
    sample_rate: Resample recorded audio to this sample rate.
    normalize_db: Normalize the audio to this many decibels. Set to None to skip
      normalization step.
    mono: Force stereo signals to single channel. If false, output can one or
      two channels depending on the source signal.

  Returns:
    An array of the recorded audio at sample_rate, shape [channels, time].
  """
  return note_seq.audio_io.wav_data_to_samples_pydub(
      wav_data=wav_data, sample_rate=sample_rate, normalize_db=normalize_db,
      num_channels=1 if mono else None)


def upload(audio_files, sample_rate=DEFAULT_SAMPLE_RATE, normalize_db=None):
  """Load a collection of audio files (.wav, .mp3) from disk into colab.

  Args:
    sample_rate: Resample recorded audio to this sample rate.
    normalize_db: Normalize the audio to this many decibels. Set to None to skip
      normalization step.

  Returns:
    An tuple of lists, (filenames, numpy_arrays).
  """
  #audio_files = files.upload()
  fnames = list(audio_files.keys())
  audio = []
  for fname in fnames:
    file_audio = audio_bytes_to_np(audio_files[fname],
                                   sample_rate=sample_rate,
                                   normalize_db=normalize_db)
    audio.append(file_audio)
  return fnames, audio


def save_dataset_statistics(data_provider,
                            file_path=None,
                            batch_size=1,
                            power_frame_size= 256, power_frame_rate= 250):
  """Calculate dataset stats and save in a pickle file.

  Calls out to postprocessing.compute_dataset_statistics.

  Args:
    data_provider: A DataProvider from ddsp.training.data.
    file_path: Path for saved pickle file of dataset statistics.
    batch_size: Iterate over dataset with this batch size.
    power_frame_size: Calculate power features on the fly with this frame size.

  Returns:
    Dictionary of dataset statistics. This is an overcomplete set of statistics,
    as there are now several different tone transfer implementations (js, colab,
    vst) that need different statistics for normalization.
  """

  ds_stats = ddsp.training.postprocessing.compute_dataset_statistics(
      data_provider, batch_size, power_frame_size,power_frame_rate)

  # Save.
  if file_path is not None:
    with tf.io.gfile.GFile(file_path, 'wb') as f:
      pickle.dump(ds_stats, f)
    print(f'Done! Saved dataset statistics to: {file_path}')

  return ds_stats


# ------------------------------------------------------------------------------
# Frequency tuning
# ------------------------------------------------------------------------------
def get_tuning_factor(f0_midi, f0_confidence, mask_on):
  """Get an offset in cents, to most consistent set of chromatic intervals."""
  # Difference from midi offset by different tuning_factors.
  tuning_factors = np.linspace(-0.5, 0.5, 101)  # 1 cent divisions.
  midi_diffs = (f0_midi[mask_on][:, np.newaxis] -
                tuning_factors[np.newaxis, :]) % 1.0
  midi_diffs[midi_diffs > 0.5] -= 1.0
  weights = f0_confidence[mask_on][:, np.newaxis]

  ## Computes mininmum adjustment distance.
  cost_diffs = np.abs(midi_diffs)
  cost_diffs = np.mean(weights * cost_diffs, axis=0)

  ## Computes mininmum "note" transitions.
  f0_at = f0_midi[mask_on][:, np.newaxis] - midi_diffs
  f0_at_diffs = np.diff(f0_at, axis=0)
  deltas = (f0_at_diffs != 0.0).astype(float)
  cost_deltas = np.mean(weights[:-1] * deltas, axis=0)

  # Tuning factor is minimum cost.
  norm = lambda x: (x - np.mean(x)) / np.std(x)
  cost = norm(cost_deltas) + norm(cost_diffs)
  return tuning_factors[np.argmin(cost)]


def auto_tune(f0_midi, tuning_factor, mask_on, amount=0.0, chromatic=False):
  """Reduce variance of f0 from the chromatic or scale intervals."""
  if chromatic:
    midi_diff = (f0_midi - tuning_factor) % 1.0
    midi_diff[midi_diff > 0.5] -= 1.0
  else:
    major_scale = np.ravel(
        [np.array([0, 2, 4, 5, 7, 9, 11]) + 12 * i for i in range(10)])
    all_scales = np.stack([major_scale + i for i in range(12)])

    f0_on = f0_midi[mask_on]
    # [time, scale, note]
    f0_diff_tsn = (
        f0_on[:, np.newaxis, np.newaxis] - all_scales[np.newaxis, :, :])
    # [time, scale]
    f0_diff_ts = np.min(np.abs(f0_diff_tsn), axis=-1)
    # [scale]
    f0_diff_s = np.mean(f0_diff_ts, axis=0)
    scale_idx = np.argmin(f0_diff_s)
    scale = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb',
             'G', 'Ab', 'A', 'Bb', 'B', 'C'][scale_idx]

    # [time]
    f0_diff_tn = f0_midi[:, np.newaxis] - all_scales[scale_idx][np.newaxis, :]
    note_idx = np.argmin(np.abs(f0_diff_tn), axis=-1)
    midi_diff = np.take_along_axis(
        f0_diff_tn, note_idx[:, np.newaxis], axis=-1)[:, 0]
    print('Autotuning... \nInferred key: {}  '
          '\nTuning offset: {} cents'.format(scale, int(tuning_factor * 100)))

  # Adjust the midi signal.
  return f0_midi - amount * midi_diff
