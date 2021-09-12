from django.http import JsonResponse
from .utilities.util import exception, isValid, isException, numToWord


def index(request):
    return JsonResponse({"error": f"Invalid path."}, status=400)

def extenso(request, number):
    if request.method == "GET":
        if not isValid(number):
            return JsonResponse({"extenso": f"Invalid value. Must be an integer ranging from -99999 to 99999."}, status=400)
        
        number = int(number)
        prefix = ''
        if number < 0:
            prefix = 'menos '
            number = abs(number)

        if isException(number):
            return JsonResponse({"extenso": f"{prefix}{exception(number)}"})
        
        wordNum = numToWord(str(number))

        return JsonResponse({"extenso": f"{prefix}{wordNum}"})
        
    else:
        return JsonResponse({"error": f"Invalid request."}, status=400)