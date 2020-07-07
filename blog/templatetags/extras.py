from django import template

register = template.Library()

@register.filter(name='get_val')
def get_val(dict, key): # 'dict'--> replyDict and 'key'--> comment.sno of 'reply for-loop' in 'blogPost.html'.
    return dict.get(key)