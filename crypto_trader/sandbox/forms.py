from django  import forms
from .models import Member


class MemberUpdateForm(forms.ModelForm):
    # Form for updating members
    class Meta:
        model  = Member
        fields = ('first_name', 'last_name', 'phone',)

