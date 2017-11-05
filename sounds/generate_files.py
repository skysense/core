from gtts import gTTS

tts = gTTS(text='Bitcoin bought.', lang='en', slow=True)
tts.save('sell.mp3')

tts = gTTS(text='Bitcoin sold.', lang='en', slow=True)
tts.save('buy.mp3')
