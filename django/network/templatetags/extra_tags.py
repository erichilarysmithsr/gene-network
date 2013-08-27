from django import template
from pprint import pformat
from pprint import pprint as pp
from django.template.defaultfilters import linebreaksbr
from django.utils.html import escape
register = template.Library()

try:
	from django.utils.safestring import mark_safe
except ImportError: # v0.96 and 0.97-pre-autoescaping compat
	def mark_safe(x): return x

@register.filter    
def subtract(value, arg):
	try:
		return int(value) - int(arg)
	except:
		return 0

register.filter('subtract',subtract)


@register.filter()
def highlight(value, word):
	try:
		replace = re.compile(re.escape(word), re.IGNORECASE)
		return  replace.sub("<span class='label label-info'>" + str(word) + "</span>", str(value))
	except:
		return value

register.filter('highlight',highlight)


@register.filter()
def v(value):
	""" Convenience function for printing out variable and properties """
	if hasattr(value, '__dict__'):
		d = {
			'__str__':str(value),
			'__unicode__':unicode(value),
			'__repr__':repr(value),
		}
		d.update(value.__dict__)
		value = d
	output = pformat(value)+'\n'
	return mark_safe("<pre>" + output + "</pre>")
register.filter('v',v)


@register.filter()
def in_array(value, term):
	try:
		return unicode(term) in map('unicode',value)
	except:
		return

register.filter('in_array',in_array)

@register.filter()
def tdict(value, term):
	""" A dictionary that can return a value within a template. """
	try:
		return value[term]
	except:
		return None

@register.filter(is_safe=True)
def to_ul(value):
	 return "<ul><li>" + "</li><li>".join(value.split(",")) + "</li></ul>"

register.filter('to_ul',to_ul)
