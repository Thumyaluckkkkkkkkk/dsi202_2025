import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import Tree, PlantingArea, PlantingPlan, Equipment
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage

# 🏠 หน้าแรก
def home(request):
    return render(request, 'home.html')

# 🌳 แสดงรายการต้นไม้
def tree_list(request):
    query = request.GET.get('q')
    trees = Tree.objects.filter(name__icontains=query) if query else Tree.objects.all()
    return render(request, 'plantapp/tree_list.html', {'trees': trees})

# 🌳 รายละเอียดต้นไม้
@login_required
def tree_detail(request, tree_id):
    tree = get_object_or_404(Tree, id=tree_id)
    return render(request, 'plantapp/tree_detail.html', {'tree': tree})

# 📍 พื้นที่ปลูก
@login_required
def planting_area_list(request):
    areas = PlantingArea.objects.filter(user=request.user)
    return render(request, 'plantapp/planting_area_list.html', {'areas': areas})

# 🗓️ แผนการปลูก
@login_required
def planting_plan_list(request):
    plans = PlantingPlan.objects.filter(user=request.user)
    return render(request, 'plantapp/planting_plan_list.html', {'plans': plans})

# 🛒 หน้ารวมสินค้า
def shop_page(request):
    trees = Tree.objects.all()
    equipment_list = Equipment.objects.all()
    return render(request, 'plantapp/shop.html', {
        'trees': trees,
        'equipment_list': equipment_list,
    })

# ⚙️ อุปกรณ์ปลูก
@login_required
def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'plantapp/equipment_list.html', {'equipment': equipment})

# ➕ ใส่สินค้าในตะกร้า
@require_POST
@login_required
def add_to_cart(request):
    item_id = request.POST.get('item_id')
    item_type = request.POST.get('item_type')

    cart = request.session.get('cart', [])
    cart.append({'id': item_id, 'type': item_type})
    request.session['cart'] = cart

    return redirect('myapp:cart')

# 🧺 ดูตะกร้าสินค้า
@login_required
def cart_view(request):
    cart = request.session.get('cart', [])
    items = []

    for i, entry in enumerate(cart):
        if entry['type'] == 'tree':
            obj = get_object_or_404(Tree, id=entry['id'])
        else:
            obj = get_object_or_404(Equipment, id=entry['id'])

        items.append({
            'id': obj.id,
            'name': obj.name,
            'price': obj.price,
            'image': obj.image.url if obj.image else None,
            'type': entry['type'],
            'index': i,
        })

    return render(request, 'plantapp/cart.html', {'cart_items': items})

# ❌ ลบสินค้าออกจากตะกร้า (ใช้ index)
@login_required
def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    try:
        del cart[index]
        request.session['cart'] = cart
    except IndexError:
        pass
    return redirect('myapp:cart')

# ✅ หน้าชำระเงิน เฉพาะสินค้าที่ถูกติ๊ก
@login_required
def checkout(request):
    if request.method == 'POST':
        selected_indexes = request.POST.getlist('selected_items')
        cart = request.session.get('cart', [])
        selected_items = []
        total = 0

        for idx in selected_indexes:
            try:
                i = int(idx)
                entry = cart[i]
                if entry['type'] == 'tree':
                    obj = get_object_or_404(Tree, id=entry['id'])
                else:
                    obj = get_object_or_404(Equipment, id=entry['id'])

                selected_items.append({
                    'id': obj.id,
                    'name': obj.name,
                    'price': obj.price,
                    'image': obj.image.url if obj.image else None,
                    'type': entry['type'],
                })
                total += obj.price
            except (IndexError, ValueError):
                continue

        request.session['selected_checkout_items'] = selected_indexes
        return render(request, 'plantapp/checkout.html', {
            'items': selected_items,
            'total': total,
        })

    return redirect('myapp:cart')

# 📤 อัปโหลดสลิป
@require_POST
@login_required
def upload_slip(request):
    slip = request.FILES.get('slip')
    if not slip:
        return redirect('myapp:checkout')

    fs = FileSystemStorage(location=os.path.join('media', 'payment_slips'))
    filename = fs.save(slip.name, slip)

    request.session['payment_slip'] = filename
    return redirect('myapp:home')
