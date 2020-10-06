#!/usr/bin/venv python3
# -*- coding: utf-8 -*-
"""
Created on Tusday Sep 29 10:54:42 2020

@author: Najmi Imad
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import speech_recognition as sr
import os
from time import sleep
import random
import requests
import pydub



driver = webdriver.Chrome('../chromedriver')

def delay(min=3, max=5):
	sleep(random.randint(min,max))

url = "https://www.google.com/recaptcha/api2/demo"
driver.get(url)

delay()

wait = WebDriverWait(driver, 10)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()

#switch to recaptcha audio control frame
driver.switch_to.default_content()
xpath= "/html/body/div[2]/div[4]"
frames=driver.find_element_by_xpath(xpath).find_elements_by_tag_name("iframe")

driver.switch_to.frame(frames[0])
delay()


driver.find_element_by_id("recaptcha-audio-button").click()
sleep(1)
#switch to recaptcha audio challenge frame
driver.switch_to.default_content()
frames= driver.find_elements_by_tag_name("iframe")
driver.switch_to.frame(frames[-1])
delay()

src = driver.find_element_by_id('audio-source').get_attribute('src')

r = requests.get(src, allow_redirects=True)

with open('sample.mp3', 'wb') as f:
	f.write(r.content)

sound = pydub.AudioSegment.from_mp3("sample.mp3")

sound.export("sample.wav", format="wav")

sample_audio = sr.AudioFile("sample.wav")

r= sr.Recognizer()

with sample_audio as source:
    audio = r.record(source)

#translate audio to text with google voice recognition
key=r.recognize_google(audio)

print("[INFO] Recaptcha Passcode: %s"%key)

driver.find_element_by_css_selector("input#audio-response").send_keys(key)
delay()

driver.find_element_by_css_selector('button#recaptcha-verify-button').click()

driver.switch_to.default_content()


 