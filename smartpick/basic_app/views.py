from django.shortcuts import render
from basic_app.forms import UserForm
from .models import Compare

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from django.views.generic import TemplateView,CreateView

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'registration.html',
                          {'user_form':user_form,
                           'registered':registered})



def user_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                context["error"] = "ACCOUNT NOT ACTIVE"
                return render(request,'login.html',context)
        else:
            context["error"] = "Invalid Credentials!"
            return render(request,'login.html',context)
    else:
        return render(request,'login.html',context)


class home(TemplateView):
    template_name = 'home.html'

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import requests


class products(object):
    def __init__(self,i_id,name,img,price,discount,link):
        self.i_id = i_id
        self.name = name
        self.img = img
        self.price = price
        self.discount = discount
        self.link = link

class detail(object):
    def __init__(self,name,img,price,spec_item,spec_value):
        self.name = name
        self.img = img
        self.price = price
        self.spec_item = spec_item
        self.spec_value = spec_value

# def abc_e(arg):
#     p = []
#     a = arg.split()
#     my_a_url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw='
#     for value in a:
#         my_a_url += value + '+'
#     my_a_url = my_a_url[:-1]
#     my_a_url +='&_sacat=0'
#     url = my_a_url
#     html = uReq(url)
#     a_page_soup = soup(html, 'html.parser')
#     a_containers = a_page_soup.findAll("div",{"class":"clearfix"})
#     i = 0
#     for u in a_containers:
#         i+=1
#         if i>=7:
#             try:
#                 name = u.img['alt']
#                 img = u.img['src']
#                 link = u.a['href']
#                 span = u.find("span",{"class":"s-item__price"})
#                 if span is not None:
#                     price = span.text
#                 else:
#                     price ='100'
#                 p.append(products(name,img,price,link))
#             except TypeError:
#                 print
#     return p

def abc_p(arg):
    p = []
    a = arg.split()
    my_a_url = 'https://paytmmall.com/shop/search?q='
    for value in a:
        my_a_url += value + '%20'
    my_a_url = my_a_url[:-3]        #to remove extra %20
    my_a_url +='&from=organic&child_site_id=6&site_id=2'
    url = my_a_url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

    # fetching the url, raising error if operation fails
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
    html = uReq(url)
    a_page_soup = soup(html, 'html.parser')
    a_containers = a_page_soup.findAll("div",{"class":"_2i1r"})
    i=0
    for u in a_containers:
            try:
                name = u.img['alt']
                img = u.img['src']
                link ='https://paytmmall.com'+u.a['href']
                span = u.find("div",{"class":"_1kMS"})
                if span is not None:
                    price = span.text
                span = u.find("span",{"class":"c-ax"})
                if span is not None:
                    discount = span.text
                else:
                    price ='100'
                    discount ='0%'
                i_id=name[:30]
                i_id=i_id.replace(' ','_')
                i_id=i_id.replace('.','_')
                i_id=i_id.replace('*','_')
                i_id=i_id.replace('|','_')
                i_id=i_id.replace('+','_')
                i_id=i_id.replace('-','_')
                i_id=i_id.replace('₹','_')
                i_id=i_id.replace(',','_')
                i_id=i_id.replace('(','_')
                i_id=i_id.replace(')','_')
                p.append(products(i_id,name,img,price,discount,link))
            except TypeError:
                print
            i+=1;
    return p

def abc_f(arg):
    p = []
    a = arg.split()
    my_a_url = 'https://www.flipkart.com/search?q='
    for value in a:
        my_a_url += value + '%20'
    my_a_url = my_a_url[:-3]
    my_a_url +='&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    url = my_a_url
    html = uReq(url)
    a_page_soup = soup(html, 'html.parser')
    a_containers = a_page_soup.findAll("div",{"class":"_1UoZlX"})
    try:
        a_containers[1]
    except IndexError:
        return p
    i = 0
    for u in a_containers:
        i+=1
        if i<=2:
            try:
                name = u.img['alt']
                img = u.img['src']
                link =  'https://www.flipkart.com'+u.a['href']
                html_i = uReq(link)
                a_page_soup_i = soup(html_i, 'html.parser')
                a_containers_i = a_page_soup_i.find("div",{"class":"_2_AcLJ"})
                img = a_containers_i['style']
                img = img.replace('/128/128/', '/1000/1000/')
                img = img[21:-1]
                span = u.find("div",{"class":"_2rQ-NK"})
                if span is not None:
                    price = span.text
                else:
                    price ='100'
                span = u.find("div",{"class":"VGWI6T"})
                if span is not None:
                    discount = span.text
                else:
                    discount = '0% off'
                i_id=name[:30]
                i_id=i_id.replace(' ','_')
                i_id=i_id.replace('.','_')
                i_id=i_id.replace('*','_')
                i_id=i_id.replace('|','_')
                i_id=i_id.replace('+','_')
                i_id=i_id.replace('-','_')
                i_id=i_id.replace('₹','_')
                i_id=i_id.replace(',','_')
                i_id=i_id.replace('(','_')
                i_id=i_id.replace(')','_')
                p.append(products(i_id,name,img,price,discount,link))
            except TypeError:
                print
    return p

