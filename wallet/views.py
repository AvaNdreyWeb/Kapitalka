from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Currency, Debt, Operation, Profile, Wallet
from .tools import generate_wallet_slug
from .forms import CreateUserForm, CreateGroupForm,  CreateUserWalletOperationForm, CreateGroupWalletOperationForm, CreateNewDebt


@login_required
def groups(request):
    """
    Функция отображения для списка групп.
    """
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            wallet_title = form.cleaned_data['title']
            members = form.cleaned_data['members']
            wallet_slug = generate_wallet_slug(wallet_title)
            all_wallet_slugs = [wallet.slug for wallet in Wallet.objects.all()]
            c = 0
            clean_slug = wallet_slug
            while clean_slug in all_wallet_slugs:
                clean_slug = f'{wallet_slug}{c}'
                c += 1

            new_wallet = Wallet.objects.create(
                title=wallet_title,
                slug=clean_slug,
            )

            current_profile = Profile.objects.get(user=request.user)
            new_wallet.members.add(current_profile)
            for member_slug in members:
                member = Profile.objects.get(slug=member_slug)
                new_wallet.members.add(member)

            new_wallet.save()

            return HttpResponseRedirect(reverse('groups'))
    else:
        form = CreateGroupForm()

    profile = Profile.objects.get(user=request.user)
    user_wallets = profile.wallets.all()
    group_list = []
    for group in user_wallets:
        members = group.members.all()
        count = members.count()
        if count > 1:
            names = [member.name for member in members]
            group_list.append((group, names,))

    context_data = {
        'group_list': group_list,
        'form': form,
    }
    return render(
        request,
        'groups.html',
        context=context_data
    )


@login_required
def user_wallet(request):
    """
    Функция отображения для личного кошелька.
    """
    profile = Profile.objects.get(user=request.user)
    wallet_slug = profile.slug + 'Wallet'
    wallet = Wallet.objects.get(slug=wallet_slug)
    if request.method == 'POST':
        form = CreateUserWalletOperationForm(request.POST)
        if form.is_valid():
            currency = Currency.objects.get(code=form.cleaned_data['currency'])
            new_operation = Operation.objects.create(
                name=form.cleaned_data['name'],
                value=form.cleaned_data['value'],
                is_income=form.cleaned_data['is_income'],
                currency=currency,
                description=form.cleaned_data['description'],
                date=form.cleaned_data['date'],
            )
            if form.cleaned_data['is_income']:
                new_operation.benefitors.add(profile)
            else:
                new_operation.depositor = profile

            new_operation.save()
            wallet.operations.add(new_operation)
            wallet.save()
            return HttpResponseRedirect(reverse('user_wallet'))
    else:
        form = CreateUserWalletOperationForm()

    operations = Operation.objects.all().filter(wallet=wallet)
    balance = 0
    for operation in operations:
        if operation.is_income:
            balance += operation.value
        else:
            balance -= operation.value
    wallet.balance = balance
    wallet.save()
    debt_list = Debt.objects.filter(debtor=profile)
    debt_sum = 0
    for debt in debt_list:
        debt_sum += debt.value
    credit_list = Debt.objects.filter(creditor=profile)
    credit_sum = 0
    for credit in credit_list:
        credit_sum += credit.value

    context_data = {
        'operations': operations,
        'wallet': wallet,
        'profile': profile,
        'form': form,
        'debt_sum': debt_sum,
        'credit_sum': credit_sum,
    }
    return render(
        request,
        'wallet.html',
        context=context_data
    )


@login_required
def debts(request):
    """
    Функция отображения для списка долгов.
    """
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = CreateNewDebt(request.POST)
        if form.is_valid():
            is_income = form.cleaned_data['is_income']
            creditor_debtor = Profile.objects.get(slug=form.cleaned_data['debtor'])
            if is_income:
                creditor = profile
                debtor = creditor_debtor
            else:
                debtor = profile
                creditor = creditor_debtor
            value = form.cleaned_data['value']
            description = form.cleaned_data['description']
            currency = Currency.objects.get(code=form.cleaned_data['currency'])
            new_debt = Debt.objects.create(
                is_income=is_income,
                debtor=debtor,
                creditor=creditor,
                value=value,
                currency=currency,
                description=description
            )

            exist = False
            user_credits = Debt.objects.filter(creditor=profile).exclude(id=new_debt.id)
            user_debts_credits = Debt.objects.filter(debtor=profile).exclude(id=new_debt.id).union(user_credits)
            for debt_credit in user_debts_credits:
                if new_debt.currency == debt_credit.currency:
                    state1 = (new_debt.creditor == debt_credit.creditor)
                    state2 = (new_debt.debtor == debt_credit.debtor)
                    state3 = (new_debt.debtor == debt_credit.creditor)
                    state4 = (new_debt.creditor == debt_credit.debtor)
                    if is_income:
                        if state2 or state3:
                            if state2:
                                debt_credit.value += new_debt.value
                            if state3:
                                debt_credit.value -= new_debt.value
                                if debt_credit.value < 0:
                                    debt_credit.is_income = not debt_credit.is_income
                                    debt_credit.debtor, debt_credit.creditor = debt_credit.creditor, debt_credit.debtor
                                    debt_credit.value *= -1
                                elif debt_credit.value == 0:
                                    exist = True
                                    debt_credit.delete()
                                    break
                            debt_credit.description = new_debt.description
                            debt_credit.save()
                            exist = True
                            break
                    else:
                        if state1 or state4:
                            if state1:
                                debt_credit.value += new_debt.value
                            if state4:
                                debt_credit.value -= new_debt.value
                                if debt_credit.value < 0:
                                    debt_credit.is_income = not debt_credit.is_income
                                    debt_credit.debtor, debt_credit.creditor = debt_credit.creditor, debt_credit.debtor
                                    debt_credit.value *= -1
                                elif debt_credit.value == 0:
                                    exist = True
                                    debt_credit.delete()
                                    break
                            debt_credit.description = new_debt.description
                            debt_credit.save()
                            exist = True
                            break

            if not exist:
                new_debt.save()
            else:
                new_debt.delete()

            return HttpResponseRedirect(reverse('debts'))
    else:
        form = CreateNewDebt()

    credit_list = Debt.objects.filter(debtor=profile)
    debt_list = Debt.objects.filter(creditor=profile).union(credit_list)
    context_data = {
        'form': form,
        'debt_list': debt_list,
        'profile': profile
    }
    return render(
        request,
        'debts.html',
        context=context_data
    )


