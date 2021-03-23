from django.shortcuts import render, redirect

def homepage(request):
    return redirect('/foods/menu')
    return render(request,'header.html')