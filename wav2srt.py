# -*- coding: utf-8 -*-

from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import os
import wave
import srt
import json
import datetime

#create output file
output = open(sys.argv[2],'a')

#vosk starts
SetLogLevel(0)

if not os.path.exists("model"):
	print ("Please download the model from https://github.com/alphacep/vosk-api/blob/master/doc/models.md and unpack as 'model' in the current folder.")
	exit (1)

wf = wave.open(sys.argv[1], "rb")
if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
	print ("Audio file must be WAV format mono PCM.")
	exit (1)

model = Model("model")
rec = KaldiRecognizer(model, wf.getframerate())

def transcribe():
	results = []
	subs = []
	while True:
		data = wf.readframes(4000)
		if len(data) == 0:
			break
		if rec.AcceptWaveform(data):
			results.append(rec.Result())
		else:
			print(rec.PartialResult())
	#results.append(rec.FinalResult())
	print(results)

	for i, res in enumerate(results):
		try:
			jres = json.loads(res)
			s = srt.Subtitle(index=i, 
						content=jres['text'], 
						start=datetime.timedelta(seconds=jres['result'][0]['start']), 
						end=datetime.timedelta(seconds=jres['result'][-1]['end']))
			subs.append(s)
		except KeyError:
			pass
	return subs

print(srt.compose(transcribe()),file=output)
