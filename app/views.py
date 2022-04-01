from django.shortcuts import render
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
import tempfile
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def Index(request):
    return render(request,'index.html')

@csrf_exempt
def generarCertificado(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        contexto = {'nombre':nombre,'apellido':apellido}
        html_string = render_to_string('certificado/certificado.html',contexto)
        html = HTML(string=html_string)
        result = html.write_pdf()
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="certificado.pdf"'
        response['Content-Transfer-Encoding'] = 'binary'
        with tempfile.NamedTemporaryFile(delete=True) as output:
            output.write(result)
            output.flush()
            output = open(output.name, 'rb')
            response.write(output.read())
        return response
    else:
        return redirect('index')
