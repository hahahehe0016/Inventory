from turtle import ondrag
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from uuid import uuid4

# Create your models here.
site_choice = (
    ('Manila','Manila'),
    ('Cebu','Cebu')
)
CATEGORY = (
    ('Hard Disk Drive', 'Hard Disk Drive'),
    ('Solid State Drive', 'Solid State Drive'),
    ('Graphics Card', 'Graphics Card'),
    ('Laptop', 'Laptop'),
    ('RAM', 'RAM'),
    ('Charger', 'Charger'),
    ('UPS', 'UPS'),
    ('Mouse', 'Mouse'),
    ('Keyboard', 'Keyboard'),
    ('Motherboard', 'Motherboard'),
    ('Monitor', 'Monitor'),
    ('Power Supply', 'Power Supply'),
    ('Router', 'Router'),
    ('AVR', 'AVR'),
    ('Tablet', 'Tablet'),
    ('System Unit', 'System Unit'),
    ('Audio Devices', 'Audio Devices'),
    ('CPU', 'CPU'),
    ('Others', 'Others'),
)


SUBCATEGORY = (
    #('Extensions', 'Extensions'),
    #('Cables', 'Cables'),
    #('Adaptors', 'Adaptors'),
    #('Handtools', 'Handtools'),
    #('External Hard Drives', 'External Hard Drives'),
    #('Flash Drives', 'Flash Drives'),
    #('Others', 'Others'),
)

DEPARTMENT = (
    ('Operations', 'Operations'),
    ('Marketing', 'Marketing'),
    ('IT', 'IT'),
    ('Management', 'Management'),
    ('Administration', 'Administration'),
)

ROLE = (
    ('Operations', 'Operations'),
    ('Marketing', 'Marketing'),
    ('IT', 'IT'),
    ('Management', 'Management'),
    ('Administration', 'Administration'),
)

STATUS = (
    ('Not Working', 'Not Working'),
    ('Working', 'Working')
)

SLOT_TYPE = (
    ('Motherboard', 'Motherboard'),
    ('Processor', 'Processor'),
    ('RAM 1', 'RAM 1'),
    ('RAM 2', 'RAM 2'),
    ('RAM 3', 'RAM 3'),
    ('RAM 4', 'RAM 4'),
    ('HDD 1', 'HDD 1'),
    ('HDD 2', 'HDD 2'),
    ('HDD 3', 'HDD 3'),
    ('HDD 4', 'HDD 4'),
    ('Power Supply Unit', 'Power Supply Unit'),
    ('Others', 'Others'),
)

COMPO_STATUS = (
    ('Active', 'Active'),
    ('Inactive', 'Inactive')
)

def generate_po_number():
    return 'PO-' + str(uuid4())[:7]

def generate_jo_number():
    return 'JO-' + str(uuid4())[:7]

def date_current():
    current_date = datetime.now()
    return current_date

def asset_tag_number():
    dt = datetime.now()
    no = Product.objects.all().count()
    counter = 0
    asset_number_date = int(str(dt.strftime('%Y%m%d')))
    if no == 0:
        counter_str = str(counter).zfill(5)
        asset_number_ref = "{}-{}".format(asset_number_date, counter_str)
        return asset_number_ref
    else: 
        counter += no + 1
        counter_str = str(counter).zfill(5)
        asset_number_ref = "{}-{}".format(asset_number_date, counter_str)
        return asset_number_ref




class Product(models.Model):
    po = models.CharField(max_length=100 ,default=generate_po_number, editable=False)
    classification = models.CharField(max_length=50, null=True, blank=True)
    atn = models.CharField(max_length=50, editable = False, unique=True)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    asset_type = models.CharField(max_length=20, choices=CATEGORY, blank=True)
    site = models.CharField(max_length=250, null=True, blank=True, choices=site_choice)
    #subcategory = models.CharField(max_length=20, choices=SUBCATEGORY, null=True)
    #quantity = models.PositiveIntegerField(default=1, null=True)
    #price = models.PositiveIntegerField(null=True)
    department = models.CharField(max_length=100, choices=DEPARTMENT, null=True, blank=True)
    serial_number = models.CharField(max_length=100, null=True, unique=True, blank=True)
    OR_number = models.CharField(max_length=100, null=True, unique=False, blank=True)
    supplier_name = models.CharField(max_length=100, null=True, default=None, blank=True)
    #assigned_to = models.CharField(max_length=100, null=True, default=None, blank=True)
    #borrowed_by = models.CharField(max_length=100, null=True, default=None, blank=True)
    #returned_by = models.CharField(max_length=100, null=True, default=None, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)
    adder = models.ForeignKey(User, models.CASCADE, null=False)
    asset_image = models.ImageField(default='Product_Default.png', upload_to='Products')

    class Meta:
        verbose_name_plural = 'Product'

    def __str__(self):
        return f'{self.atn} / {self.serial_number} / {self.model_name}'

    def save(self, *args, **kwargs): #overriding the save function para matawag natin 'yung function na "set_atn". Ginagamit 'yun for generating item's ATN.
        super().save(*args, **kwargs)
        self.set_atn()

    def set_atn(self):
        dt = datetime.now()
        component_name = self.model_name
        if not self.atn:
            asset_number_date = str(dt.strftime('%Y%m%d')) #Pagtawag ng current date
            asset_number_ref = str(self.id).zfill(5) #Pag-fill ng mga zeros before the number.
            asset_tag_number = str(self.classification) + asset_number_date + asset_number_ref #Ito na 'yung kabuuan ng ATN.
            if self.classification == "016": #Dito 'yung pag-add ng object sa Component Table kapag may na-create na system unit sa asset table.
                Component.objects.create(
                    compo_atn = asset_tag_number,
                    catn = "X-" + asset_tag_number,
                    compo_name = self.model_name
                )
            asset = Product.objects.get(id=self.id)
            asset.atn = asset_tag_number
            asset.save()


