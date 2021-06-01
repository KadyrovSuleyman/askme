from app.models import *
from django.db.models import Count


def pt(request):
    popular_tags = ['perl', 'python', 'TechnoPark', 'MySQL', 'django', 'Mail.Ru', 'Voloshin', 'Firefox']

    t = Tag.objects.all().annotate(count = Count('question')).order_by('-count')

    if t.count() > 14:
      popular_tags = [t[0].name, t[1].name, t[2].name, t[3].name,t[4].name,t[5].name, t[6].name, t[7].name, t[8].name, t[9].name, t[10].name, t[11].name,t[12].name,t[13].name]
 
    return {"popular_tags":popular_tags}
