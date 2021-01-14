from apps.shop.comparelist import CompareList


def compare(request):
    compare_list = CompareList(request)
    return {'comparelist_len' : len(list(compare_list))}