class Employee(models.Model):
    in_name = models.CharField(max_length=100, null=False)
    out_name = models.CharField(max_length=100, null=False)
    emp_email = models.EmailField(max_length=30, null=True)
    emp_department = models.CharField(max_length=30, choices=ROLE, null=False)

    class Meta:
        verbose_name_plural = 'Employee'

    def __str__(self):
        return f'{self.in_name} {self.out_name}'

class Order(models.Model):
    jo = models.CharField(max_length=100 ,default=generate_jo_number, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, limit_choices_to={"status": "Not Working"}, unique=True, error_messages={'unique': "Job order has been created for this unit/device already."})
    employee = models.ForeignKey(User, models.CASCADE, null=False)
    person_in_charge = models.ForeignKey(Employee, models.CASCADE, null=False)
    date = models.DateTimeField(auto_now_add=True)
    disposal_remarks = models.TextField()

    class Meta:
        verbose_name_plural = 'Job Order'

    def __str__(self):
        return f'{self.product} was ordered by {self.employee.username} last {self.date}'



class Component(models.Model):
    compo_atn = models.CharField(max_length=100, null=True, editable=False)
    compo_name = models.CharField(max_length=100, null=True, editable=False)
    catn = models.CharField(max_length= 100, null=True, editable=False)
    date_installed = models.DateField(null=True, blank=True, verbose_name=u"Installation Date")
    date_replaced = models.DateField(null=True, blank=True, verbose_name=u"Replace Date")
    activeness = models.CharField(max_length=20, choices=COMPO_STATUS, null=True, blank=True, verbose_name=u"Status")
    #components
    motherboard = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'motherboard', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type": "Motherboard"})
    processor = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'processor', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type": "CPU"})
    gpu = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'GPU', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type": "Graphics Card"}, verbose_name=u"GPU")
    RAM1 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'RAM1', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type": "RAM"}, verbose_name=u"RAM #1")
    RAM2 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'RAM2', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type": "RAM"}, verbose_name=u"RAM #2")
    RAM3 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'RAM3', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type": "RAM"}, verbose_name=u"RAM #3")
    RAM4 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'RAM4', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type": "RAM"}, verbose_name=u"RAM #4")
    PSU = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'PSU', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type": "Power Supply"}, verbose_name=u"Power Supply")
    HDD1 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'HDD1', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type__in": ["Hard Disk Drive", "Solid State Drive"]},verbose_name=u"HDD #1")
    HDD2 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'HDD2', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type__in": ["Hard Disk Drive", "Solid State Drive"]}, verbose_name=u"HDD #2")
    HDD3 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'HDD3', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type__in": ["Hard Disk Drive", "Solid State Drive"]}, verbose_name=u"HDD #3")
    HDD4 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'HDD4', unique=True, error_messages={'unique': "This component is already installed in another device!"}, limit_choices_to={"asset_type__in": ["Hard Disk Drive", "Solid State Drive"]},verbose_name=u"HDD #4")
    Others = models.CharField(max_length= 100, null=True, blank=True)


    class Meta:
        verbose_name_plural = 'Component'

    def __str__(self):
        return f'{self.catn} / {self.compo_name}'


LOCATIONS = (
    ('Room - 2G', 'Room - 2G'),
    ('Room - 304', 'Room - 304'),
    ('Room - 305', 'Room - 305'),
    ('Admin', 'Admin'),
    ('IT - Room', 'IT - Room'),
    ('Clinic', 'Clinic'),
    ('Conference - Room', 'Conference - Room'),
    ('Others', 'Others')
)

class Allocation(models.Model):
    allocation_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=30, choices=LOCATIONS)
    asset_allocation = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="asset_alloc", unique=True, error_messages={'unique': "This device is already allocated somewhere else."}, limit_choices_to={"asset_type__in": ["Hard Disk Drive", "Solid State Drive", 'Graphics Card', 'Laptop', 'RAM', 'Charger', 'UPS', 'Mouse', 'Keyboard', 'Motherboard', 'Monitor', 'Power Supply', 'Router', 'AVR', 'Tablet', 'Audio Devices', 'CPU', 'Others']})
    system_allocation = models.ForeignKey(Component, on_delete=models.SET_NULL, null=True, blank=True, related_name="system_alloc", unique=True, error_messages={'unique': "This device is already allocated somewhere else."})
    alloc_date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name_plural = 'Allocation'

    def __str__(self):
        return f'{self.id}'

    def save(self, *args, **kwargs):
        if self.alloc_date:
            self.alloc_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Inayos ko lang dito 'yung time format kapag mag-u-update ka ng item
        super().save(*args, **kwargs)


class Disposal(models.Model):
    disposal_name = models.CharField(max_length=30)
    disposal_serial_number = models.CharField(max_length=100, null=True, blank=True)
    disposal_date = models.DateTimeField(auto_now_add=True)
    remarks = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Disposal'

    def __str__(self):
        return f'{self.disposal_name} / {self.disposal_serial_number}'