from abc import ABC, abstractmethod 
from user.models import CustomUser, OneTimePassword
from orders.models import Address
from django.contrib.auth import authenticate
from datetime import timedelta
from django.utils import timezone
from django.db.models import Prefetch

class IUserRepository(ABC):
    @abstractmethod
    def create_user(self):
        pass
    
    @abstractmethod
    def get_user(self):
        pass            
    
    @abstractmethod
    def delete_user(self):
        pass
    
    @abstractmethod
    def update_user(self):
        pass
    
    @abstractmethod
    def is_email_free(self):
        pass
    
class UserRepository(IUserRepository):
    
    def create_user(self, email, first_name, last_name, phone_number ):
        return CustomUser.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,  
            is_staff = False,
            is_superuser = False,                    
        )
    
    def get_user(self, email):
        try:
            unique_addresses_qs = Address.objects.order_by('address').distinct('address')
            return CustomUser.objects.prefetch_related(
                Prefetch('addresses', queryset=unique_addresses_qs),
            ).get(email=email)
        except CustomUser.DoesNotExist:
            return None
         

    
    def delete_user(self, email):
        user = CustomUser.objects.get(email=email)
        user.is_active = False
        user.save()
        
        
    def update_user(self, user, data):
        fields_to_update = ['first_name', 'last_name', 'phone_number']
        for field in fields_to_update:
            setattr(user, field, data.get(field, getattr(user, field)))    
        user.save()
        
    def is_email_free(self, email):
        return not CustomUser.objects.filter(email=email).exists()
    
    def is_phone_free(self, phone):
        return not CustomUser.objects.filter(phone_number=phone).exists()
        
        
        
class TemporaryPasswordRepository:
    def create_temporary_password(self, user, password):
        expiration_time = timezone.now() + timedelta(hours=1)
        temp_password = OneTimePassword(user=user, code=password, expiration_time=expiration_time)        
        temp_password.save()
        return temp_password

    def get_valid_temporary_password(self, user):
        try:
            temp_password = OneTimePassword.objects.filter(user=user).latest('created_at')
            if temp_password.is_valid():
                return temp_password
            else:
                temp_password.delete()
                return None
        except OneTimePassword.DoesNotExist:
            return None
       