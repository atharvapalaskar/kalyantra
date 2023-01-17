import speech_recognition as sr  
import logging   
from datetime import datetime
from kal_bot_ent import kalyantra  
from time import sleep

logging.basicConfig(filename='kalb.log', encoding='utf-8', level=logging.INFO,)


def get_text(wakeup=True) -> str:
    with kalyantra.mic as source: 
        print('ignore above alsa unwanted logs \n') 
        kalyantra.srecg.adjust_for_ambient_noise(source,duration=1)
        
        if wakeup:
           audio =  kalyantra.srecg.listen(source,phrase_time_limit=2)
        else: 
           print("listening what to do")  
           kalyantra.speak(text='Yes') 
           sleep(0.2) 
           audio =  kalyantra.srecg.listen(source,phrase_time_limit=6)

        # recognize speech using Google Speech Recognition
        try:
            rtxt =  kalyantra.srecg.recognize_google(audio)
            print("recog: " + rtxt) 
            return rtxt
        except sr.UnknownValueError:
            pass
        #     print("err: get_text(): could not understand audio")
        except sr.RequestError as e:
            logging.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} err at get_text(): {e}") 





