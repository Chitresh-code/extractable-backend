from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form for admin."""
    
    class Meta:
        model = User
        fields = ('email', 'name')
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(_('A user with this email already exists.'))
        return email


class CustomUserChangeForm(UserChangeForm):
    """Custom user change form for admin."""
    
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Production-ready User admin configuration."""
    
    # Forms to use for creating and changing users
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    
    # Fields to display in the user list
    list_display = (
        'email', 
        'name', 
        'is_active', 
        'is_staff', 
        'is_admin', 
        'is_user',
        'last_login',
        'date_joined_display'
    )
    
    # Fields that can be clicked to go to the user detail page
    list_display_links = ('email', 'name')
    
    # Fields to filter by in the right sidebar
    list_filter = (
        'is_active',
        'is_staff', 
        'is_admin',
        'is_user',
        'last_login',
    )
    
    # Fields to search by
    search_fields = ('email', 'name')
    
    # Default ordering
    ordering = ('email',)
    
    # Fields that can be edited directly in the list view
    list_editable = ('is_active', 'is_user')
    
    # Number of users to show per page
    list_per_page = 25
    
    # Enable filtering by date hierarchy
    date_hierarchy = 'last_login'
    
    # Fieldsets for the user detail page
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('name',)
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_admin', 
                'is_user',
                'is_superuser',
                'groups', 
                'user_permissions'
            ),
            'classes': ('collapse',)
        }),
        (_('Important dates'), {
            'fields': ('last_login',),
            'classes': ('collapse',)
        }),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_user'),
            'classes': ('collapse',)
        }),
    )
    
    # Actions
    actions = ['activate_users', 'deactivate_users', 'make_staff', 'remove_staff']
    
    def date_joined_display(self, obj):
        """Display date joined in a readable format."""
        if hasattr(obj, 'date_joined'):
            return obj.date_joined.strftime('%Y-%m-%d %H:%M')
        return '-'
    date_joined_display.short_description = _('Date Joined')
    date_joined_display.admin_order_field = 'date_joined'
    
    def activate_users(self, request, queryset):
        """Bulk action to activate users."""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            f'{updated} user(s) were successfully activated.'
        )
    activate_users.short_description = _('Activate selected users')
    
    def deactivate_users(self, request, queryset):
        """Bulk action to deactivate users."""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} user(s) were successfully deactivated.'
        )
    deactivate_users.short_description = _('Deactivate selected users')
    
    def make_staff(self, request, queryset):
        """Bulk action to make users staff."""
        updated = queryset.update(is_staff=True)
        self.message_user(
            request,
            f'{updated} user(s) were given staff permissions.'
        )
    make_staff.short_description = _('Grant staff permissions')
    
    def remove_staff(self, request, queryset):
        """Bulk action to remove staff permissions."""
        updated = queryset.update(is_staff=False)
        self.message_user(
            request,
            f'{updated} user(s) had staff permissions removed.'
        )
    remove_staff.short_description = _('Remove staff permissions')
    
    def get_queryset(self, request):
        """Optimize queryset for admin list view."""
        qs = super().get_queryset(request)
        return qs.select_related()
    
    def has_delete_permission(self, request, obj=None):
        """Restrict delete permissions for safety."""
        # Only superusers can delete users
        return request.user.is_superuser
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields readonly based on user permissions."""
        readonly_fields = ['last_login']
        
        # Non-superusers cannot modify superuser status
        if not request.user.is_superuser:
            readonly_fields.extend(['is_superuser', 'user_permissions', 'groups'])
            
        # If editing existing user, make email readonly for data integrity
        if obj:
            readonly_fields.append('email')
            
        return readonly_fields
