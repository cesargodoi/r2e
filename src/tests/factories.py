import random
import factory

from faker import Faker
from apps.accounts.models import CustomUser
from apps.center.models import Center
from apps.event.models import Activity
from apps.register.models import BankFlag


fake = Faker("pt_BR")
get_gender = random.choice(["M", "F"])


#  User
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = fake.email()
    is_staff = True


#  Center
class CenterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Center

    name = f"Center {fake.pyint(min_value=1, max_value=100)}"
    short_name = f"C-{name.split()[1]}"
    city = fake.city()
    state = fake.estado_sigla()
    country = fake.current_country_code()
    email = fake.email()
    phone = fake.phone_number()

    @factory.post_generation
    def contact(self, create, extracted, **kwargs):
        """contact is a many-to-many field"""
        self.contact.add(UserFactory(email=fake.email()))


#  Activity
class ActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Activity

    name = f"Activity {fake.pyint(min_value=1, max_value=9)}"
    activity_type = "CNF"


#  BankFlags
class BankflagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BankFlag

    name = f"BankFlag {fake.pyint(min_value=1, max_value=9)}"


# #  PayTypes
# class PaytypeFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = PayTypes

#     name = f"PayType {fake.pyint(min_value=1, max_value=9)}"
#     pay_type = random.choice([pt[0] for pt in PAY_TYPES])
