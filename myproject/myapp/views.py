import os, base64
from io import BytesIO
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.files.storage import FileSystemStorage
import qrcode
from myapp.utils.promptpay_qr import qr_code  # ✅ ใช้ไฟล์ utils ที่สร้างไว้

from .models import Tree, PlantingArea, PlantingPlan, Equipment

# ✅ หน้าแรก
def home(request):
    return render(request, 'home.html')

# ✅ รายการต้นไม้
def tree_list(request):
    query = request.GET.get('q')
    trees = Tree.objects.filter(name__icontains=query) if query else Tree.objects.all()
    return render(request, 'plantapp/tree_list.html', {'trees': trees})

# ✅ รายละเอียดต้นไม้
@login_required
def tree_detail(request, tree_id):
    tree = get_object_or_404(Tree, id=tree_id)
    return render(request, 'plantapp/tree_detail.html', {'tree': tree})

# ✅ รายการพื้นที่ปลูก
@login_required
def planting_area_list(request):
    areas = PlantingArea.objects.filter(user=request.user)
    return render(request, 'plantapp/planting_area_list.html', {'areas': areas})

# ✅ แผนการปลูก
@login_required
def planting_plan_list(request):
    plans = PlantingPlan.objects.filter(user=request.user)
    return render(request, 'plantapp/planting_plan_list.html', {'plans': plans})

# ✅ หน้าร้านค้า
def shop_page(request):
    trees = Tree.objects.all()
    equipment_list = Equipment.objects.all()
    return render(request, 'plantapp/shop.html', {
        'trees': trees,
        'equipment_list': equipment_list,
    })

# ✅ รายการอุปกรณ์
@login_required
def equipment_list(request):
    query = request.GET.get('q')
    equipment = Equipment.objects.filter(name__icontains=query) if query else Equipment.objects.all()
    return render(request, 'plantapp/equipment_list.html', {'equipment_list': equipment})

# ✅ เพิ่มสินค้าลงตะกร้า
@require_POST
@login_required
def add_to_cart(request):
    item_id = request.POST.get('item_id')
    item_type = request.POST.get('item_type')
    cart = request.session.get('cart', [])
    cart.append({'id': item_id, 'type': item_type})
    request.session['cart'] = cart
    return redirect('myapp:cart')

# ✅ ดูตะกร้าสินค้า
@login_required
def cart_view(request):
    cart = request.session.get('cart', [])
    items = []
    for i, entry in enumerate(cart):
        obj = get_object_or_404(Tree if entry['type'] == 'tree' else Equipment, id=entry['id'])
        items.append({
            'id': obj.id,
            'name': obj.name,
            'price': obj.price,
            'image': obj.image.url if obj.image else None,
            'type': entry['type'],
            'index': i,
        })
    return render(request, 'plantapp/cart.html', {'cart_items': items})

# ✅ ลบสินค้าออกจากตะกร้า
@login_required
def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    try:
        del cart[index]
        request.session['cart'] = cart
    except IndexError:
        pass
    return redirect('myapp:cart')

# ✅ สร้าง QR พร้อมเพย์แบบใช้ได้จริง
def generate_promptpay_qr(phone_number, amount):
    if amount <= 0:
        return None
    payload = qr_code(phone_number, amount=Decimal(amount))
    qr = qrcode.make(payload)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()

# ✅ หน้าชำระเงินพร้อม QR ตามยอดรวม
@login_required
def checkout(request):
    if request.method == 'POST':
        selected_indexes = request.POST.getlist('selected_items')
        cart = request.session.get('cart', [])
        selected_items, total = [], 0

        for idx in selected_indexes:
            try:
                entry = cart[int(idx)]
                obj = get_object_or_404(Tree if entry['type'] == 'tree' else Equipment, id=entry['id'])
                selected_items.append({
                    'id': obj.id,
                    'name': obj.name,
                    'price': obj.price,
                    'image': obj.image.url if obj.image else None,
                    'type': entry['type'],
                })
                total += obj.price
            except:
                continue

        if not selected_items or total <= 0:
            return redirect('myapp:cart')

        request.session['selected_checkout_items'] = selected_indexes
        qr_code_img = generate_promptpay_qr('0944245565', total)

        return render(request, 'plantapp/checkout.html', {
            'items': selected_items,
            'total': total,
            'qr_code': qr_code_img
        })

    return redirect('myapp:cart')

# ✅ อัปโหลดสลิป
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
