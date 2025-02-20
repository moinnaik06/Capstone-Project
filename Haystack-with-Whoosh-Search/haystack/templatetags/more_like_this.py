from __future__ import unicode_literals
from django import template
from django.db import models
from haystack.query import SearchQuerySet


register = template.Library()


class MoreLikeThisNode(template.Node):
    def __init__(self, model, varname, for_types=None, limit=None):
        self.model = template.Variable(model)
        self.varname = varname
        self.for_types = for_types
        self.limit = limit

        if not self.limit is None:
            self.limit = int(self.limit)

    def render(self, context):
        try:
            model_instance = self.model.resolve(context)
            sqs = SearchQuerySet()

            if not self.for_types is None:
                intermediate = template.Variable(self.for_types)
                for_types = intermediate.resolve(context).split(',')
                search_models = []

                for model in for_types:
                    model_class = models.get_model(*model.split('.'))

                    if model_class:
                        search_models.append(model_class)

                sqs = sqs.models(*search_models)

            sqs = sqs.more_like_this(model_instance)

            if not self.limit is None:
                sqs = sqs[:self.limit]

            context[self.varname] = sqs
        except:
            pass

        return ''


@register.tag
def more_like_this(parser, token):

    bits = token.split_contents()

    if not len(bits) in (4, 6, 8):
        raise template.TemplateSyntaxError(u"'%s' tag requires either 3, 5 or 7 arguments." % bits[0])

    model = bits[1]

    if bits[2] != 'as':
        raise template.TemplateSyntaxError(u"'%s' tag's second argument should be 'as'." % bits[0])

    varname = bits[3]
    limit = None
    for_types = None

    if len(bits) == 6:
        if bits[4] != 'limit' and bits[4] != 'for':
            raise template.TemplateSyntaxError(u"'%s' tag's fourth argument should be either 'limit' or 'for'." % bits[0])

        if bits[4] == 'limit':
            limit = bits[5]
        else:
            for_types = bits[5]

    if len(bits) == 8:
        if bits[4] != 'for':
            raise template.TemplateSyntaxError(u"'%s' tag's fourth argument should be 'for'." % bits[0])

        for_types = bits[5]

        if bits[6] != 'limit':
            raise template.TemplateSyntaxError(u"'%s' tag's sixth argument should be 'limit'." % bits[0])

        limit = bits[7]

    return MoreLikeThisNode(model, varname, for_types, limit)
