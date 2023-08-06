# PyPocketsphinx

PyPocketsphinx is a fork of [Pocketsphinx Python](https://github.com/bambocher/pocketsphinx-python) with the following changes:

* Fixes OSX installation issue described in [issue #28](https://github.com/bambocher/pocketsphinx-python/issues/28) using fix from [pull request #44](https://github.com/bambocher/pocketsphinx-python/pull/44)

## Installation

```shell
# Make sure we have up-to-date versions of pip, setuptools and wheel
python -m pip install --upgrade pip setuptools wheel
pip install --upgrade pypocketsphinx
```

## Usage

### LiveSpeech

It's an iterator class for continuous recognition or keyword search from a microphone.

```python
from pypocketsphinx import LiveSpeech
for phrase in LiveSpeech(): print(phrase)
```

An example of a keyword search:

```python
from pypocketsphinx import LiveSpeech

speech = LiveSpeech(lm=False, keyphrase='forward', kws_threshold=1e-20)
for phrase in speech:
    print(phrase.segments(detailed=True))
```

With your model and dictionary:

```python
import os
from pypocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(model_path, 'en-us'),
    lm=os.path.join(model_path, 'en-us.lm.bin'),
    dic=os.path.join(model_path, 'cmudict-en-us.dict')
)

for phrase in speech:
    print(phrase)
```

### AudioFile

It's an iterator class for continuous recognition or keyword search from a file.

```python
from pypocketsphinx import AudioFile
for phrase in AudioFile(): print(phrase) # => "go forward ten meters"
```

An example of a keyword search:

```python
from pypocketsphinx import AudioFile

audio = AudioFile(lm=False, keyphrase='forward', kws_threshold=1e-20)
for phrase in audio:
    print(phrase.segments(detailed=True)) # => "[('forward', -617, 63, 121)]"
```

With your model and dictionary:

```python
import os
from pypocketsphinx import AudioFile, get_model_path, get_data_path

model_path = get_model_path()
data_path = get_data_path()

config = {
    'verbose': False,
    'audio_file': os.path.join(data_path, 'goforward.raw'),
    'buffer_size': 2048,
    'no_search': False,
    'full_utt': False,
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join(model_path, 'cmudict-en-us.dict')
}

audio = AudioFile(**config)
for phrase in audio:
    print(phrase)
```

Convert frame into time coordinates:

```python
from pypocketsphinx import AudioFile

# Frames per Second
fps = 100

for phrase in AudioFile(frate=fps):  # frate (default=100)
    print('-' * 28)
    print('| %5s |  %3s  |   %4s   |' % ('start', 'end', 'word'))
    print('-' * 28)
    for s in phrase.seg():
        print('| %4ss | %4ss | %8s |' % (s.start_frame / fps, s.end_frame / fps, s.word))
    print('-' * 28)

# ----------------------------
# | start |  end  |   word   |
# ----------------------------
# |  0.0s | 0.24s | <s>      |
# | 0.25s | 0.45s | <sil>    |
# | 0.46s | 0.63s | go       |
# | 0.64s | 1.16s | forward  |
# | 1.17s | 1.52s | ten      |
# | 1.53s | 2.11s | meters   |
# | 2.12s |  2.6s | </s>     |
# ----------------------------
```

### Pocketsphinx

It's a simple and flexible proxy class to `pocketsphinx.Decode`.

```python
from pypocketsphinx import Pocketsphinx
print(Pocketsphinx().decode()) # => "go forward ten meters"
```

A more comprehensive example:

```python
from __future__ import print_function
import os
from pypocketsphinx import Pocketsphinx, get_model_path, get_data_path

model_path = get_model_path()
data_path = get_data_path()

config = {
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join(model_path, 'cmudict-en-us.dict')
}

ps = Pocketsphinx(**config)
ps.decode(
    audio_file=os.path.join(data_path, 'goforward.raw'),
    buffer_size=2048,
    no_search=False,
    full_utt=False
)

print(ps.segments()) # => ['<s>', '<sil>', 'go', 'forward', 'ten', 'meters', '</s>']
print('Detailed segments:', *ps.segments(detailed=True), sep='\n') # => [
#     word, prob, start_frame, end_frame
#     ('<s>', 0, 0, 24)
#     ('<sil>', -3778, 25, 45)
#     ('go', -27, 46, 63)
#     ('forward', -38, 64, 116)
#     ('ten', -14105, 117, 152)
#     ('meters', -2152, 153, 211)
#     ('</s>', 0, 212, 260)
# ]

print(ps.hypothesis())  # => go forward ten meters
print(ps.probability()) # => -32079
print(ps.score())       # => -7066
print(ps.confidence())  # => 0.04042641466841839

print(*ps.best(count=10), sep='\n') # => [
#     ('go forward ten meters', -28034)
#     ('go for word ten meters', -28570)
#     ('go forward and majors', -28670)
#     ('go forward and meters', -28681)
#     ('go forward and readers', -28685)
#     ('go forward ten readers', -28688)
#     ('go forward ten leaders', -28695)
#     ('go forward can meters', -28695)
#     ('go forward and leaders', -28706)
#     ('go for work ten meters', -28722)
# ]
```

### Default config

If you don't pass any argument while creating an instance of the Pocketsphinx, AudioFile or LiveSpeech class, it will use next default values:

```python
verbose = False
logfn = /dev/null or nul
audio_file = site-packages/pocketsphinx/data/goforward.raw
audio_device = None
sampling_rate = 16000
buffer_size = 2048
no_search = False
full_utt = False
hmm = site-packages/pocketsphinx/model/en-us
lm = site-packages/pocketsphinx/model/en-us.lm.bin
dict = site-packages/pocketsphinx/model/cmudict-en-us.dict
```

Any other option must be passed into the config as is, without using symbol `-`.

If you want to disable default language model or dictionary, you can change the value of the corresponding options to False:

```python
lm = False
dict = False
```

### Verbose

Send output to stdout:

```python
from pypocketsphinx import Pocketsphinx

ps = Pocketsphinx(verbose=True)
ps.decode()

print(ps.hypothesis())
```

Send output to file:

```python
from pypocketsphinx import Pocketsphinx

ps = Pocketsphinx(verbose=True, logfn='pypocketsphinx.log')
ps.decode()

print(ps.hypothesis())
```

### Compatibility

Parent classes are still available:

```python
import os
from pypocketsphinx import DefaultConfig, Decoder, get_model_path, get_data_path

model_path = get_model_path()
data_path = get_data_path()

# Create a decoder with a certain model
config = DefaultConfig()
config.set_string('-hmm', os.path.join(model_path, 'en-us'))
config.set_string('-lm', os.path.join(model_path, 'en-us.lm.bin'))
config.set_string('-dict', os.path.join(model_path, 'cmudict-en-us.dict'))
decoder = Decoder(config)

# Decode streaming data
buf = bytearray(1024)
with open(os.path.join(data_path, 'goforward.raw'), 'rb') as f:
    decoder.start_utt()
    while f.readinto(buf):
        decoder.process_raw(buf, False, False)
    decoder.end_utt()
print('Best hypothesis segments:', [seg.word for seg in decoder.seg()])
```

### Install requirements

Windows requirements:

* [Python](https://www.python.org/downloads)
* [Git](http://git-scm.com/downloads)
* [Swig](http://www.swig.org/download.html)
* [Visual Studio Community](https://www.visualstudio.com/ru-ru/downloads/download-visual-studio-vs.aspx)

Ubuntu requirements:

```shell
sudo apt-get install -qq python python-dev python-pip build-essential swig git libpulse-dev libasound2-dev
```

Mac OS X requirements:

```shell
brew reinstall swig python
```

## License

[The BSD License](https://github.com/bambocher/pocketsphinx-python/blob/master/LICENSE)
