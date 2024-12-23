from jamo import h2j,j2hcj
from fastapi import FastAPI, UploadFile, Response
from unicode import join_jamos
import pandas as pd
import re
from pydantic import BaseModel
import random
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from ggoodleDB import add_user,get_user,delete_all

#uvicorn ggoodle:app --reload --host=0.0.0.0 --port=8800

app=FastAPI()

today_num=351

async def change_word():
    global today_num
    today_num=random.randint(0,len(first_str_word)-1)
    await delete_all()
    print(today_num)

scheduler = AsyncIOScheduler()

#리눅스 서버 배포시 시간 -9시간 해줘야함
#scheduler.add_job(change_word, 'cron', hour=3, minute=0)
scheduler.add_job(change_word, 'cron', hour=12, minute=0)

scheduler.start()

class Users(BaseModel):
    name: str
    time : int
    count : int
    score : int
    isSolved : bool

class Item(BaseModel):
    word: str
    result: str 
    strList: list

class validWord(BaseModel):
    validWord: list

@app.get("/api/hello")
async def Hello():
    return "hello,world"

@app.post("/api/save/rank")
async def add_user_info(users: Users):
    return await add_user(users)

@app.get("/api/get/rank")
async def get_user_info():
    return await get_user()

@app.delete("/api/delete/rank")
async def delete_all_info():
    return await delete_all()

@app.post("/api/validation")
async def word_validation(word: validWord):
    valid_word=word.validWord
    isValid=False
    print(valid_word)
    for word in first_str_word:
        if(isValid):
            break
        isValid=True
        for j in range(0,6):
            if word[j]!=valid_word[j]:
                isValid=False
                break
    print(isValid)
    return isValid

@app.get("/api/change/number")
async def change_num():
    str_jamo_list=find_hangle_list()
    today_num=random.randint(0,len(str_jamo_list)-1)
    print(today_num)
    return ;
    
@app.get("/api/todayWord")
async def today_word():
    print(today_num)
    return first_str_word[today_num]

@app.get("/api/wordList")
async def getWordList():
    str_jamo_list=find_hangle_list()
    return str_jamo_list

@app.post("/api/recommend")
async def recommend(item: Item):
    # str_jamo_list=find_hangle_list()  #이거 없애기
    item_dict=item.dict()
    myText=item.word
    myResult=item.result
    myStrJamoList=item.strList
    resultWord=recommend_word_ggodle(myText,myResult,myStrJamoList) 
    #단어 합체하는 코드 작성 필요
    resultJoinWord=joinWord(resultWord)
    item_dict.update({"resultWord" : resultWord})
    item_dict.update({"resultJoinWord": resultJoinWord })
    #단어 합체된거 업데이트 코드
    return item_dict


def joinWord(Str_List):
    join_list=[]
    for i in range(len(Str_List)):
        join_list.append(join_jamos(Str_List[i]))
    print(join_list)
    return join_list
    
def recommend_word_ggodle(my_text,result_text,str_jamo_list):
    result=[]
    st_word=[]
    str_word_list=[]
    for i in range(0,6):
        result.append(result_text[i])
    my_jamoText=jamo_split(my_text)
    str_jamo_list=recommend_text(my_jamoText,result,str_jamo_list)
    for i in range(len(str_jamo_list)):
        str_word_list.append(join_jamos(str_jamo_list[i]))
    for i in range(len(str_jamo_list)):
        st_word.append(jamo_split(str_word_list[i]))
    print(st_word)
    return str_jamo_list

def find_hangle_list():
    test_list=[]
    excel_data=pd.read_excel('./한국어 학습용 어휘 목록.xls',usecols=[1]) #현재 터미널 위치에 따라 변경
    data=excel_data['단어'].to_list()
    for i in range(len(data)):
        data[i]=re.sub(r'\d','',data[i])
        str_jamo=jamo_split(data[i])
        if(len(str_jamo)==6):
            test_list.append(str_jamo)
    return test_list

def jamo_split(word):
    jamo = j2hcj(h2j(word))
    dic = {'ㅐ':'ㅏㅣ','ㅒ':'ㅑㅣ','ㅔ':'ㅓㅣ','ㅖ':'ㅕㅣ',
       'ㅘ':'ㅗㅏ','ㅙ':'ㅗㅐ','ㅚ':'ㅗㅣ','ㅝ':'ㅜㅓ',
       'ㅞ':'ㅜㅔ','ㅟ':'ㅜㅣ','ㅢ':'ㅡㅣ',
       'ㄳ' : 'ㄱㅅ', 'ㄵ' : 'ㄴㅈ', 'ㄶ' : 'ㄴㅎ','ㄺ' : 'ㄹㄱ',
       'ㄻ' : 'ㄹㅁ', 'ㄼ' : 'ㄹㅂ', 'ㄽ' : 'ㄹㅅ', 'ㄾ' : 'ㄹㅌ', 
       'ㄿ' : 'ㄹㅍ', 'ㅀ' : 'ㄹㅎ', 'ㅄ' : 'ㅂㅅ', 'ㄲ' : 'ㄱㄱ','ㅆ'  : 'ㅅㅅ'}
    for i in jamo:
        if i in dic.keys():
            jamo = jamo.replace(i,dic[i])
    return jamo

def recommend_text(my_jamoText,result,jamo_str):
    result_set=[]
    recommend_set=[]
    recommend_word=[]
    for text in jamo_str:
        Test(my_jamoText,text,result_set)
    
    for i in range(len(result_set)):
        if(result==result_set[i]):
            recommend_set.append(jamo_str[i])
    return recommend_set

def Test(my_jamoText,target_jamoText,result_set):
    temp_my=[]
    temp_answer=[]
    for i in range(len(my_jamoText)):
        temp_my.append(my_jamoText[i])
        temp_answer.append(target_jamoText[i])
    result=[0 for _ in range(6)]
    for i in range(len(my_jamoText)):
        if(temp_my[i]=="X"):
            continue
        for k in range(len(my_jamoText)):
            if(temp_my[k]==temp_answer[k]):
                temp_my[k]="X"
                temp_answer[k]="N"
                result[k] = 'g'
                continue
        for j in range(len(my_jamoText)):
            if(temp_my[j]=="X"):
                break
            if(temp_my[i]==temp_answer[j]):
                temp_my[i]="X"
                temp_answer[j]="N"
                result[i] = 'y'
                break
            elif(j==5):
                result[i] = 'o'
    result_set.append(result)
    return

first_str_word = find_hangle_list()
print(first_str_word[len(first_str_word)-1])
print(len(first_str_word))

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
# str_jamo_list=find_hangle_list()

# while(True):
#     result=[]
#     result_text=input()
#     my_text=input()
#     for i in range(0,6):
#         result.append(result_text[i])
#     my_jamoText=jamo_split(my_text)
#     str_jamo_list=recommend_text(my_jamoText,result,str_jamo_list)


# while(True):
#     my_text=input()
#     result_text=input()
#     str_jamo_list=recommend_word_ggodle(my_text,result_text,str_jamo_list)

#테스트
# result_set=[]
# Test(jamo_split("김창"),jamo_split("각각"),result_set)
# print(result_set)