def abc_a(arg):
    p = []
    price ='100'
    discount = ''
    a = arg.split()
    my_a_url = 'https://www.amazon.in/s?k='
    for value in a:
        my_a_url += value + '+'
    my_a_url = my_a_url[:-1]
    my_a_url +='&ref=nb_sb_noss_2'
    url = my_a_url
    html = uReq(url)
    a_page_soup = soup(html, 'html.parser')
    a_containers = a_page_soup.findAll("div",{"class":"s-border-bottom"})
    i = 0
    for u in a_containers:
            try:
                name = u.img['alt']
                img = u.img['src']
                link = 'https://www.amazon.in'+u.a['href']
                span = u.find("span",{"class":"a-price-whole"})
                if span is not None:
                    price = span.text
                i_id=name[:30]
                i_id=i_id.replace(' ','_')
                i_id=i_id.replace('.','_')
                i_id=i_id.replace('*','_')
                i_id=i_id.replace('|','_')
                i_id=i_id.replace('+','_')
                i_id=i_id.replace('-','_')
                i_id=i_id.replace('₹','_')
                i_id=i_id.replace(',','_')
                i_id=i_id.replace('(','_')
                i_id=i_id.replace(')','_')
                p.append(products(i_id,name,img,price,discount,link))
            except TypeError:
                print
    return p
