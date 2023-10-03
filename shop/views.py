from django.shortcuts import render
from .models import Products,Order
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def index(request):
    product_objects = Products.objects.all()

    #search code
    item_name = request.GET.get('item_name')
    if item_name != '' and item_name is not None:
        product_objects = product_objects.filter(title__icontains=item_name)

    # paginator code
    paginator = Paginator(product_objects,4)
    page = request.GET.get("page")
    product_objects = paginator.get_page(page)

    return render(request,'shop/index.html',{'product_objects':product_objects})

    
    


def detail(request,id):
    product_object = Products.objects.get(pk=id)
    return render(request,'shop/detail.html',{'product_object':product_object})


@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        try:
            # 读取请求体数据并存储在一个变量中
            body_unicode = request.body.decode('utf-8')
            post_data = json.loads(body_unicode)

            # 从post_data中提取姓名、信箱、地址和总价
            name = post_data.get('name')
            email = post_data.get('email')
            address = post_data.get('address')
            total_price = post_data.get('total_price')

            # 这里可以进行订单的创建和保存，以下是示例代码
            # order = Order.objects.create(name=name, email=email, address=address, total_price=total_price)
            # order.save()

            # 这里你可以根据需要返回任何其他信息，例如订单确认信息
            response_data = {
                'message': 'Order placed successfully.',
                'name': name,
                'email': email,
                'address': address,
                'total_price': total_price
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            # 如果JSON解析失败，返回错误响应
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    # 如果不是POST请求，渲染checkout页面
    return render(request, 'shop/checkout.html')

def get_product_name(request, product_id):
    try:
        product = Products.objects.get(pk=product_id)
        product_data = {
            'product_name': product.title,
            'product_price': product.price
        }
        return JsonResponse(product_data)
    except Products.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    
