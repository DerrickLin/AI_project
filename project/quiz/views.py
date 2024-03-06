from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .models import CustomUser, product, Category
from .forms import SignUpForm
from django.views.generic import  CreateView
from .forms import RegisterForm
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import UpdateUserForm
from roboflow import Roboflow
from PIL import Image
import os
import cv2
#from .models import UserProfile

from django.views import generic
from django.contrib import auth
from django.contrib.auth.models import  BaseUserManager
from django.views.decorators.csrf import csrf_protect


#import the model deploied on Roboflow
rf = Roboflow(api_key="WBwLaRxuckwQFXwFCETu")
project = rf.workspace().project("item_detection-fucyd")
model = project.version("2").model



class RegisterManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model( email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user( email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your views here.


class SignUpView(CreateView):
    form_class = RegisterForm  # 使用你的 RegisterForm

    success_url = reverse_lazy('login')
    template_name = 'sign_up.html'
    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)  # 自动登录新创建的用户
        return response
    
    
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User registered successfully.")
            return redirect('home')
        else:
            print("Form errors:", form.errors)
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})
#    return render(request, 'sign_up.html')


def check_user_existence(username):
    try:
        user = CustomUser.objects.get(username=username)
        print(f"User with username {username} exists.")
        return user
    except CustomUser.DoesNotExist:
        print(f"User with username {username} does not exist.")
        return None


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(f"Trying to authenticate with username: {username} and password: {password}")

        try:
            user = CustomUser.objects.get(username=username, password=password)
        except CustomUser.DoesNotExist:
            # Handle login failure with messages
            messages.error(request, '無此帳號')
            return render(request, 'login.html')

        if user is not None and user.is_active:
            auth_login(request, user)
            print("Redirecting to main_page")
            return redirect('home')
        else:
            # Handle login failure with messages
            messages.error(request, '帳號密碼錯誤')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

    
def main_page(request):
    return render(request, 'main_page.html')


def log_out(request):
    auth.logout(request)
    return render(request, 'log_out.html')


def remove_duplicates(lst):
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result



# 這邊之後要改成將框選照片存到model中，把暫存在assets中的圖片刪掉
def home(request):
    if request.method == "POST":		#如果是以POST方式才處理
        img = request.FILES.get('myvalue')
        img_1 = Image.open(img)
        img_1 = img_1.transpose(Image.ROTATE_270)
        img_1.save(os.path.join('./static/assets', 'test.jpg'))

		
		# detection
        predictions_dict = model.predict('./static/assets/test.jpg', confidence=40, overlap=30).json()
        pred_list = predictions_dict['predictions']
		
        # add class to results
        result = []
        item_amount = []
        noodle_amount = 0
        ooha_amount = 0
        hi_chew_amount = 0
        cookie_amount = 0
        tea_amount = 0
    
        
        for prediction in pred_list:
            result.append(prediction['class'])
            print("Class:", result[-1])
            if prediction['class'] == "noodle":
                noodle_amount += 1
            elif prediction['class'] == "OOha":
                ooha_amount += 1
            elif prediction['class'] == "hi_chew":
                hi_chew_amount += 1
            elif prediction['class'] == "cookie":
                cookie_amount += 1
            elif prediction['class'] == "black_tea":
                tea_amount += 1
                
        #排序商品(不重複)       
        unique_list = remove_duplicates(result)
        
        for i in unique_list:
            if i == "noodle":
                item_amount.append(noodle_amount)
            elif i == "OOha":
                item_amount.append(ooha_amount)
            elif i == "hi_chew":
                item_amount.append(hi_chew_amount)
            elif i == "cookie":
                item_amount.append(cookie_amount)
            elif i == "black_tea":
                item_amount.append(tea_amount)      

        
        #合併成dict  
        merged_Item_info = dict(zip(unique_list, item_amount))
        
        
		# draw bounding-box
        image = cv2.imread('./static/assets/test.jpg')
    
        for i in range(len(result)):
    		# print(f"{predictions_dict['predictions'][i]['x']}, {predictions_dict['predictions'][i]['y']}")
            image = cv2.rectangle(image, (int(pred_list[i]['x'] - (pred_list[i]['width'] / 2)), int(pred_list[i]['y'] - (pred_list[i]['height'] / 2))), (int(pred_list[i]['x'] + (pred_list[i]['width'] / 2)), int(pred_list[i]['y'] + (pred_list[i]['height'] / 2))), (0,0,255), 8)
        cv2.imwrite('./static/assets/result.jpg', image)
        
        # no class
        if len(result) == 0:
            detect_finish = "未辨識出商品"
            #合併成dict  
        elif len(result) != 0:
            detect_finish = "辨識已完成"
            

    return render(request, "home.html", locals())



def about(request):
    return render(request,'about.html',{})


def update_user(request, id=None):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            
            # 更新用戶資料
            user = CustomUser.objects.get(id=id)
            user.username = username
            user.email = email
            user.password = password
            user.phone = phone
            user.save()
            
            # 确保更新成功后重定向到正确的页面
            return redirect('home')
    else:
        form = UpdateUserForm()
    return render(request, 'update_user.html', {'form': form})


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login')  # 或是你想要的登入成功後跳轉的 URL
    template_name = 'registration_form.html'


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            print("User registered and logged in successfully.")
            return redirect('main_page')
        else:
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    print(f"{field}: {error}")
        
    else:
        form = SignUpForm()
    return render(request, 'sign_up.html', {'form': form})


def shop(request):
    products = product.objects.all()
    sort_by = request.GET.get('sort_by')

    if sort_by == 'price_asc':
        products = products.order_by('pCost')
    elif sort_by == 'price_desc':
        products = products.order_by('-pCost')
    
    return render(request, 'shop.html', locals())

def noodles(request):
    noodles_category = Category.objects.get(name="泡麵")
    products = product.objects.filter(pCategory=noodles_category.id)
    sort_by = request.GET.get('sort_by')

    if sort_by == 'price_asc':
        products = products.order_by('pCost')
    elif sort_by == 'price_desc':
        products = products.order_by('-pCost')
    
    return render(request, 'shop.html', locals())

def candy(request):
    candy_category = Category.objects.get(name="糖果")
    products = product.objects.filter(pCategory=candy_category.id)
    sort_by = request.GET.get('sort_by')

    if sort_by == 'price_asc':
        products = products.order_by('pCost')
    elif sort_by == 'price_desc':
        products = products.order_by('-pCost')
    
    return render(request, 'shop.html', locals())

def biscuits(request):
    biscuits_category = Category.objects.get(name="餅乾")
    products = product.objects.filter(pCategory=biscuits_category.id)
    sort_by = request.GET.get('sort_by')

    if sort_by == 'price_asc':
        products = products.order_by('pCost')
    elif sort_by == 'price_desc':
        products = products.order_by('-pCost')
    
    return render(request, 'shop.html', locals())

def drinks(request):
    drinks_category = Category.objects.get(name="飲料")
    products = product.objects.filter(pCategory=drinks_category.id)
    sort_by = request.GET.get('sort_by')

    if sort_by == 'price_asc':
        products = products.order_by('pCost')
    elif sort_by == 'price_desc':
        products = products.order_by('-pCost')
    
    return render(request, 'shop.html', locals())



    
# def register_create_view(request):
#     form = RegisterForm(request.POST or None)
#     if form.is_valid():
#         Register.objects.create(**form.cleaned_data)
#         form = RegisterForm
#     context = {
#         'form':form
#     }
#     return render(request, 'register_create.html', context)