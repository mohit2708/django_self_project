from django.shortcuts import render, redirect
from django.http import HttpResponse
from crud_function_based.models import Customer


# Get a logger instance



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
		print(request.POST)
		if 'dof' in request.POST and not request.POST['dof']:
			dof = None  # Set to None if empty
		else:
			dof = request.POST.get('dof', '').strip()

		if 'age' in request.POST and not request.POST['age']:
			age = None  # Set to None if empty
		else:
			age = request.POST.get('age', '').strip()

		first_name = request.POST.get('first_name', '').strip()
		last_name = request.POST.get('last_name', '').strip()
		email = request.POST.get('email', '').strip()
		user_name = request.POST.get('user_name', '').strip()
		phone_number = request.POST.get('phone_number', '').strip()
		gender = request.POST.get('gender', '').strip()
		# dof = request.POST.get('dof', '').strip()
		# age = request.POST.get('age', '').strip()
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


def show(request, id):
	customer = Customer.objects.get(id=id)
	return render(request, 'crud_function_based/edit.html', {'customers':customer})

# def edit(request):
# 	pass

def update(request, id):
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

	customer_update = Customer.objects.get(id=id)
	customer_update.first_name = first_name
	customer_update.last_name = last_name
	customer_update.email = email
	customer_update.phone_number = phone_number
	customer_update.gender = gender
	customer_update.dof = dof
	customer_update.age = age
	customer_update.country = country
	customer_update.city = city
	customer_update.message = message
	customer_update.save()

	return redirect('/')
	# return HttpResponseRedirect(reverse('index'))


def destroy(request, id):
    del_data = Customer.objects.get(id=id)  
    del_data.delete()
    return redirect('/')