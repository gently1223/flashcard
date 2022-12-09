from django.shortcuts import render
from .models import user_info, question_book, setting
from .serializers import UserInfoSerializer, QuestionBookSerializer, SettingSerializer
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser 
from rest_framework import status
import MySQLdb
import ast
from pathlib import Path
import os, re, random, glob
from PIL import Image
# Create your views here.
def vue_test(request):
    return render(request, 'cardapp/vue-test.html')
def vue_test1(request):
    return render(request, 'cardapp/vue-test.html')

@api_view(['GET', 'POST', 'DELETE'])
def UserInfoList(request):
    if request.method == 'GET':
        users = user_info.objects.all()
        
        user_id = request.GET.get('user_id', None)
        password = request.GET.get('password', None)
        if user_id is not None and password is not None:
            users = users.filter(user_id=user_id, password=password)
        
        user_serializer = UserInfoSerializer(users, many=True)
        return JsonResponse(user_serializer.data, safe=False) 
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        print(user_data)
        userinfo_serializer = UserInfoSerializer(data=user_data)
        if userinfo_serializer.is_valid():
            temp_setting = {
                "user_id": user_data['user_id'],
                "data": {"plan": {"unit": "日", "start": "2022-05-30", "friday": 1, "monday": 1, "number": 2, "sunday": 1, "tuesday": 1, "saturday": 1, "thursday": 1, "wednesday": 1}, "period": {"easy": 604800, "miss": 14400, "easy_num": 2, "miss_num": 4, "standard": 86400, "difficult": 3600, "easy_unit": "weeks", "miss_unit": "hours", "standard_num": 2, "difficult_num": 1, "standard_unit": "days", "difficult_unit": "hours"}, "reward": {"point": 47}}
            }
            setting_serializer = SettingSerializer(data = temp_setting)
            if setting_serializer.is_valid():
                setting_serializer.save()
            userinfo_serializer.save()
            return JsonResponse(userinfo_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(userinfo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def QuestionBookList(request):
    if request.method == 'GET':
        books = question_book.objects.all()        
        book_serializer = QuestionBookSerializer(books, many=True)
        return JsonResponse(book_serializer.data, safe=False) 

@api_view(['GET', 'POST', 'DELETE'])
def SettingList(request):
    if request.method == 'GET':
        settings = setting.objects.all()
        user_id = request.GET.get('user_id', None)
        if user_id is not None:
            settings = settings.filter(user_id=user_id)
        
        setting_serializer = SettingSerializer(settings, many=True)
        return JsonResponse(setting_serializer.data, safe=False) 

@api_view(['GET', 'PUT', 'DELETE'])
def SettingDetail(request, pk):
    settings = setting.objects.get(pk=pk)
    if request.method == 'GET':
        setting_serializer = SettingSerializer(settings) 
        return JsonResponse(setting_serializer.data)
    elif request.method == 'PUT':
        setting_data = JSONParser().parse(request) 
        setting_serializer = SettingSerializer(settings, data=setting_data) 
        if setting_serializer.is_valid(): 
            setting_serializer.save() 
            return JsonResponse(setting_serializer.data) 
        return JsonResponse(setting_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@staticmethod
def fromListToDict(keys, list):
    outList = []
    for data in list:
        outList.append(dict(zip(keys, data)))
    return outList
@staticmethod
def sortingFilePathList(file_path_list):
    if len(file_path_list) == 0:
        return []
    file_name_list = [os.path.basename(file_path) for file_path in file_path_list]
    #for debug (re.searchの動作確認。ファイル名から0-9にピリオドが続くものを見つけて、0-9のGroupを取り出す)
    # file_name_list_sorted = Misc.sort_filenames(file_name_list)
    # for file in file_name_list:
    #     tmp = re.search(r"([0-9]+)\.", file).group(1)
    #     print (tmp1)
    #拡張子のピリオドの直前の数字で並び替える
    file_name_list_sorted = sorted(file_name_list, key=lambda x:int((re.search(r"([0-9]+)\.", x)).group(1)))
    # file_name_list_sorted = sorted(file_name_list, key=lambda x:int((re.search(r"[0-9]+", x)).group(0)))
    dir_path = os.path.dirname(file_path_list[0])
    new_file_path_list = [os.path.join(dir_path, file) for file in file_name_list_sorted]
    return new_file_path_list
@staticmethod
def getFilePathList(folder, extension):
    pathList = []
    for x in glob.glob(f'{folder}/*.{extension}'):
        pathList.append(Path(x))
    pathList = sortingFilePathList(pathList)
    return pathList
@api_view(['GET', 'POST', 'DELETE'])
def getMaxCount(request):
    if request.method == 'GET':
        book_uuid = request.GET.get('book_uuid', None)
        pageList = (request.GET.get('pageList', None))
        pageList = ast.literal_eval(pageList)
        if len(pageList) > 0:
            sql = 'select max(r.count) from cardapp_records as r \
                    left join cardapp_questions_areas as q on r.question_area_uuid = q.area_uuid \
                    where r.book_uuid = "{0}" and q.page_number in ({1});'.format(book_uuid, ', '.join('{}'.format(pageList[i]) for i in range(len(pageList))))
        else:
            sql = 'select max(count) from cardapp_records where book_uuid = "{0}"'.format(book_uuid)
        print(sql)
        conn = MySQLdb.connect(
                    host='gotit.smagai.com',
                    user='usersql',
                    passwd='20220622',
                    db='kioku_db',
                    charset='utf8')        
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if len(data) == 0:
            studyCount = data[0]
        else:
            studyCount = 0
        if len(pageList) > 0:
            sql = 'select q.area_uuid, q.area_number,  q.x, q.y, q.width, q.height, q.book_uuid, q.page_number, qb.image_folder, \
                       a.area_uuid, a.area_number,  a.x, a.y, a.width, a.height, a.book_uuid, a.page_number, ab.image_folder,  \
                       r.count,     date_format(r.datetime,"%Y-%m-%d %H:%i:%s.%f"), r.result, r.level \
                        from cardapp_questions_areas as q \
                        left join cardapp_cardapp_answers_areas as a on q.area_uuid = a.linked_uuid \
                        left join cardapp_question_book as qb on q.book_uuid = qb.uuid \
                        left join cardapp_cardapp_answers_book as ab on a.book_uuid = ab.uuid \
                        left join records_latest_date as r on q.area_uuid = r.question_area_uuid and r.count ={0} \
                        where q.book_uuid = "{1}" and q.page_number in ({2}) \
                        order by cast(q.page_number as signed) asc, cast(q.area_number as signed) asc;'.format(studyCount, book_uuid, ', '.join('{}'.format(pageList[i]) for i in range(len(pageList))))
        else:
            sql = 'select q.area_uuid, q.area_number,  q.x, q.y, q.width, q.height, q.book_uuid, q.page_number, qb.image_folder, \
                       a.area_uuid, a.area_number,  a.x, a.y, a.width, a.height, a.book_uuid, a.page_number, ab.image_folder,  \
                       r.count,     date_format(r.datetime,"%Y-%m-%d %H:%i:%s.%f"), r.result, r.level \
                        from questions_areas as q \
                        left join answers_areas as a on q.area_uuid = a.linked_uuid \
                        left join questions_book as qb on q.book_uuid = qb.uuid \
                        left join answers_book as ab on a.book_uuid = ab.uuid \
                        left join records_latest_date as r on q.area_uuid = r.question_area_uuid and r.count ={0} \
                        where q.book_uuid = "{1}" \
                        order by cast(q.page_number as signed) asc, cast(q.area_number as signed) asc;'.format(studyCount, book_uuid)
        cursor.execute(sql)
        areas = cursor.fetchall()
        cursor.close()
        conn.close()
        label = ['q.area_uuid', 'q.area_number',  'q.x', 'q.y', 'q.width', 'q.height', 'q.book_uuid', 'q.page_number', 'q.image_folder', \
                'a.area_uuid', 'a.area_number',  'a.x', 'a.y', 'a.width', 'a.height', 'a.book_uuid', 'a.page_number', 'a.image_folder', \
                'r.count',     'r.datetime',     'r.result', 'r.level']
        areas_dict = fromListToDict(label, areas)
        cards = areas_dict
        imageFolder = [".\\vueapp\\src\\assets\\img"+card['q.image_folder'] for card in cards if card['q.image_folder'] is not None]
        pagesQuestions = getFilePathList(imageFolder[0], 'jpg')
        imageFolder = [".\\vueapp\\src\\assets\\img"+card['a.image_folder'] for card in cards if card['a.image_folder'] is not None]
        pagesAnswers = getFilePathList(imageFolder[0], 'jpg')
        print(pagesQuestions)   
        print(pagesAnswers)
        return render(request, 'cardapp/vue-test.html')