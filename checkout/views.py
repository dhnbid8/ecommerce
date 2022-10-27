from django.shortcuts import render
import logging
from django.http import Http404, HttpResponse
from rest_framework.decorators import api_view
from card.models import Card
from rest_framework.response import Response

from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException

from account.models import Profile
from order.models import Order
@api_view(["POST"])
def go_to_gateway_view(request):

    profile = Profile.objects.get(user=request.user) if Profile.objects.filter(user=request.user) else Profile.objects.create(user=request.user) 
    
    if profile.name:
        name = profile.name
    elif request.data['name']:
        name = request.data['name']
    else :
        return Response({"message":"نام نمی تواند خالی باشد"})

    if profile.phonenumber:
        phonenumber = profile.phonenumber
    elif  request.data['phonenumber'] :
        phonenumber = request.data['phonenumber']
    else :
        return Response({"message":"شماره تلفن نمی تواند خالی باشد"})

    if profile.address:
        address = profile.address
    elif request.data['address']:
        address = request.data['address']
    else :
        return Response({"message":"آدرس نمی تواند خالی باشد"})

    if profile.zipcode:
        zipcode = profile.zipcode
    elif request.data['zipcode']:
        zipcode = request.data['zipcode']
    else :
        return Response({"message":"کدپستی نمی تواند خالی باشد"})


    card = Card.objects.filter(user=request.user).first() if Card.objects.filter(user=request.user).count() > 0 else Card.objects.create(user=request.user).save()
    amount = card.get_items_price() * 10
    if amount == 0 or card.items.all().count() == 0 :
        return Response({"message":"سبد خرید شما خالی است "})

        
    factory = bankfactories.BankFactory()
    try:
        bank = factory.create(bank_models.BankType.IDPAY) 
        bank.set_request(request)
        bank.set_amount(amount)

        bank.set_client_callback_url(reverse('callback-gateway'))
    
        bank_record = bank.ready()
        card.convert_to_order(name, address, phonenumber, zipcode)
        
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
        
    except AZBankGatewaysException as e:
        logging.critical(e)
        return Response({"message":"خطای غیر منتظره ای رخ داد لطفا دوباره امتحان کنید !"})
        raise e

def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        
        # card = Card.objects.filter(user=request.user).first() if Card.objects.filter(user=request.user).count() > 0 else Card.objects.create(user=request.user).save()
        order = Order.objects.filter(user=request.user, status="PP").first()
        if order :
            order.status = "PE"
            order.save()
            return HttpResponse('{"message":"پرداخت با موفقیت انجام شد و سفارش شما با موفقیت  ثبت شد"}')
        else:
            return HttpResponse('{"message":"پرداخت با موفقیت انجام اما مشکلی در ثبت سفارش به وجود اومده لطفا با پشتیبانی تماس بگیرید"}')
            


    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")