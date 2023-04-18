import speech_recognition as sr  
import logging   
from datetime import datetime
from kal_bot_ent import kalyantra  
from time import sleep
from kal_bot_ent import move_en

logging.basicConfig(filename='kalb.log', encoding='utf-8', level=logging.INFO,)


def get_text(wakeup=True,dur=7,interupt=False) -> str:
    
    with kalyantra.mic as source: 
        print('ignore above alsa unwanted logs \n') 
        kalyantra.srecg.adjust_for_ambient_noise(source,duration=1)
        
        if wakeup:
           kalyantra.awaiting_awake_cmd = True
           kalyantra.led_handler()
           audio = kalyantra.srecg.listen(source,phrase_time_limit=2)
        else: 
           print("listening what to do")   
         
           if kalyantra.move is not move_en.HALT.value and interupt:  
            kalyantra.speak('I am busy, want to abort tasks ?')
            sleep(0.5)   
           else: 
            kalyantra.speak(text='Yes') 
            sleep(0.2) 
           
           kalyantra.listening_wtd = True 
           kalyantra.led_handler()
           audio = kalyantra.srecg.listen(source,phrase_time_limit=dur)
           
        # recognize speech using Google Speech Recognition
        try: 
            rtxt =  kalyantra.srecg.recognize_google(audio)
            print("recog: " + rtxt) 
            return rtxt
        except sr.UnknownValueError:
            return 
        #     print("err: get_text(): could not understand audio")
        except sr.RequestError as e:
            logging.error(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} err at get_text(): {e}") 
            return 





