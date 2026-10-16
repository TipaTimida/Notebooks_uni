import wave
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

file_path = '/home/gea/Documents/Notebooks/School/Lab/First_semester_home/My recording 21.wav'
# Apertura del file audio, vedi https://docs.python.org/3/library/wave.html
stream = wave.open(file_path)
signal = np.frombuffer(stream.readframes(stream.getnframes()), dtype=np.int16)
# Importante: se il file originale e‘ stereo dobbiamo prendere solo uno dei canali.
if stream.getnchannels() == 2:
    signal = signal[::2]
# L’unica cosa che ci manca e‘ l’array dei tempi corrispondenti ai singoli campioni.
t = np.arange(len(signal)) / stream.getframerate()

# A questo punto siamo pronti per analizzare il tracciato audio. Una volta
# messi i dati in un grafico di matplotlib possiamo utilizzare lo strumento
# zoom ed il mouse per misurare i tempi di rimbalzo della pallina.
plt.figure('Rimbalzi pallina')
plt.plot(t, signal)
plt.xlabel('Tempo [s]')
plt.savefig('audio_rimbalzi.png')
plt.show()

