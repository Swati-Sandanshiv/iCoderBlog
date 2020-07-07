from django.shortcuts import render, HttpResponse, redirect
from .models import Post,BlogComment
from django.contrib import messages # To flash message as we comment successfully.
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts':allPosts}
    return render(request, 'blog/blogHome.html',context)
    # return HttpResponse('This is blogHome')

# Whatever we write in '<str:slug>' we get that in 'slug' variable.
def blogPost(request, slug):
    # To view content of our each post on click of 'continue reading'.
    post = Post.objects.filter(slug=slug).first()
    # Along with posts we also Bring comments on our blogPost with respect to 'post' of BlogComment Model.
    comments = BlogComment.objects.filter(post=post, parent=None) # If parent is None only comments will be seen and not the replies.
    # Here we pull replies to see below its corresponding comment. 
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    # print(comments, replies)
    # print(replyDict)
    context = {'post':post, 'comments':comments, 'user': request.user,'replyDict': replyDict}
    return render(request, 'blog/blogPost.html',context)
    # return HttpResponse(f'This is blogPost: {slug}')

def postComment(request):
    if request.method == 'POST':
        # sno and timestamp are automatic.
        # comment, postSno we going to get from 'blogPost' template using form.
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")

        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f"/blog/{post.slug}")