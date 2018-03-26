from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime, localtime
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'full_stack_app/index.html')

def process_all_info(request):
    book_exist = Book.objects.filter(title = request.POST['title'])
    
    print "Values from input", request.POST
    errors = {}
    # errors = Author.objects.basic_validator(request.POST)
   
    errors = Book.objects.basic_validator(request.POST)

    if len(errors)==0:
        if len(book_exist) == 0 :
            # we assume if no author is given, default o drop down value
            if len(request.POST['author']) == 0 : 
                a = Author.objects.get(name = request.POST['authorDropDown'])
            # create a new author
            else:
                # if the author is already in the list, tell the user to start from scratch    
                a = Author.objects.create(name = request.POST['author'])
                a.save()
        
            b = Book.objects.create(title=request.POST['title'], author = a)
            b.save()
        # if the book exists, we don't create a new reord
        else:
            b = Book.objects.get(title = request.POST['title'])
        
        u = User.objects.get(id=request.session['id'])
        r = Review.objects.create(rating = request.POST['rating'], content=request.POST['review'], user=u, book=b)
        r.save()
        return redirect('/books/'+ str(b.id))
    else:
        print "ERROR FOUND"
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
       
    return redirect('/books/add')

def display_book_reviews(request, id):    
    if 'login' not in request.session:
        return redirect('/')
    if request.session['login']==False:
        return redirect('/')

    b = Book.objects.filter(id=id)
    data = {
        'book': b[0],
        'reviews':Review.objects.filter(book_id=id)
    }
    return render(request, 'full_stack_app/display_book_reviews.html', data)

def display_user(request, id):
    if 'login' not in request.session:
        return redirect('/')
    if request.session['login']==False:
        return redirect('/')

    data = {
        'reviews': Review.objects.filter(user_id=id),
        'user': User.objects.get(id=id),
        'count': len(Review.objects.filter(user_id=id)),
    }
    return render(request, 'full_stack_app/display_user.html', data)

def delete_review(request, id):
    # retrieve all books associated with the same review id
    # if only book, delete the review and book
    book_id = Review.objects.get(id=id).book_id
    Review.objects.get(id=id).delete()
    return redirect('/books/'+str(book_id))


def add_user(request):
    errors = User.objects.basic_validator(request.POST)
    print "FROM USER", request.POST
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
    else: 
        myrequest = request.POST

        # need to Bcrypt our password
        hash1 = bcrypt.hashpw( myrequest['pw'].encode('utf8') , bcrypt.gensalt())
        user = User.objects.create(first_name=myrequest['first_name'], last_name=myrequest['last_name'], email=myrequest['email'], pw=hash1 )
        user.save()
    return redirect('/')

def books_dashboard(request):
    if 'login' not in request.session:
        return redirect('/')
    if request.session['login']==False:
        return redirect('/')
    print 'go to dashboard'
    data = {
        'reviews': Review.objects.all().order_by('-created_at')[:3],
        'books': Book.objects.all()
    }
    return render(request, 'full_stack_app/dashboard.html', data)

def books_add_dashboard(request):
    if 'login' not in request.session:
        return redirect('/')
    if request.session['login']==False:
        return redirect('/')
    
    data = {'authors': Author.objects.all()}

    return render(request, 'full_stack_app/add_book.html', data)

def login(request):
    if request.method == 'POST':
        myrequest = request.POST
        user = User.objects.filter(email=myrequest['email'])
        # if record not found
        if len(user) == 0:
            errors = {}
            errors['email_not_found'] = 'Email not found in our records'
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            # password on file
            hashed_pw = user[0].pw
            if bcrypt.checkpw( myrequest['pw'].encode('utf8'), hashed_pw.encode('utf8') )  :
                request.session['first_name']= user[0].first_name
                request.session['last_name']= user[0].last_name
                request.session['id'] = user[0].id
                request.session['login'] = True
                return redirect('/books')
            else:
                errors = {}
                errors['password_no_match'] = "Password doesn't match our records. Incorrect password."
                for tag, error in errors.iteritems():
                    messages.error(request, error, extra_tags=tag)

    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')