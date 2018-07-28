import geocoder
from time import sleep

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import *
from .forms import *

STATE_DICT = {
    '01': 'AL',
    '02': 'AK',
    '04': 'AZ',
    '05': 'AR',
    '06': 'CA',
    '08': 'CO',
    '09': 'CT',
    '10': 'DE',
    '11': 'DC',
    '12': 'FL',
    '13': 'GA',
    '15': 'HI',
    '16': 'ID',
    '17': 'IL',
    '18': 'IN',
    '19': 'IA',
    '20': 'KS',
    '21': 'KY',
    '22': 'LA',
    '23': 'ME',
    '24': 'MD',
    '25': 'MA',
    '26': 'MI',
    '27': 'MN',
    '28': 'MS',
    '29': 'MO',
    '30': 'MT',
    '31': 'NE',
    '32': 'NV',
    '33': 'NH',
    '34': 'NJ',
    '35': 'NM',
    '36': 'NY',
    '37': 'NC',
    '38': 'ND',
    '39': 'OH',
    '40': 'OK',
    '41': 'OR',
    '42': 'PA',
    '44': 'RI',
    '45': 'SC',
    '46': 'SD',
    '47': 'TN',
    '48': 'TX',
    '49': 'UT',
    '50': 'VT',
    '51': 'VA',
    '53': 'WA',
    '54': 'WV',
    '55': 'WI',
    '56': 'WY',
    '60': 'AS',
    '66': 'GU',
    '69': 'MP',
    '72': 'PR',
    '78': 'VI',
    '74': 'UM',
    '64': 'FM',
    '68': 'MH',
    '70': 'PW'
}

def index(request):
    issue = Issue.objects.first()
    return render(request, 'onboarding.html', locals())

@csrf_exempt
def question_confirm(request):
    answer_ = {
        'issue': Issue.objects.first(),
        'questions': ','.join(request.POST.getlist('answer[]'))
    }

    VoterResponse.objects.create(**answer_)
    return HttpResponse('success')

@csrf_exempt
def address_confirm(request):
    latlon = []
    polygon = []
    # issue = Issue.objects.first()

    address = request.POST.get('address', '')
    trial = 3

    while trial > 0:
        sleep(0.05)
        try:
            g = geocoder.google(address)
            latlon = g.geojson['features'][0]['geometry']['coordinates']
            break
        except (RuntimeError, ValueError, TypeError, Exception):
            trial = trial - 1

    if latlon:
        point = 'POINT({} {})'.format(latlon[0], latlon[1])
        congress_district = District.objects.filter(boundary__contains=point).first()

        # update answer with the district
        qas = VoterResponse.objects.all().last()
        qas.district = congress_district
        qas.save()

        polygon = congress_district.get_polygon_lst()
        st_dis = STATE_DICT[congress_district.statefp] + congress_district.districtid if congress_district else ''
        repr = Representative.objects.filter(st_dis_115=st_dis).first()

        return JsonResponse({
            'location': [latlon[1], latlon[0]],
            'rep_name': '{} {}'.format(repr.first_name, repr.last_name),
            'polygon': polygon
        }, safe=False)

    return HttpResponse('fail')

@csrf_exempt
def chart_data(request):
    count = VoterResponse.objects.all().count()

    result = {
        'count': count,
        'selected': [0, 0, 0, 0, 0]
    }
    
    for ii in VoterResponse.objects.all():
        qs = ii.questions.split(',')
        for jj in range(6):
            result['selected'][jj-1] += qs.count(str(jj))

    return JsonResponse(result, safe=True)

@csrf_exempt
def save_email(request):
    email = request.POST.get('email')
    try:
        Email.objects.create(email=email)
    except Exception as e:
        pass

    return HttpResponse('')
