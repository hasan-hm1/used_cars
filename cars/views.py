from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Car, Comment
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import CarSerializer
import json
from django.contrib.auth.models import User

def home(request):
    if request.method == 'POST':
        cars_query_set = Car.objects.all()
        filtered_cars = list(cars_query_set)

        # brand filter
        brand = request.POST.get('brand')
        if brand:
            cars = filtered_cars
            filtered_cars = []
            for car in cars:
                if car.brand == brand:
                    filtered_cars.append(car)

        # model filter
        model = request.POST.get('model')
        if model and (model != 'all'):
            cars = filtered_cars
            filtered_cars = []
            for car in cars:
                if car.model == model:
                    filtered_cars.append(car)

        # price filter
        from_price = request.POST.get('from_price')
        to_price = request.POST.get('to_price')
        if from_price and to_price:
            from_price = int(from_price)
            to_price = int(to_price)
            if from_price > to_price:
                messages.warning(request, 'السعر غير صالح')
            else:
                cars = filtered_cars
                filtered_cars = []
                for car in cars:
                    if car.price >= from_price and car.price <= to_price:
                        filtered_cars.append(car)
        elif (from_price and not to_price) or (to_price and not from_price):
            messages.warning(
                request, 'من فضلك حدد السعر الأدنى و السعر الأعلى')

        # production year filter
        from_year = request.POST.get('from_year')
        to_year = request.POST.get('to_year')
        if from_year and to_year:
            from_year = int(from_year)
            to_year = int(to_year)
            if from_year > to_year:
                messages.warning(request, 'السنة غير صالحة')
            else:
                cars = filtered_cars
                filtered_cars = []
                for car in cars:
                    if car.production_year >= from_year and car.production_year <= to_year:
                        filtered_cars.append(car)
        elif (from_year and not to_year) or (to_year and not from_year):
            messages.warning(
                request, 'من فضلك حدد السنة الأقدم و السنة الأحدث')

        # kilometer filter
        from_kilometer = request.POST.get('from_kilometer')
        to_kilometer = request.POST.get('to_kilometer')
        if from_kilometer and to_kilometer:
            from_kilometer = int(from_kilometer)
            to_kilometer = int(to_kilometer)
            if from_kilometer > to_kilometer:
                messages.warning(request, 'الكيلومتر غير صالح')
            else:
                cars = filtered_cars
                filtered_cars = []
                for car in cars:
                    if car.kilometer >= from_kilometer and car.kilometer <= to_kilometer:
                        filtered_cars.append(car)
        elif (from_kilometer and not to_kilometer) or (to_kilometer and not from_kilometer):
            messages.warning(
                request, 'من فضلك حدد الكيلومتر الأدنى و الكيلومتر الأعلى')

        cars = filtered_cars
        if not cars:
            messages.warning(request, 'لا توجد نتائج تطابق البحث')
    else:
        cars = Car.objects.all().order_by('-date')
        # li = Car.objects.filter(brand='شيفروليه')
        # for car in li:
        #     loves = car.loves.all()
        #     for love in loves:
        #         messages.warning(request, love.username)

    context = {'active': 'home', 'title': 'الرئيسية', 'cars': cars}
    return render(request, 'cars/home.html', context)


def love_unlove(request):
    if request.method == 'POST':
        operation = request.POST.get('operation')
        id = request.POST.get('id')
        if operation == 'love':
            Car.objects.get(pk=id).loves.add(request.user)
        elif operation == 'unlove':
            Car.objects.get(pk=id).loves.remove(request.user)
    return JsonResponse({'loves': Car.objects.get(pk=id).loves.count()})


