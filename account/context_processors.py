from .models import InspirationalQuotes
from .models import Affirmations


def get_quotes(request):
    # quote1 = InspirationalQuotes.objects.all()
    # b = ""
    # for a in quote1:
    #     b = b + "     " + "   " + a.quote
    #     print(b)
    return {
        'quotes': InspirationalQuotes.objects.order_by("?").all()
    }


def get_affirmations(request):
    return {
        "affirmations": Affirmations.objects.all()
    }
