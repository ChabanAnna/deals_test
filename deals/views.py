from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from django.shortcuts import render
from .models import Deals
from csv import DictReader
from .forms import UploadFileForm


def statistic(request):
    top_customers = Deals.objects.values('customer').annotate(total_price=Sum('total')).order_by('-total_price')[0:5]
    res = list(top_customers)
    top_customers_names = [c['customer'] for c in res]
    j = 0
    for current in top_customers:
        res[j]['items'] = list(Deals.objects.filter(customer__exact=current['customer']).values_list('item', flat=True).distinct())
        j += 1
    for i in range(len(res)):
        new_items = list()
        for cur in res[i]['items']:
            is_two = False
            for other in range(len(res)):
                if other != i and cur in res[other]['items']:
                    is_two = True
            if is_two:
                new_items.append(cur)
        res[i]['items'] = new_items
    return JsonResponse({'response': res})


def loader(request):
    if request.method == "POST":
        if 'deals_file' in request.FILES:
            form = DictReader(request.FILES['deals_file'].read().decode('utf-8').split('\n'))
            mas_deals = []
            errors = []
            i = 0
            for line in form:
                inst_deals = Deals(customer=line['customer'], date=line['date'], quantity=line['quantity'],
                                    total=line['total'], item=line['item'])
                try:
                    inst_deals.clean_fields()
                except ValidationError as e:
                    errors.append(str(i) + ': ' + e.__str__())
                i += 1
                mas_deals.append(inst_deals)
            if len(errors) > 0:
                return JsonResponse({'Status': 'Error', 'Desc': 'Ошибка обработки строк: '+str(errors)})
            for item in mas_deals:
                item.save()
            return JsonResponse({'Status': 'ОК'})
        else:
            return JsonResponse({'Status': 'Error', 'Desc': 'Файл не выбран'})
    else:
        return render(request, "deals/post_form.html")

