from django.db import models
from django.contrib.auth.models import User

class Tree(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='trees/', blank=True, null=True)
    care_instructions = models.TextField(help_text="วิธีดูแลต้นไม้ เช่น รดน้ำ ใส่ปุ๋ย")

    def __str__(self):
        return self.name


class PlantingArea(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    size_in_sq_meters = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.location})"


class PlantingPlan(models.Model):
    PLAN_CHOICES = [
        ('monthly_1', 'ปลูก 1 ต้น/เดือน'),
        ('yearly_10', 'ปลูก 10 ต้น/ปี'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_type = models.CharField(max_length=20, choices=PLAN_CHOICES)
    start_date = models.DateField()

    def __str__(self):
        return f"{self.get_plan_type_display()} - {self.user.username}"

# --- เติมส่วนเสริมเพื่อเพิ่มความสะดวก ---

# เพิ่ม Model สำหรับบันทึกว่าต้นไม้แต่ละต้นปลูกที่ไหน (เชื่อม Tree กับ PlantingArea)
class TreePlanting(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    planting_area = models.ForeignKey(PlantingArea, on_delete=models.CASCADE)
    planted_date = models.DateField(auto_now_add=True)  # วันที่ปลูก

    def __str__(self):
        return f"{self.tree.name} planted at {self.planting_area.name} on {self.planted_date}"
