import pyaudio
import wave
import os


def record_to_wav() -> str:
    chunk = 1024     # record in chunks od 1024 samples
    sample_format = pyaudio.paInt16     # 16 bits per sample
    channels = 2
    fs = 44100  # samples per second
    seconds = 6

    list_files = os.listdir("APP/voice/record_voice/data_wav")
    last_file = list_files[len(list_files)-1]
    last_file = last_file.split('.')
    n = int(last_file[0]) + 1

    filename = "APP/voice/record_voice/data_wav/{0}.wav".format(n)

    p = pyaudio.PyAudio()   # create an interface to PortAudio
    print("Rec")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []     # initialize array to store frames

    # store data in chunks
    for i in range(0, int(fs/chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # stop and close the stream
    stream.stop_stream()
    stream.close()
    # terminate the PortAudio interface
    p.terminate()

    print("Finished")

    # save to wav
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

    return wav_to_spectogram(n)