def pqr_f(item):
    p = []
    spec_item = []
    spec_value = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    try:
        response = requests.get(item, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
    html = uReq(item)
    page_soup = soup(html, 'html.parser')
    containers = page_soup.findAll("div",{"class":"_2rDnao"})
    i = page_soup.find("div",{"class":"_2_AcLJ"})
    span = page_soup.find("div",{"class":"_3qQ9m1"})
    spec = page_soup.find("div",{"class":"MocXoX"})
    spec_i = page_soup.findAll("td",{"class":"col-3-12"})
    spec_v = page_soup.findAll("li",{"class":"_3YhLQA"})
    for u,v in zip(spec_i,spec_v):
        spec_item.append(u.text)
        spec_value.append(v.text)
    for u in containers:
        try:
            name = u.img['alt']
            img = i['style']
            img = img.replace('/128/128/', '/1000/1000/')
            img = img[21:-1]
            price = span.text
            p.append(detail(name,img,price,spec_item,spec_value))
        except TypeError:
            print
    return p

def pqr_p(item):
    p = []
    spec_item = []
    spec_value = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}
    try:
        response = requests.get(item, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
    html = uReq(item)
    page_soup = soup(html, 'html.parser')
    container = page_soup.find("img",{"class":"_3v_O"})

    span = page_soup.find("span",{"class":"_1V3w"})
    spec = page_soup.find("div",{"class":"UlvO"})
    spec_i = spec.findAll("div",{"class":"w3LC"})
    spec_v = spec.findAll("div",{"class":"_2LOI"})
    for u,v in zip(spec_i,spec_v):
        spec_item.append(u.text)
        spec_value.append(v.text)
    try:
        name = container['alt']
        img = container['src']
        price = span.text
        p.append(detail(name,img,price,spec_item,spec_value))
    except TypeError:
        print
    return p

C = Compare.objects.first()

def result(request):
    r = []
    fulltext = request.GET['fulltext']
    print('___________')
    print(fulltext)
    print('___________')
    f = abc_f(fulltext)
    p = abc_p(fulltext)
    # a = abc_a(fulltext)
    i=0
    for v in range(10):
        try:
            r.append(products(f[v].i_id,f[v].name,f[v].img,f[v].price,f[v].discount,f[v].link))
        except IndexError:
            print
        try:
            r.append(products(p[v].i_id,p[v].name,p[v].img,p[v].price,p[v].discount,p[v].link))
        except IndexError:
            print
        # try:
        #     r.append(products(a[v].i_id,a[v].name,a[v].img,a[v].price,a[v].discount,a[v].link))
        # except IndexError:
        #     print
    dic = {'r':r,'C':C,'insert_me':fulltext}
    return render(request,'result.html',dic)

def compare(request):
    spec_i = []
    p_spec_v = []
    q_spec_v = []
    r_spec_v = []
    i_spec_i = []
    i_p_spec_v = []
    i_q_spec_v = []
    i_r_spec_v = []
    j_spec_i = []
    j_p_spec_v = []
    j_q_spec_v = []
    j_r_spec_v = []
    ij_spec_i = []
    ij_p_spec_v = []
    ij_q_spec_v = []
    ij_r_spec_v = []
    a = detail('','','',spec_i,p_spec_v)
    b = [a,]
    link1=C.item1_link
    link2=C.item2_link
    link3=C.item3_link
    p_i=0
    q_i=0
    r_i=0
    if 'paytmmall' in link1:
        p = pqr_p(link1)
    elif 'flipkart' in link1:
        p = pqr_f(link1)
    else:
        p_i=1
        p = b

    if 'paytmmall' in link2:
        q = pqr_p(link2)
    elif 'flipkart' in link2:
        q = pqr_f(link2)
    else:
        q_i=1
        q = b

    if 'paytmmall' in link3:
        r = pqr_p(link3)
    elif 'flipkart' in link3:
        r = pqr_f(link3)
    else:
        r_i=1
        r = b

    if p_i==1:
        p = q
        q = r
        r = b
    elif q_i==1:
        q = r
        r = b
    for u in p[0].spec_item:
        try:
            i = q[0].spec_item.index(u)
        except ValueError:
            try:
                j = r[0].spec_item.index(u)
            except ValueError:
                ij_spec_i.append(u)
                ij_p_spec_v.append(p[0].spec_value[p[0].spec_item.index(u)])
                ij_q_spec_v.append('')
                ij_r_spec_v.append('')
                continue
            spec_i.append(u)
            i_p_spec_v.append(p[0].spec_value[p[0].spec_item.index(u)])
            i_q_spec_v.append('')
            i_r_spec_v.append(r[0].spec_value[j])
            continue
        try:
            j = r[0].spec_item.index(u)
        except ValueError:
            j_spec_i.append(u)
            j_p_spec_v.append(p[0].spec_value[p[0].spec_item.index(u)])
            j_q_spec_v.append(q[0].spec_value[i])
            j_r_spec_v.append('')
            continue
        spec_i.append(u)
        p_spec_v.append(p[0].spec_value[p[0].spec_item.index(u)])
        q_spec_v.append(q[0].spec_value[i])
        r_spec_v.append(r[0].spec_value[j])
    p[0].spec_item = spec_i + j_spec_i + i_spec_i + ij_spec_i
    p[0].spec_value = p_spec_v + j_p_spec_v + i_p_spec_v + ij_p_spec_v
    q[0].spec_value = q_spec_v + j_q_spec_v + i_q_spec_v + ij_q_spec_v
    r[0].spec_value = r_spec_v + j_r_spec_v + i_r_spec_v + ij_r_spec_v
    dic = {'p':p,'q':q,'r':r}
    return render(request,'compare.html',dic)


def comp(request):
    if request.method == 'POST':
        item1 = request.POST.get('i1')
        item2 = request.POST.get('i2')
        item3 = request.POST.get('i3')
        item1_img = request.POST.get('i1_img')
        item2_img = request.POST.get('i2_img')
        item3_img = request.POST.get('i3_img')
        item1_link = request.POST.get('i1_link')
        item2_link = request.POST.get('i2_link')
        item3_link = request.POST.get('i3_link')
        if item1 is not None:
            C.item1 = item1
        else:
            C.item1 = ''
        if item2 is not None:
            C.item2 = item2
        else:
            C.item2 = ''
        if item3 is not None:
            C.item3 = item3
        else:
            C.item3 = ''
# img
        if item1_img is not None:
            C.item1_img = item1_img
        else:
            C.item1_img = ''
        if item2_img is not None:
            C.item2_img = item2_img
        else:
            C.item2_img = ''
        if item3_img is not None:
            C.item3_img = item3_img
        else:
            C.item3_img = ''
# link
        if item1_link is not None:
            C.item1_link = item1_link
        else:
            C.item1_link = ''
        if item2_link is not None:
            C.item2_link = item2_link
        else:
            C.item2_link = ''
        if item3_link is not None:
            C.item3_link = item3_link
        else:
            C.item3_link = ''

        C.save()

    return HttpResponse('')
