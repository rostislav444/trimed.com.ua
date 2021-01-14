from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from apps.catalogue.models import Product
from apps.comments.models import Comment, CommentLike, CommentImages

from apps.user.models import CustomUser
from django.db.models import Q






def comment_likes(request, product_id, comment_id, like):
    redirect_page = request.GET.get('return')
   
    if request.user.is_authenticated:
        like = True if like == 'like' else False
        try:    
            comment_like = CommentLike.objects.get(user=request.user, parent__pk=int(comment_id))
        except: 
            comment = Comment.objects.get(pk=int(comment_id))
            comment_like = CommentLike(user=request.user, parent=comment)
        comment_like.like = like
      
        comment_like.save()
    if redirect_page:
        return redirect(redirect_page)
    return redirect(request.META.get('HTTP_REFERER'))