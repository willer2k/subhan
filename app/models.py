from django.db import models


class Signal(models.Model):
    """
    "BULL CROSS\nSymbol: {{exchange}}:{{ticker}}:{{interval}}\nPrice: {{close}}"
    {"text": "BULL CROSS\nSymbol: FX:GBPUSD:1\nPrice: 1.37613"}
    """
    message = models.CharField(max_length=255*2, null=False, blank=False)

    title = models.CharField(max_length=255*2, null=True, blank=True, default="")
    exchange = models.CharField(max_length=255, null=True, blank=True, default="")  # FX
    ticker = models.CharField(max_length=255, null=True, blank=True, default="")  # GBPUSD
    interval = models.CharField(max_length=255, null=True, blank=True, default="")  # 1
    price = models.CharField(max_length=255, null=True, blank=True, default="")  # 1.37649

    bullish = models.BooleanField(default=False)
    bearish = models.BooleanField(default=False)
    comment = models.TextField(max_length=255*2, null=True, blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    def init_signal(self, message):
        self.message = message
        messages = message.split('\n')
        if len(messages) == 1:
            messages = message.split('\\n')

        self.title = messages[0].strip()
        self.exchange = messages[1].split(':')[1].strip()
        self.ticker = messages[1].split(':')[2].strip()
        self.interval = messages[1].split(':')[3].strip()
        self.price = messages[2].split(':')[1].strip()

        if 'bull' in self.title.lower() or 'buy' in self.title.lower():
            self.bullish = True

        if 'bear' in self.title.lower() or 'sell' in self.title.lower():
            self.bearish = True
        return self