from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group, Permission, User

def send_otp_email(email: str, otp: str):
    try:
        subject = "Your One-Time Password (OTP)"
        message = f"Your login code is {otp}. It is valid for 5 minutes. Do not share this code."
    
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL, 
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        return False

def create_group_and_add_permissions(group_name: str, permission_codenames: list):
    group, created = Group.objects.get_or_create(name=group_name)
    
    if not created:
        group.permissions.clear()
        
    permissions_to_add = []
    for codename in permission_codenames:
        try:
            permission = Permission.objects.get(codename=codename)
            permissions_to_add.append(permission)
        except Permission.DoesNotExist:
            print(f"Permission with codename '{codename}' not found. Skipping.")

    group.permissions.set(permissions_to_add)
    print(f"Group '{group_name}' created/updated with {len(permissions_to_add)} permissions.")
    
    return group

def add_user_to_group(user: User,group_name: str):
    groups_to_add = []
    permissions_to_add=[
        "add_address"
        "change_address"
        "delete_address"
        "view_address"
        "view_category"
        "view_stock"
        "view_product"
        "view_image"
        "add_orders"
        "change_orders"
        "delete_orders"
        "view_orders"
        "add_cart"
        "change_cart"
        "delete_cart"
        "view_cart"
        "add_wishlist"
        "change_wishlist"
        "delete_wishlist"
        "view_wishlist"
    ]
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist as e:
        group = create_group_and_add_permissions(group_name, permissions_to_add)
    groups_to_add.append(group)
    user = user.groups.set(groups_to_add)
    
     