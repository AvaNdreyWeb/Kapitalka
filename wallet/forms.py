from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Profile
from django.contrib.auth.models import User


class MyAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username','password']

    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'логин'})
        self.fields['username'].label = False
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder':'пароль'}) 
        self.fields['password'].label = False


class CreateUserForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'электронная почта'})
    )
    login = forms.CharField(
        min_length=4,
        max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'логин'})
    )
    password = forms.CharField(
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'пароль'}
        )
    )
    repeat = forms.CharField(
        min_length=8,
        max_length=20,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'повторите пароль'}
        )
    )
    agree = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'rules'})
    )

    def clean_login(self):
        data = self.cleaned_data["login"]

        profiles = Profile.objects.all()
        slugs = [profile.slug for profile in profiles]
        if data in slugs:
            raise ValidationError('Данный логин уже занят.')

        return data

    def clean_repeat(self):
        data = self.cleaned_data["repeat"]
        check = self.cleaned_data["password"]

        if data != check:
            raise ValidationError('Пароли не совпадают.')

        return data

    def clean_agree(self):
        data = self.cleaned_data["agree"]
        if not data:
            raise ValidationError(
                'Необходимо принять условия пользовательского соглашения.'
            )

        return data


class CreateGroupForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
            attrs={
                "placeholder": "Название",
            }
        ),
        min_length=1,
        max_length=50
    )
    members = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'disabled': True,
                'class': 'member-list',
                'placeholder': '@UserName1\n@UserName2\n...'
            }
        )
    )

    def clean_members(self):
        data = self.cleaned_data["members"].split()
        # data = list(set(data))
        all_slugs = [profile.slug for profile in Profile.objects.all()]
        i = 0
        while i < len(data):
            slug = data[i][1:]
            if not (slug in all_slugs):
                data.pop(i)
            else:
                data[i] = slug
                i += 1

        return data


class CreateUserWalletOperationForm(forms.Form):
    is_income = forms.BooleanField(required=False, label='Пополнение', widget=forms.CheckboxInput(attrs={'class': 'rules'}))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Название"}))
    value = forms.FloatField(widget=forms.NumberInput(attrs={"class": "sum", "placeholder": "Сумма"}))
    currency = forms.CharField(max_length=10, widget=forms.TextInput(attrs={"type": "hidden", "value": "RUB"}))
    #currency = forms.CharField(max_length=10, widget=forms.TextInput(attrs={"type": "hidden", "value": "RUB", "class": "hidden-cur-code"}))
    date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'operation-date'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Описание"}), required=False)


class CreateGroupWalletOperationForm(forms.Form):
    is_income = forms.BooleanField(required=False, label='Пополнение', widget=forms.CheckboxInput(attrs={'class': 'rules'}))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Название"}))
    value = forms.FloatField(widget=forms.NumberInput(attrs={"class": "sum", "placeholder": "Сумма"}))
    currency = forms.CharField(max_length=10, widget=forms.TextInput(attrs={"type": "hidden", "value": "RUB", "class": "hidden-cur-code"}))
    date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'operation-date'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Описание"}), required=False)
    depositor = forms.ModelChoiceField(label='Заплатил:', queryset=Profile.objects.all())
    benefitors = forms.ModelMultipleChoiceField(label='Будут должны:', queryset=Profile.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select-mult'}))

    def clean_benifitors(self):
        data = self.cleaned_data["benefitors"]
        print(data)

        return data


class CreateNewDebt(forms.Form):
    debtor = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Пользователь"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Описание"}), required=False)
    value = forms.FloatField(widget=forms.NumberInput(attrs={"class": "sum", "placeholder": "Сумма"}))
    currency = forms.CharField(max_length=10, widget=forms.TextInput(attrs={"type": "hidden", "value": "RUB"}))
    is_income = forms.BooleanField(required=False, initial=True, label='Даю взаймы', widget=forms.CheckboxInput(attrs={'class': 'rules'}))

    def clean_debtor(self):
        data = self.cleaned_data["debtor"]
        if data[0] == '@':
            return data[1:]

        return data
