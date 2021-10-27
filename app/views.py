from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.models import Signal
import json


class HomepageView(LoginRequiredMixin, View):
    template_name = 'index.html'
    extra_context = {'section': 'homepage'}

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):

        # GBPUSD / USDCAD /...
        tickers = []
        _tickers = Signal.objects.all().values("ticker").annotate(n=models.Count("pk"))
        for ticker in _tickers:
            tickers.append(ticker['ticker'])

        # 1 / 15 / 30 / ...
        intervals = []
        _intervals = Signal.objects.all().values("interval").annotate(n=models.Count("pk"))
        for interval in _intervals:
            intervals.append(interval['interval'])

        context = {
            'view': self,
            'tickers': sorted(tickers),
            'intervals': sorted(intervals),
        }
        kwargs.update(context)
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs

    def get(self, request):
        """Present default page'"""
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request):
        signal = Signal.objects.get(pk=request.POST['signal-pk'])
        signal.comment = request.POST['comment']
        signal.save()
        context = self.get_context_data()
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        """
        Return a TemplateResponse with the given template_name.
        Pass response_kwargs to the constructor of the response class.
        """
        return TemplateResponse(
            self.request, self.template_name, context, **response_kwargs)


class HookView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        # body = b'BULL_ CROSS\\nSymbol: FX:GBPUSD:1\\nPrice: 1.37649'
        signal = Signal().init_signal(request.body.decode('utf-8'))
        signal.save()

        with open('request.json', 'w') as fd:
            json.dump(request.POST.dict(), fd)

        return JsonResponse({
            "status": "success",
            "code": 200,}, safe=False)