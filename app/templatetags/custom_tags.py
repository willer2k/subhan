import os

from django import template
from django.db import models
from django.utils.safestring import mark_safe

from app.models import Signal

register = template.Library()


@register.simple_tag
def get_signal(ticker, interval):

	titles = Signal.objects.filter(
		ticker=ticker, interval=interval).values('title').annotate(n=models.Count("pk"))
	result = ""
	for title in titles:
		signal = Signal.objects.filter(
			ticker=ticker,
			interval=interval,
			title=title['title']).order_by('-timestamp').first()
		if signal:
			extra_style = ""
			if signal.bullish:
				extra_style = "color:MediumSeaGreen;"
			elif signal.bearish:
				extra_style = "color:Tomato;"
			result += f'<div class="collapse{ticker} collapse show" ' \
					  f'style="' \
					  f'border-style: solid; ' \
					  f'border-width: 1px; ' \
					  f'padding: 5px; ' \
					  f'margin-bottom: 7px; ' \
					  f'{extra_style}">'
			result += f"<span><bold>{signal.title}</bold><span><br><br>"
			result += f"<span>{signal.timestamp.date()}<span><br>"
			result += f"<span>{signal.timestamp.strftime('%H:%M:%S')}<span><br>"
			result += f"<span>Price: {signal.price}<span><br>"
			result += f"""
			<form method="post">
			<input type="hidden" id="signal-pk" name="signal-pk" value="{signal.pk}">
			<textarea id="comment" name="comment">{signal.comment}</textarea><br>
			  <input type="submit" value="Save">
			</form>
			"""

			result += "</div>"
	return mark_safe(result)
