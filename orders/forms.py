from django import forms
from orders.models import ShippingAddress

# Create your tests here.
# dev_25
class ShippingForm(forms.ModelsForm):
    class Meta:
        model = ShippingAddress
        fields = "__all__"
        exclude = ["user"]
