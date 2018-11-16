from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from utils import http
from models import Room, Booking
from utils import codes, messages

@csrf_exempt
@http.json_response()
@require_http_methods("GET")
def get_all_rooms(request):
	rooms = Room.objects.all()
	return {
		'results': [r.to_json() for r in rooms]
	}

@csrf_exempt
@http.json_response()
@require_http_methods("POST")
@http.required_parameters(["start_timestamp", "end_timestamp"])
def get_available_rooms(request):
	start_timestamp = request.POST.get("start_timestamp")
	end_timestamp = request.POST.get("end_timestamp")
	bad_bookings = Booking.objects.filter(start_timestamp__lte=end_timestamp, end_timestamp__gte=start_timestamp)
	rooms = Room.objects.all().exclude(id__in=[x.room.id for x in bad_bookings])
	return {
		'results': [r.to_json() for r in rooms]
	}


@csrf_exempt
@http.json_response()
@require_http_methods("POST")
@http.required_parameters(["room_id", "start_timestamp", "end_timestamp"])
def make_booking(request):
	room_id = request.POST.get("room_id")
	start_timestamp = request.POST.get("start_timestamp")
	end_timestamp = request.POST.get("end_timestamp")
	room = Room.objects.get(id=room_id)
	if room is None:
		return http.code_response(codes.ROOM_DOES_NOT_EXIST, message=messages.ROOM_DOES_NOT_EXIST) 
	b, _ = Booking.objects.get_or_create(room=room, start_timestamp=start_timestamp, end_timestamp=end_timestamp)
	print(b)
	qr_code = str(room_id) + str(start_timestamp) + str(end_timestamp)
	return {
		'results':{
			'qr_code': qr_code,
		}
	}

