import time
import json
import os
import azure.cognitiveservices.speech as speechsdk


speech_key, service_region = os.environ['SPEECH_KEY'], os.environ['SPEECH_REGION']
weatherfilename="en-us_zh-cn.wav"

# Currently the v2 endpoint is required. In a future SDK release you won't need to set it. 
endpoint_string = "wss://{}.stt.speech.microsoft.com/speech/universal/v2".format(service_region)
speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=endpoint_string)
# audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Set the LanguageIdMode (Optional; Either Continuous or AtStart are accepted; Default AtStart)
speech_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceConnection_LanguageIdMode, value='Continuous')

auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
    languages=["en-US", "zh-CN"])

speech_recognizer = speechsdk.SpeechRecognizer( 
    speech_config=speech_config, 
    auto_detect_source_language_config=auto_detect_source_language_config,
    audio_config=audio_config)

done = False

def stop_cb(evt):
    """callback that signals to stop continuous recognition upon receiving an event `evt`"""
    print('CLOSING on {}'.format(evt))
    #nonlocal done
    done = True

# Connect callbacks to the events fired by the speech recognizer
speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
# stop continuous recognition on either session stopped or canceled events
speech_recognizer.session_stopped.connect(stop_cb)
speech_recognizer.canceled.connect(stop_cb)

# Start continuous speech recognition
speech_recognizer.start_continuous_recognition()
while not done:
    time.sleep(.5)

speech_recognizer.stop_continuous_recognition()