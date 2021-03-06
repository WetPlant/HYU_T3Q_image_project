# -*- coding: utf-8 -*-
import pytesseract
import PIL
import pandas as pd
import re

capture_path = "C:/Users/Elite/Desktop/2차/"
all_words = 0
counts = 0
fail = []
han = {}

for i in range(1,84):
    #box 불러오기
    df = pd.read_csv(capture_path + 'second (' + str(i) +').box', sep=' ', header=None, engine='python', encoding='utf-8')
    box_data = df[0].tolist()
    print(df)
    print(box_data)

    #img파일
    img_path = capture_path + "second (" + str(i) + ").jpg"
    fp = open(img_path, "rb")
    img = PIL.Image.open(fp)
    #config setting
    config= ('-l vkor+52font --oem0 --psm6')
    #ocr_result
    txt = pytesseract.image_to_string(img, config= config)
    all_words += 7
    txt = txt.replace(' ', '')

    if bool(re.search('\d{2}\D\d{4}', txt)):
        txt = re.search('\d{2}\D\d{4}', txt).group()
        print("OCR 2차 :", txt)
    elif bool(re.search('\d{2}\D', txt)) and bool(re.search('\d{4}', txt)):
        txt = re.search('\d{2}\D', txt).group() + re.search('\d{4}', txt).group()
        print("OCR 2차_2 :", txt)

    try:
        for index in range(len(box_data)):
            if str(box_data[index]) != txt[index]:
                counts += 1
                fail.append(str(i))
                print('실패 : ' + str(i))
    except IndexError:
        txt = txt + 'a'
    #make_box
    #txt = pytesseract.image_to_boxes(img, lang="vikor2")
    print("ocr 결과 : " + txt)
    print('index' + str(i))
    f = open(capture_path + 'font_testkor' + '.txt', 'a')
    f.write(txt+ '\n')



    #한글 단어 개수 세기
    for idx in box_data:
        if idx in han:
            han[idx] = han[idx] + 1
        else:
            han[idx] = 1

print('총 단어의 수 :' + str(all_words))
print('틀린 단어 수 : ' + str(counts))
print('인식율 : ' + str(100 -(counts/all_words*100)))
for fa in fail:
    print("틀린 번호판 :" + fa)

print('문자별 개수 : ' + str(han))

f.close()