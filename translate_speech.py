import os
import time
import azure.cognitiveservices.speech as speechsdk

speech_key, service_region = os.environ['SPEECH_KEY'], os.environ['SPEECH_REGION']
from_language, to_languages = 'zh-CN', ['en','zh','ja','de']


def translate_speech_to_text():
    translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=speech_key, region=service_region)

    translation_config.speech_recognition_language = from_language
    #translation_config.add_target_language(to_language)
    for lang in to_languages:
        translation_config.add_target_language(lang)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    #add auto detect source language
    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(languages=["en-US", "zh-CN"])

    translation_recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=translation_config, 
            auto_detect_source_language_config=auto_detect_source_language_config,
            audio_config=audio_config)
    
    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        translation_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    translation_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    translation_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    translation_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    translation_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    translation_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))

    translation_recognizer.session_stopped.connect(stop_cb)
    translation_recognizer.canceled.connect(stop_cb)



    translation_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    translation_recognizer.stop_continuous_recognition()

translate_speech_to_text()