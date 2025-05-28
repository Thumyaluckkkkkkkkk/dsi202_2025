from django.shortcuts import render, get_object_or_404
from .models import Tree, PlantingArea, PlantingPlan, Equipment
from django.contrib.auth.decorators import login_required

# 🏠 หน้าแรก
def home(request):
    return render(request, 'home.html')

# 🌳 แสดงรายการต้นไม้ (ทุกคนเข้าชมได้)
def tree_list(request):
    trees = Tree.objects.all()
    return render(request, 'plantapp/tree_list.html', {'trees': trees})

# 🌳 รายละเอียดต้นไม้
@login_required
def tree_detail(request, tree_id):
    tree = get_object_or_404(Tree, id=tree_id)
    return render(request, 'plantapp/tree_detail.html', {'tree': tree})

# 📍 พื้นที่ปลูกของผู้ใช้
@login_required
def planting_area_list(request):
    areas = PlantingArea.objects.filter(user=request.user)
    return render(request, 'plantapp/planting_area_list.html', {'areas': areas})

# 📅 แผนการปลูกของผู้ใช้
@login_required
def planting_plan_list(request):
    plans = PlantingPlan.objects.filter(user=request.user)
    return render(request, 'plantapp/planting_plan_list.html', {'plans': plans})

# 🛒 หน้า Shop ที่รวมต้นไม้และอุปกรณ์
def shop_page(request):
    trees = Tree.objects.all()
    equipment_list = Equipment.objects.all()
    return render(request, 'plantapp/shop.html', {
        'trees': trees,
        'equipment_list': equipment_list,
    })

# 🧰 หน้าแสดงเฉพาะอุปกรณ์
@login_required
def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'plantapp/equipment_list.html', {'equipment': equipment})
