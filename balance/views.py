from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Company_info, Company, History_info
from .parser import get_all
import time


def get_balance(request):
    companies = Company.objects.all()
    get_all(companies)
    return redirect('balance:balance')

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def balance(request):
    #companies = Company.objects.all()
    companies = Company.objects.all().order_by("name")
    date = companies[0].company_info.updated.strftime('%d.%m.%y')
    return render(request, 'balance/balance.html', {'companies': companies, 'date': date})

def line_chart(request, key):
    companies = Company.objects.all().order_by("name")
    date = companies[0].company_info.updated.strftime('%d.%m.%y')

    company= get_object_or_404(Company, pk=key)
    labels = []
    data = []

    # история компании за текущий месяц
    queryset = History_info.objects.filter(company_key=company.key).filter(published_date__month=time.strftime('%m'))
    for q in queryset:
        labels.append(q.published_date.strftime('%d'))
        data.append(q.expenses)
    return render(request, 'balance/line_chart.html', {
        'company': company,
        'labels': labels,
        'data': data,

        'companies': companies,
        'date': date,

    })
