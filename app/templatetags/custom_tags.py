import os
from pytz import timezone

from django import template
from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe

from app.models import Signal

register = template.Library()


@register.simple_tag
def get_signal(ticker, interval):

	titles = Signal.objects.filter(
		ticker=ticker, interval=interval).values('title').annotate(n=models.Count("pk"))
	result = ""
	titles = [title['title'] for title in titles]

	def rank_title(_title):
		if 'buy' in _title.lower() or 'bull' in _title.lower():
			return 0
		if 'sell' in _title.lower() or 'bear' in _title.lower():
			return 1
		else:
			return 2

	for title in sorted(titles, key=lambda x: (rank_title(x), x)):
		signal = Signal.objects.filter(
			ticker=ticker,
			interval=interval,
			title=title).order_by('-timestamp').first()
		settings_time_zone = timezone(settings.TIME_ZONE)
		timestamp = signal.timestamp.astimezone(settings_time_zone)
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
			result += f"<span>{timestamp.date()}<span><br>"
			result += f"<span>{timestamp.strftime('%H:%M:%S')}<span><br>"
			result += f"<span>Price: {signal.price[:7]}<span><br>"
			result += f"""
			<form method="post">
			<input type="hidden" id="signal-pk" name="signal-pk" value="{signal.pk}">
			<textarea id="comment" name="comment">{signal.comment}</textarea><br>
			  <input type="submit" value="Save">
			</form>
			"""

			result += "</div>"
	return mark_safe(result)
