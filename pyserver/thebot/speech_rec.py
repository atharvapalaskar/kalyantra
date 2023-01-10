import speech_recognition as sr  
 
recg = sr.Recognizer() 

def get_text(wakeup=True) -> str:
    with sr.Microphone() as source: 
        print('ignore above alsa unwanted logs \n') 
        recg.adjust_for_ambient_noise(source,duration=1)  
        print("say 'ok yantra' or 'do something'")
        if wakeup:
           audio =  recg.listen(source,phrase_time_limit=2)
        else: 
           audio =  recg.listen(source,phrase_time_limit=5)

        # recognize speech using Google Speech Recognition
        try:
            rtxt =  recg.recognize_google(audio)
            print("recog: " + rtxt) 
            return rtxt
        except sr.UnknownValueError:
            print("err: get_text(): could not understand audio")
        except sr.RequestError as e:
            print(f"err get_text(): {e}")





