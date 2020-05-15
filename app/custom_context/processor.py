from CC.models import Category
# this exists to serve the categories globally
# so the header works anywhere

CONTEXT = {
    "cat_1": Category.objects.get(pk=1),
    "cat_2": Category.objects.get(pk=3),
    "cat_3": Category.objects.get(pk=4)
}


def get_context(request):
    return {'default_context': CONTEXT}


