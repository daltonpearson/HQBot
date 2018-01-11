import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import glob
import os
import time
from googleapiclient.discovery import build

def google_results_count(query):
    service = build("customsearch", "v1",
                    developerKey="developerKey"
                    )

    result = service.cse().list(
            q=query,
            cx='searchEngineId',
            num=1
        ).execute()

    return result["searchInformation"]["totalResults"]

path="*.png"

def img_rec(filename):
	img = Image.open(filename)
	question = img.crop((30, 130, 700, 500))#200
	answer1 = img.crop((80, 520, 650, 615))
	answer2 = img.crop((80, 650, 650, 740))
	answer3 = img.crop((80, 775, 650, 880))

	answer=[]
	result=[]

	question = pytesseract.image_to_string(question).replace('\n', ' ')
	answer.append(pytesseract.image_to_string(answer1))
	answer.append(pytesseract.image_to_string(answer2))
	answer.append(pytesseract.image_to_string(answer3))
	
	invert=0

	if 'NOT' in question.split():
		invert=1

	question = question.replace('\n', ' ')
	
	question = question.replace('NOT', '')
	
	for count in range(3):
		search = question+" \""+answer[count]+"\""
		start_time = time.time()
		result.append(float(google_results_count(search).encode("utf-8")))
		#result[count]=(result[count])/float(google_results_count(answer[count]).encode("utf-8"))
		print(time.time() - start_time)
		print result
	if invert==0:
		result[result.index(max(result))]='*BEST*'+str(result[result.index(max(result))])
		result[result.index(min(result))]='**WORST**'+str(result[result.index(min(result))])
	else:
		result[result.index(max(result))]='**WORST**'+str(result[result.index(max(result))])
		result[result.index(min(result))]='*BEST*'+str(result[result.index(min(result))])
	print("\nQuestion: "+question.replace('\n', ' ')+"\nAnswer 1: "+str(result[0])+" "+answer[0]+"\t"+"\nAnswer 2: "+str(result[1])+" "+answer[1]+"\t"+"\nAnswer 3: "+str(result[2])+" "+answer[2])

while(0==0):
	images=glob.glob(path)	
	if len(images)>=1:
		start_time = time.time()
		for filename in glob.glob(path):	
			img_rec(filename)
		print filename
		print(time.time() - start_time)
		os.remove(filename)
	time.sleep(0.1)
