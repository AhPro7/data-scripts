# we will use this script to split the audio files into chunks using start and end time cloumns

# import the required libraries
import os
import pandas as pd
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from pydub import AudioSegment

audio_path = input('Enter the path of the audio files: ')
extion = '.wav'
# load the csv file
path = input('Enter the path of the csv file: ')
save_path = input('Enter the path to save the splitted audio files: ')
#check if the save_path exists
if not os.path.exists(save_path):
    os.makedirs(save_path)
    print('The save path does not exist, created a new one')
hf_token = input('Enter the huggingface token: ')

df = pd.read_csv(path)
print(df.head())

new_df = {

    'video_pth': [],
    'text': []

}
# check if the video_id values in path save in jo-aud folder by the name of video_id+chunk number.wav
from tqdm import tqdm
for i in tqdm(range(len(df))):
    video_id = df['video_id'][i]
    start_time = str(df['start'][i])
    end_time = str(df['end'][i])
    text = df['text'][i]
    # load the audio file
    audio_file = os.path.join(audio_path, video_id+extion)
    # check if the file exists
    if os.path.exists(audio_file):
        # load the audio file
        # audio, sr = librosa.load(audio_file, sr=44100)
        # get the start and end time in seconds in data frame start and end columns has values 00:00:06.140	we need to convert it to milliseconds
        hours, minutes, seconds_milliseconds = start_time.split(':')
        seconds, milliseconds = seconds_milliseconds.split('.')
        start_time_in_ms = int(hours)*3600000 + int(minutes)*60000 + int(seconds)*1000 + int(milliseconds)
        hours, minutes, seconds_milliseconds = end_time.split(':')
        seconds, milliseconds = seconds_milliseconds.split('.')
        end_time_in_ms = int(hours)*3600000 + int(minutes)*60000 + int(seconds)*1000 + int(milliseconds)
        audio_chunk = AudioSegment.from_wav(audio_file)
        audio_chunk = audio_chunk[start_time_in_ms:end_time_in_ms]
        # save the audio chunk
        save_path = save_path # need to make it dynamic
        audio_chunk.export(os.path.join(save_path, video_id+'-'+str(i)+extion), format='wav')
        # add the video path to the new_df
        new_df['video_pth'].append(os.path.join(save_path, video_id+'-'+str(i)+extion))
        # add the text to the new_df
        new_df['text'].append(text)
    else:
        print('The file does not exist: ', audio_file)

# convert the new_df to data frame
new_df = pd.DataFrame(new_df)
print(new_df.head())
# save the new_df to csv file
new_df.to_csv('splitted_jod.csv', index=False)

# upload to huggingface

from huggingface_hub.hf_api import HfFolder
HfFolder.save_token(hf_token)

from datasets import load_dataset
from datasets import Dataset
from datasets import Audio

audio_dataset = Dataset.from_dict({
  'audio': new_df['video_pth'],
  'text':new_df['text']
}).cast_column("audio", Audio())

data_set_name = input('Enter the name of the dataset: ')
audio_dataset.push_to_hub(data_set_name, use_auth_token=hf_token)
