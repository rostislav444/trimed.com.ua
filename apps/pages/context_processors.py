from apps.pages.models import PageGroup


def static_pages(request):
    return {'page_groups' : PageGroup.objects.all() }
