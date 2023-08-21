from django.shortcuts import render, redirect
from django.http import HttpResponse
from crud_function_based.models import Customer

# Create your views here.
def list(request):
	customer = Customer.objects.all()
	context = {
        'customers': customer,
        'empl': "sdg"
    }
	return render(request,"crud_function_based/index.html",context)
	# return render(request, 'crud_function_based/index.html')

def create(request):
	return render(request, 'crud_function_based/add.html')

def store(request):
	if request.method == 'POST':
		first_name = request.POST.get('first_name', '').strip()
		last_name = request.POST.get('last_name', '').strip()
		email = request.POST.get('email', '').strip()
		user_name = request.POST.get('user_name', '').strip()
		phone_number = request.POST.get('phone_number', '').strip()
		gender = request.POST.get('gender', '').strip()
		dof = request.POST.get('dof', '').strip()
		age = request.POST.get('age', '').strip()
		country = request.POST.get('business', '').strip()
		city = request.POST.get('city', '').strip()
		message = request.POST.get('message', '').strip()

        # Create an instance of YourModel with cleaned data
		save_data = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            user_name=user_name,
            phone_number=phone_number,
            gender=gender,
            dof=dof,
            age=age,
            country=country,
            city=city,
            message=message,
        )

        # Save the data to the database
		save_data.save()
		return redirect('/')  # Redirect to a success page or any other URL after saving


def show(request):
	pass

# def edit(request):
# 	pass

# def update(request):
# 	pass

# def destroy(request):
# 	pass