@login_required
def sell(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        production_year = request.POST.get('production_year')
        place = request.POST.get('place')
        kilometer = request.POST.get('kilometer')
        price = request.POST.get('price')
        engine_capacity = request.POST.get('engine_capacity')
        cylinders = request.POST.get('cylinders')
        transmission_type = request.POST.get('transmission_type')
        fuel = request.POST.get('fuel')
        body_shape = request.POST.get('body_shape')
        seats = request.POST.get('seats')
        technical_status = request.POST.get('technical_status')
        inner_color = request.POST.get('inner_color')
        outer_color = request.POST.get('outer_color')
        images = request.FILES.getlist('images')
        images_count = len(images)
        image0 = images[0]
        image1 = None
        image2 = None
        image3 = None
        image4 = None
        image5 = None
        image6 = None
        image7 = None
        image8 = None
        image9 = None

        if images_count > 1:
            image1 = images[1]
            if images_count > 2:
                image2 = images[2]
                if images_count > 3:
                    image3 = images[3]
                    if images_count > 4:
                        image4 = images[4]
                        if images_count > 5:
                            image5 = images[5]
                            if images_count > 6:
                                image6 = images[6]
                                if images_count > 7:
                                    image7 = images[7]
                                    if images_count > 8:
                                        image8 = images[8]
                                        if images_count > 9:
                                            image9 = images[9]

        extra_features_list = []

        index = 1
        while(index < 21):
            index_str = str(index)
            item = 'ef' + index_str
            ef = request.POST.get(item)
            if ef:
                extra_features_list.append(ef)
            index = index + 1

        extra_features = ','.join(extra_features_list)
        current_user = request.user
        car = Car(owner=current_user, brand=brand, model=model, production_year=production_year,
                  place=place, kilometer=kilometer, price=price, engine_capacity=engine_capacity,
                  cylinders=cylinders, transmission_type=transmission_type, fuel=fuel,
                  body_shape=body_shape, seats=seats, technical_status=technical_status,
                  inner_color=inner_color, outer_color=outer_color,
                  extra_features=extra_features,
                  image0=image0, image1=image1, image2=image2,
                  image3=image3, image4=image4, image5=image5,
                  image6=image6, image7=image7, image8=image8, image9=image9
                  )
        car.save()

        messages.success(request, 'تم عرض سيارتك بنجاح')
        return redirect('cars-home')

    return render(request, 'cars/sell_my_car.html', {'active': 'sell_my_car', 'title': 'اعرض سيارتي'})


def details(request, id):
    car = Car.objects.filter(id=id).first()

    if request.method == 'POST':
        if 'add' in request.POST:
            comment_content = request.POST.get('comment')
            comment = Comment(author=request.user,
                              content=comment_content, car=car)
            comment.save()
            messages.success(request, 'تم إضافة التعليق بنجاح')
        else:
            comment_id = request.POST.get('delete')
            Comment.objects.filter(id=comment_id).delete()
            messages.success(request, 'تم حذف التعليق بنجاح')
            car = Car.objects.filter(id=id).first()
    images = []
    extra_features = [x.strip() for x in car.extra_features.split(',')]

    if car.image1:
        images.append(car.image1)
    if car.image2:
        images.append(car.image2)
    if car.image3:
        images.append(car.image3)
    if car.image4:
        images.append(car.image4)
    if car.image5:
        images.append(car.image5)
    if car.image6:
        images.append(car.image6)
    if car.image7:
        images.append(car.image7)
    if car.image8:
        images.append(car.image8)
    if car.image9:
        images.append(car.image9)
    transmission = resolve_transmission(car.transmission_type)
    fuel = resolve_fuel(car.fuel)
    comments = car.comment_set.all()

    context = {'active': ' ', 'title': 'التفاصيل', 'car': car,
               'images': images, 'transmission': transmission,
               'fuel': fuel, 'extra_features': extra_features, 'comments': comments}
    return render(request, 'cars/details.html', context)


@login_required
def my_garage(request):
    if request.method == 'POST':
        id = request.POST.get('delete')
        Car.objects.filter(id=id).delete()
        messages.success(request, 'تم حذف السيارة بنجاح')
        cars = request.user.car_owner.all()
        context = {'active': 'my_garage', 'title': 'كراجي', 'cars': cars}
        return render(request, 'cars/my_garage.html', context)
    else:
        cars = request.user.car_owner.all()
        context = {'active': 'my_garage', 'title': 'كراجي', 'cars': cars}
        return render(request, 'cars/my_garage.html', context)


def about(request):

    return render(request, 'cars/about.html', {'active': 'about', 'title': 'حول الموقع'})


def password_reset(request):

    return render(request, 'cars/password_reset.html', {'active': '', 'title': 'تغيير كلمة المرور'})


@login_required
def price(request):
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        production_year = request.POST.get('production_year')
        technical_status = request.POST.get('technical_status')
        transmission_type = request.POST.get('transmission_type')
        kilometer = request.POST.get('kilometer')
        sun_roof = request.POST.get('sun_roof')
        abs_breakers = request.POST.get('abs_breakers')
        digital_condition = request.POST.get('digital_condition')
        steering_control = request.POST.get('steering_control')
        air_bags = request.POST.get('air_bags')
        chrome_wheel = request.POST.get('chrome_wheel')



        server_data = {
            'brand': brand,
            'model': model,
            'production_year': production_year,
            'technical_status': technical_status,
            'transmission_type': transmission_type,
            'kilometer': kilometer,
            'sun_roof': sun_roof,
            'abs_breakers': abs_breakers,
            'digital_condition': digital_condition,
            'steering_control': steering_control,
            'air_bags': air_bags,
            'chrome_wheel': chrome_wheel,
        }


        import joblib as jb
        import numpy as np

	
        gbr_model = jb.load('model.pkl')

        #calculate price
        arr = np.zeros(24)
        arr[8] = kilometer
        arr[9] = production_year
        if model == "4":
            arr[14] = 1
        elif model == "3":
            arr[13] = 1
        elif model == "2":
            arr[12] = 1
        elif model == "1":
            arr[11] = 1
        elif model == "0":
            arr[10] = 1

        if technical_status == "1":
            arr[20] = 1
        elif technical_status == "2":
            arr[21] = 1
        else:
            arr[19] = 1

        if abs_breakers == '1':
            arr[1] = 1
        else:
            arr[0] = 1

        if air_bags == '1':
            arr[3] = 1
        else:
            arr[2] = 1

        if chrome_wheel == '1':
            arr[5] = 1
        else:
            arr[4] = 1

        if digital_condition == '1':
            arr[7] = 1
        else:
            arr[6] = 1

        if steering_control == '1':
            arr[16] = 1
        else:
            arr[15] = 1

        if sun_roof == '1':
            arr[18] = 1
        else:
            arr[17] = 1

        if transmission_type == '1':
            arr[23] = 1
        else:
            arr[22] = 1


        arr = arr.astype(np.int)
        arr = arr.reshape(1, -1)
        price = gbr_model.predict(arr)
        price = int(price)

        return JsonResponse({'price': price,'min_price' : 'false','max_price' : 'false' ,'server_data': server_data})

    return render(request, 'cars/price.html', {'active': 'car-price', 'title': 'سعر سيارتي'})


    #     if int(kilometer) > 200000:
    #         kilometer = '200000'
    #     if int(kilometer) < 30000:
    #         kilometer = '30000'


    #     price = None
    #     max_price = None
    #     min_price = None
    #     min_max_active = False

    #     if sun_roof == '1' or abs_breakers == '1' or digital_condition == '1' or steering_control == '1' or air_bags == '1' or chrome_wheel == '1' :
    #         min_max_active = True
        
    #     if sun_roof == '1' and abs_breakers == '1' and digital_condition == '1' and steering_control == '1' and air_bags == '1' and chrome_wheel == '1' :
    #         min_max_active = False
    

    #     from sklearn.externals import joblib
    #     import numpy as np

    #     gbr_model = joblib.load('model.pkl')
    #     # model_columns =joblib.load('model_columns.pkl')

    #     # calculate price
    #     arr = np.zeros(11)
    #     arr[4] = kilometer
    #     arr[5] = production_year
    #     if model == "4":
    #         arr[6] = 4
    #     elif model == "3":
    #         arr[6] = 3
    #     elif model == "2":
    #         arr[6] = 2
    #     elif model == "1":
    #         arr[6] = 1
    #     elif model == "0":
    #         arr[6] = 0

    #     if technical_status == "1":
    #         arr[9] = 1
    #     elif technical_status == "2":
    #         arr[9] = 2
    #     else:
    #         arr[9] = 0

    #     if abs_breakers == '1':
    #         arr[0] = 1
    #     else:
    #         arr[0] = 0

    #     if air_bags == '1':
    #         arr[1] = 1
    #     else:
    #         arr[1] = 0

    #     if chrome_wheel == '1':
    #         arr[2] = 1
    #     else:
    #         arr[2] = 0

    #     if digital_condition == '1':
    #         arr[3] = 1
    #     else:
    #         arr[3] = 0

    #     if steering_control == '1':
    #         arr[7] = 1
    #     else:
    #         arr[7] = 0

    #     if sun_roof == '1':
    #         arr[8] = 1
    #     else:
    #         arr[8] = 0

    #     if transmission_type == '1':
    #         arr[10] = 1
    #     else:
    #         arr[10] = 0

    #     arr = arr.astype(np.int)
    #     arr = arr.reshape(1, -1)
    #     price = gbr_model.predict(arr)
    #     price = int(price)

        
    #     if min_max_active:
    #         # calculate min price
    #         arr = np.zeros(11)
    #         arr[4] = kilometer
    #         arr[5] = production_year
    #         if model == "4":
    #             arr[6] = 4
    #         elif model == "3":
    #             arr[6] = 3
    #         elif model == "2":
    #             arr[6] = 2
    #         elif model == "1":
    #             arr[6] = 1
    #         elif model == "0":
    #             arr[6] = 0

    #         if technical_status == "1":
    #             arr[9] = 1
    #         elif technical_status == "2":
    #             arr[9] = 2
    #         else:
    #             arr[9] = 0

            
    #         arr[0] = 0  # abs breakers
    #         arr[1] = 0 # air bags
    #         arr[2] = 0 # chrome wheel
    #         arr[3] = 0 # digital condition
    #         arr[7] = 0 # steering control
    #         arr[8] = 0 # sun roof
    #         if transmission_type == '1':
    #             arr[10] = 1
    #         else:
    #             arr[10] = 0

    #         arr = arr.astype(np.int)
    #         arr = arr.reshape(1, -1)
    #         min_price = gbr_model.predict(arr)
    #         min_price = int(min_price)

    #         # calculate max price
    #         arr = np.zeros(11)
    #         arr[4] = kilometer
    #         arr[5] = production_year
    #         if model == "4":
    #             arr[6] = 4
    #         elif model == "3":
    #             arr[6] = 3
    #         elif model == "2":
    #             arr[6] = 2
    #         elif model == "1":
    #             arr[6] = 1
    #         elif model == "0":
    #             arr[6] = 0

    #         if technical_status == "1":
    #             arr[9] = 1
    #         elif technical_status == "2":
    #             arr[9] = 2
    #         else:
    #             arr[9] = 0

            
    #         arr[0] = 1  # abs breakers
    #         arr[1] = 1 # air bags
    #         arr[2] = 1 # chrome wheel
    #         arr[3] = 1 # digital condition
    #         arr[7] = 1 # steering control
    #         arr[8] = 1 # sun roof
    #         if transmission_type == '1':
    #             arr[10] = 1
    #         else:
    #             arr[10] = 0

    #         arr = arr.astype(np.int)
    #         arr = arr.reshape(1, -1)
    #         max_price = gbr_model.predict(arr)
    #         max_price = int(max_price)

    #     if min_price:
    #         return JsonResponse({'price': price,'min_price' : min_price,'max_price' : max_price ,'server_data': server_data})
    #     else:
    #         return JsonResponse({'price': price,'min_price' : 'false','max_price' : 'false' ,'server_data': server_data})


        

    # return render(request, 'cars/price.html', {'active': 'car-price', 'title': 'سعر سيارتي'})


@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST.get('mobile')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        k = 0
        if username != request.user.username:
            user = User.objects.get(username=username)
            if user:
                messages.warning(request,'عذرا رقم الموبايل مرتبط بحساب آخر')
                return render(request, 'cars/profile.html', {'title': 'الملف الشخصي'})
            else:
                request.user.username = username
                k = k + 1
        if first_name != request.user.first_name:
            request.user.first_name = first_name
            k = k + 1
        if last_name != request.user.last_name:
            request.user.last_name = last_name
            k = k + 1
        if email != request.user.email:
            user = User.objects.filter(email=email)
            if user:
                messages.warning(request,'عذرا البريد الالكتروني مرتبط بحساب آخر')
                return render(request, 'cars/profile.html', {'title': 'الملف الشخصي'})
            else:
                request.user.email = email
                k = k + 1
        if image:
            request.user.profile.image = image
            k = k + 1
        if k > 0:
            request.user.save()
            messages.success(request, 'تم تعديل البيانات بنجاح')
        else:
            messages.warning(request, 'لم تقم بإجراء أية تعديلات')

    return render(request, 'cars/profile.html', {'title': 'الملف الشخصي'})


def resolve_fuel(fuel):
    if fuel == 0:
        return 'بنزين'
    else:
        return 'مازوت'


def resolve_transmission(transmission):
    if transmission == 0:
        return 'عادي'
    else:
        return 'أوتوماتيك'

# class CarsList(APIView):

#     def get(self,request):
#         cars = Car.objects.all()
#         serilaizer = CarSerializer(cars, many=True)
#         return Response(serilaizer.data)

#     def post(self,request):
#         pass