@login_required
def settings(request):
    """
    Функция отображения для страницы настроек.
    """
    context_data = {}
    return render(
        request,
        'settings.html',
        context=context_data
    )


def create_user(request):
    """
    Функция отображения для страницы регистрации.
    """
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data['login']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            new_user = User.objects.create_user(login, email, password)
            new_user.save()
            new_profile = Profile.objects.create(
                user=new_user,
                name=login,
                slug=login
            )
            new_profile.save()
            wallet_title = f'Кошелёк {login}'
            wallet_slug = f'{login}Wallet'
            new_wallet = Wallet.objects.create(
                title=wallet_title,
                slug=wallet_slug,
            )
            new_wallet.members.add(new_profile)
            new_wallet.save()

            return HttpResponseRedirect(reverse('login'))
    else:
        form = CreateUserForm()

    context_data = {
        'form': form,
    }
    return render(
        request,
        'sing_up.html',
        context=context_data
    )

###############################################################################
@login_required
def group_wallet(request, slug):
    """
    Функция отображения для кошелька группы.
    """
    group = Wallet.objects.get(slug=slug)
    profile = Profile.objects.get(user=request.user)

    if not (Wallet.objects.filter(members__slug=profile.slug).count()):
        return HttpResponseRedirect(reverse('groups'))

    if request.method == 'POST':
        form = CreateGroupWalletOperationForm(request.POST)
        if form.is_valid():
            depositor = form.cleaned_data['depositor']
            currency = Currency.objects.get(code=form.cleaned_data['currency'])
            new_operation = Operation.objects.create(
                name=form.cleaned_data['name'],
                value=form.cleaned_data['value'],
                is_income=form.cleaned_data['is_income'],
                currency=currency,
                description=form.cleaned_data['description'],
                date=form.cleaned_data['date'],
                depositor=depositor,
            )
            new_operation.save()
            group.operations.add(new_operation)
            group.save()
            name = form.cleaned_data['name']
            value = form.cleaned_data['value']
            benefitors = form.cleaned_data['benefitors']
            if depositor in benefitors:
                equal_sum = round((value - value/len(benefitors))/(len(benefitors)-1),2)
                benefitors = benefitors.exclude(slug=depositor.slug)
            else:
                equal_sum = round(value/len(benefitors), 2)

            for benefitor in benefitors:

                new_debt = Debt.objects.create(
                    creditor=depositor,
                    debtor=benefitor,
                    value=equal_sum,
                    is_income=False,
                    description=f'{group.title}: {name}'
                )

                exist = False
                benefitor_credits = Debt.objects.filter(creditor=benefitor).exclude(id=new_debt.id)
                benefitor_debts_credits = Debt.objects.filter(debtor=benefitor).exclude(id=new_debt.id).union(benefitor_credits)
                for debt_credit in benefitor_debts_credits:
                    if new_debt.currency == debt_credit.currency:
                        state1 = (new_debt.creditor == debt_credit.creditor)
                        state4 = (new_debt.creditor == debt_credit.debtor)
                        
                        if state1 or state4:
                            if state1:
                                debt_credit.value += new_debt.value
                            if state4:
                                debt_credit.value -= new_debt.value
                                if debt_credit.value < 0:
                                    debt_credit.is_income = not debt_credit.is_income
                                    debt_credit.debtor, debt_credit.creditor = debt_credit.creditor, debt_credit.debtor
                                    debt_credit.value *= -1
                                elif debt_credit.value == 0:
                                    exist = True
                                    debt_credit.delete()
                                    break
                            debt_credit.description = new_debt.description
                            debt_credit.save()
                            exist = True
                            break

                if not exist:
                    new_debt.save()
                else:
                    new_debt.delete()

            
            return HttpResponseRedirect(reverse('group_wallet', kwargs={'slug': slug}))
    else:
        form = CreateGroupWalletOperationForm()

    operations = Operation.objects.all().filter(wallet=group)
    debt_sum = 0
    credit_sum = 0
    for member in group.members.all():
        debt_list = Debt.objects.filter(debtor=profile, creditor=member)
        for debt in debt_list:
            debt_sum += debt.value
        credit_list = Debt.objects.filter(creditor=profile, debtor=member)
        for credit in credit_list:
            credit_sum += credit.value

    context_data = {
        'operations': operations,
        'wallet': group,
        'profile': profile,
        'form': form,
        'debt_sum': debt_sum,
        'credit_sum': credit_sum,
    }

    return render(
        request,
        'group_wallet.html',
        context=context_data
    )
