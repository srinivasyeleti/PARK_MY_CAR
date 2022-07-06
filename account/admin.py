from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account
from .forms import UserRegistrationForm

# Register your models here.

class AccountAdmin(UserAdmin) :
	# exclude							= ['password1', 'password2']
	# form							= UserRegistrationForm # overrides the admin form for registeration,
	exclude							= ['booked_slot', 'slot_id']
	list_display					= ('email', 'username', 'date_joined', 'last_login', 'is_active', 'is_staff')
	search_fields					= ('email', 'username')
	readonly_fields					= ('date_joined', 'last_login')


	filter_horizontal				= ()
	list_filter						= ()
	fieldsets						= ()	


admin.site.register(Account, AccountAdmin)