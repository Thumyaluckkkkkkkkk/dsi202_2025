import libscrc
import base64
import io
import qrcode

from django.db.models import Q 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Tree, Equipment, PlantingArea, UserTreeOrder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone

def home(request):
    return render(request, 'home.html')

def tree_list(request):
    query = request.GET.get("q", "")
    if query:
        trees = Tree.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        trees = Tree.objects.all()
    return render(request, 'plantapp/tree_list.html', {
        'trees': trees,
        'query': query,
    })

@login_required
def tree_detail(request, tree_id):
    tree = get_object_or_404(Tree, id=tree_id)
    return render(request, 'plantapp/tree_detail.html', {'tree': tree})

def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'plantapp/equipment_list.html', {'equipment': equipment})

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item_type = request.POST.get('item_type')
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', [])
        if item_type == 'tree':
            item = get_object_or_404(Tree, id=item_id)
        elif item_type == 'equipment':
            item = get_object_or_404(Equipment, id=item_id)
        else:
            return redirect('myapp:cart')

        for cart_item in cart:
            if cart_item['id'] == item.id and cart_item['type'] == item_type:
                cart_item['quantity'] += quantity
                break
        else:
            cart.append({
                'id': item.id,
                'name': item.name,
                'price': float(item.price),
                'image': item.image.url if item.image else '',
                'quantity': quantity,
                'type': item_type
            })

        request.session['cart'] = cart
        return redirect('myapp:cart')

@login_required
def cart_view(request):
    cart = request.session.get('cart', [])
    for idx, item in enumerate(cart):
        item['index'] = idx
    return render(request, 'plantapp/cart.html', {'cart_items': cart})

@login_required
@require_POST
def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    try:
        index = int(index)
        if 0 <= index < len(cart):
            del cart[index]
            request.session['cart'] = cart
    except Exception as e:
        print("Error removing from cart:", e)
    return redirect('myapp:cart')

@login_required
@require_POST
def confirm_cart(request):
    cart = request.session.get('cart', [])
    selected_indexes = request.POST.getlist('selected_items')

    selected_indexes = [int(i) for i in selected_indexes if i.isdigit()]
    selected_items = [item for idx, item in enumerate(cart) if idx in selected_indexes]

    request.session['checkout_cart'] = selected_items

    has_tree = any(item['type'] == 'tree' for item in selected_items)
    if has_tree:
        return redirect('myapp:tree_location_list')
    else:
        return redirect('myapp:equipment_list')

@login_required
def tree_location_list(request):
    query = request.GET.get('q', '')
    if query:
        locations = PlantingArea.objects.filter(province__icontains=query)
    else:
        locations = PlantingArea.objects.all()
    return render(request, 'plantapp/tree_location_list.html', {
        'locations': locations,
        'query': query,
    })

@login_required
def select_location_for_tree(request):
    location_id = request.GET.get('location_id')
    if location_id:
        location = get_object_or_404(PlantingArea, id=location_id)
        request.session['tree_location'] = location.province
        request.session['tree_location_description'] = location.description
    return redirect('myapp:checkout')

def generate_qr_base64(phone_number, amount):
    payload = f"00020101021129370016A00000067701011101130066{phone_number[1:]}530376454{len(f'{amount:.2f}'):02d}{amount:.2f}5802TH6304"
    crc = libscrc.ccitt_false(payload.encode('ascii')).to_bytes(2, 'big').hex().upper()
    final_payload = payload + crc
    img = qrcode.make(final_payload)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

@login_required
def checkout(request):
    cart = request.session.get('checkout_cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)

    location = request.session.get('tree_location', 'ไม่ระบุ')
    location_desc = request.session.get('tree_location_description', '')

    qr_code = generate_qr_base64("0944245565", total)

    return render(request, 'plantapp/checkout.html', {
        'items': cart,
        'total': total,
        'location': location,
        'location_desc': location_desc,
        'qr_code': qr_code,
    })

@login_required
def confirm_payment(request):
    cart = request.session.get('checkout_cart', [])
    location_name = request.session.get('tree_location', None)

    if cart and location_name:
        planting_area = PlantingArea.objects.filter(province=location_name).first()

        for item in cart:
            if item['type'] == 'tree':
                UserTreeOrder.objects.create(
                    user=request.user,
                    tree_id=item['id'],
                    quantity=item['quantity'],
                    planting_area=planting_area,
                    status='pending',
                    order_date=timezone.now()
                )

    request.session['cart'] = []
    request.session['checkout_cart'] = []

    return redirect('myapp:my_orders')

@login_required
def my_orders(request):
    orders = UserTreeOrder.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'plantapp/my_orders.html', {'orders': orders})

def upload_slip(request):
    return render(request, 'plantapp/upload_slip.html')

def shop_page(request):
    return render(request, 'plantapp/shop.html')

@login_required
def notifications(request):
    orders = UserTreeOrder.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'plantapp/notifications.html', {'orders': orders})




