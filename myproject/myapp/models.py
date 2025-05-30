from django.db import models
from django.contrib.auth.models import User

class Tree(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='trees/', blank=True, null=True)
    care_instructions = models.TextField(help_text="วิธีดูแลต้นไม้ เช่น รดน้ำ ใส่ปุ๋ย")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class PlantingArea(models.Model):
    province = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Tree Location"
        verbose_name_plural = "Tree Locations"

    def __str__(self):
        return self.province

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

class TreePlanting(models.Model):
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    planting_area = models.ForeignKey(PlantingArea, on_delete=models.CASCADE)
    planted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tree.name} planted in {self.planting_area.province} on {self.planted_date}"

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='equipment_images/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class UserTreeOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('planted', 'ปลูกแล้ว'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    planting_area = models.ForeignKey(PlantingArea, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tree.name} x{self.quantity} by {self.user.username} ({self.get_status_display()})"

