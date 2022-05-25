from django.contrib.auth.decorators import user_passes_test
from django.core.checks import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Store
import requests
from Moirant.settings import DEBUG
from .forms import AddItem
import json

from trendyol_sdk.api import TrendyolApi
from trendyol_sdk.services import ProductIntegrationService


trendyol_url = "https://stageapi.trendyol.com/stagesapigw/" if DEBUG else "https://api.trendyol.com/sapigw/"
hepsiburada_url = "https://mpop-sit.hepsiburada.com/product/api/" if DEBUG else "https://mpop.hepsiburada.com/product/api/"
gittigidiyor_url = ""


@user_passes_test(lambda usr: usr.auth_level >= 2)
def store(request: str) -> HttpResponse:
    stores = Store.objects.order_by('-name')

    context = {
        'stores': stores,
    }

    return render(request, "stores/stores.html", context)


@user_passes_test(lambda usr: usr.auth_level >= 2)
def store_detail(request: str, name) -> HttpResponse:

    """ NOTE: trendyol has its own api python package, which i
        installed, but seeing we will be adding a lot more and it
        needs to be scalable i scrapped that. Many popular store
        fronts probably has a similar API package but better
        stick with our own API calls for now.


        Here is an example:
        api = TrendyolApi(api_key="<TRENDYOL_API_KEY>", api_secret="<TRENDYOL_API_SECRET>", supplier_id="<TRENDYOL_SELLER_ID>")
        service = ProductIntegrationService(api)
        products = service.get_products()
    """

    # Get our own information
    current_store = Store.objects.get(name=name)

    # request url     Dummy link provided by trendyol                        Actual link we need to use
    base_url = trendyol_url if current_store.store_id == 1 else hepsiburada_url if current_store.store_id == 2 else "ERR"

    if base_url == "ERR":
        return render(request, "stores/store_detail.html", {'error': True})

    # Optional stuff we can pass to trendyol requests.
    filter_params = {}

    params = {
        "approved": filter_params.get("approved", ""),
        "barcode": filter_params.get("barcode", ""),
        "startDate": filter_params.get("startDate", ""),
        "endDate": filter_params.get("endDate", ""),
        "page": filter_params.get("page", ""),
        "dateQueryType": filter_params.get("dateQueryType", ""),
        "size": filter_params.get("size", "")
    }

    # The actual request from trendyol.
    response = requests.get(
        "{}suppliers/{}/products".format(base_url, current_store.seller_id),
        params=params,
        headers=None,
        files=None
    )

    # Check results and redirect on error code.
    if response.status_code == 200:
        items = response.json()
        item_amount = [index for index, _ in enumerate(items["product"])]
    else:
        items, item_amount = None, None
        # return render(request, "stores/store_detail.html", {'error': True})

    context = {
        'items': items,
        'store': current_store,
        'amount': item_amount
    }

    return render(request, "stores/store_detail.html", context)


@user_passes_test(lambda usr: usr.auth_level >= 2)
def add_product_to_store(request: str, name) -> HttpResponse:
    current_store = Store.objects.get(name=name)

    context = {
        'store': current_store,
    }

    if request.method == "POST":
        new_item = AddItem(request.POST)
        if new_item.is_valid():
            params = {
                "items": new_item
            }
            match current_store.store_id:
                case 1:
                    response = requests.post("{}/suppliers/{}/products".format(trendyol_url, current_store.seller_id),
                                             params=params
                                             )
                case 2:
                    response = requests.post(
                        "{}/categories/get-all-categories?leaf=true&status=ACTIVE&available=true&page=0&size=1000&version=1".format(hepsiburada_url),
                        params=params
                    )
                case 3:
                    response = requests.post("{}".format(trendyol_url))

            if response.status_code == 200:
                messages.add_message(request, messages.INFO, "Ürün başarıyla oluşturulmuştur!")
                return redirect('/stores/{}'.format(name))
            else:
                return render(request, "stores/add_item.html".format(name), (context | {'error': new_item}))
        else:
            return render(request, "stores/add_item.html".format(name), (context | {'error': new_item}))
    else:
        return render(request, "stores/add_item.html", context)
