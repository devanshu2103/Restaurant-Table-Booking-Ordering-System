from django.shortcuts import render, redirect
from .models import TableCategory, Booking,MenuItem,Order
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime,timedelta
from django.utils import timezone
def home(request):
    return render(request, 'index.html')

def starter_page(request):
    return render(request,'starter-page.html')

def book_table(request):
    tables = TableCategory.objects.all()
    bookings = Booking.objects.all()
    message = ''
    if request.method == 'POST':
        print(f"POST data received: {request.POST}")  
        name = request.POST.get('name')
        table_type_id = request.POST.get('table_type')
        booking_time_str = request.POST.get('booking_time')
        duration_minutes = int(request.POST.get('duration'))
        print(f"Received table_type_id: {table_type_id}") 
        try:
            table_type = TableCategory.objects.get(id=table_type_id)
            booking_time = datetime.strptime(booking_time_str,"%Y-%m-%dT%H:%M")
            duration = timedelta(minutes=duration_minutes)
            print(f"Found TableCategory: {table_type}")  

            if table_type.available_tables > 0:
                existing_bookings = Booking.objects.filter(table_type=table_type,actual_end_time__isnull=True)
                assigned_seats =[b.seat_number for b in existing_bookings if  b.seat_number]
                seat_number = None
                for i in range(10):
                    suffix = chr(65 + i)  # A to J
                    candidate = f"{table_type.category}{suffix}"
                    if candidate not in assigned_seats:
                        seat_number = candidate
                        break
                Booking.objects.create(name=name, table_type=table_type,booking_time = booking_time,duration=duration,seat_number=seat_number)
                table_type.available_tables -= 1
                table_type.save()
                message = f"Table booked successfully for {name}! Seat:{seat_number}"
            else:
                message = "Sorry, no tables available for the selected category."
        except TableCategory.DoesNotExist:
            message = "Invalid table category selected."
    return render(request, 'book_table.html', {'tables': tables, 'message': message, 'bookings': bookings})

@require_POST
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        table_type = booking.table_type
        table_type.available_tables += 1
        table_type.save()
        booking.delete()
    except Booking.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('book_table'))
def dashboard(request):
    categories = TableCategory.objects.all()
    bookings = Booking.objects.all()
    menu_items =  MenuItem.objects.all()
    orders = Order.objects.all()
    
    # //////////////////////////////////////////////customer bill ki chije yaha include karna he meko 

    return render(request,'dashboard.html',{
        'categories': categories,
        'bookings': bookings,
        'menu_items': menu_items,
        'orders': orders
    })


@require_POST
def leave_table(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)

        if not booking.actual_end_time:
            booking.actual_end_time = timezone.now()
            booking.save()

            table_type = booking.table_type
            table_type.available_tables += 1
            table_type.save()

    except Booking.DoesNotExist:
        pass

    return redirect('book_table')


def menu_order(request):
    bookings = Booking.objects.filter(actual_end_time__isnull=True)
    menu_items = MenuItem.objects.all()

    if request.method == 'POST':
        booking_id = request.POST.get('booking')
        item_id = request.POST.get('item')
        quantity = int(request.POST.get('quantity'))

        booking = Booking.objects.get(id=booking_id)
        item = MenuItem.objects.get(id=item_id)

        Order.objects.create(booking=booking, item=item, quantity=quantity)
        return redirect('menu_order')

    return render(request, 'menu_order.html', {
        'bookings': bookings,
        'menu_items': menu_items
    })

def history_view(request):
    completed_bookings =  Booking.objects.exclude(actual_end_time__isnull = True).order_by('-actual_end_time')
    return render(request,'history.html',{'complete_booking':completed_bookings})