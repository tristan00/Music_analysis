import pydub
import pandas as pd
import numpy as np
import glob
import gc

path = r'/media/td/Samsung_T51/Music/Structured'


class Audio:
    def __init__(self, path):
        self.path = path
        song = pydub.AudioSegment.from_mp3(self.path)
        self.array_type=song.array_type
        self.channels=song.channels
        self.converter=song.converter
        self.dBFS=song.dBFS
        self.duration_seconds=song.duration_seconds
        self.ffmpeg=song.ffmpeg
        self.frame_rate=song.frame_rate
        self.frame_width=song.frame_width
        self.max=song.max
        self.max_dBFS=song.max_dBFS
        self.max_possible_amplitude=song.max_possible_amplitude
        self.rms=song.rms
        self.sample_width=song.sample_width
        self.len_raw_data=len(list(song.raw_data))
        raw_data = list(song.raw_data)

        raw_data_channeled = [raw_data[i::self.frame_width] for i in range(self.frame_width)]
        self.raw_data_array = np.array(raw_data_channeled)

        print(path, len(raw_data), min(raw_data), max(raw_data), self.raw_data_array.shape)
        self.raw_data_array = self.raw_data_array.astype(np.uint8)
        del song, raw_data, raw_data_channeled
        gc.collect()


if __name__ == '__main__':
    files = glob.glob(f'{path}/*/*.mp3')
    print(len(files), files)


    file_lengths = list()

    for i in files:
        song = pydub.AudioSegment.from_mp3(i)
        file_lengths.append({'artist':i.split('/')[-2],
                             'song':i.split('/')[-1].replace('.mp3', ''),
                             'array_type':song.array_type,
                             'channels':song.channels,
                             'converter':song.converter,
                             'dBFS':song.dBFS,
                             'duration_seconds':song.duration_seconds,
                             'ffmpeg':song.ffmpeg,
                             'frame_rate':song.frame_rate,
                             'frame_width':song.frame_width,
                             'max':song.max,
                             'max_dBFS':song.max_dBFS,
                             'max_possible_amplitude':song.max_possible_amplitude,
                             'rms':song.rms,
                             'sample_width': song.sample_width,
                             'len_raw_data':len(list(song.raw_data))})

    pd.DataFrame.from_dict(file_lengths).to_csv('overview.csv', index = False, sep = '|')
