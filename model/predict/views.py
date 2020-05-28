from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .apps import PredictConfig
import numpy as np
import pandas as pd
import tldextract

def extract_domain_subdomain(record):
    domain = record
    ret=''
    try:
        ext = tldextract.extract(domain)
        ret = ext.domain
    except :
        print(record)
    return ret


VALID_CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789-_.'
LOOKUP_TABLE = None


def pad(l, content, width):
    l.extend([content] * (width - len(l)))
    return l


def check_validchar(domain):
    for c in domain.lower():
        if c not in VALID_CHARS:
            return False
    return True


def features_extract(domain):
    global VALID_CHARS
    global LOOKUP_TABLE
    if not LOOKUP_TABLE:
        LOOKUP_TABLE = dict()
        idx = 1
        for c in VALID_CHARS:
            LOOKUP_TABLE[c] = int(idx)
            idx += int(1)
            # ds = tldextract.extract(fqdn)
    # domain = ds.domain
    ratio = len(set(domain)) / len(domain)

    rvalue = list()
    if len(domain) <= 63:
        for c in domain.lower():
            try:
                rvalue.append(LOOKUP_TABLE[c])
            except:
                print(f"Char error out in {domain}: {c}")
    else:
        # print(domain)
        pass

    rvalue = pad(rvalue, 0, 63)
    return rvalue + [ratio]

class call_model(APIView):

    def get(self, request):
        if request.method == 'GET':
            # sentence is the query we want to get the prediction for
            domain = request.GET.get('fqdn')

            features = [features_extract(extract_domain_subdomain(domain))]
            # feature needs to be passed as numpy array. same should be used for training.
            response = PredictConfig.ml.predict(np.array(features))
            print(response[0])

            # returning JSON response
            return JsonResponse({'prediction': float(response[0])})