import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia


#opciones de voz(idiomas)
id1= 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2= 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

#escuchar microfono y devolver el audio en texto
def transformar_audio_en_texto():

    #almacenar recognizer en variable
    r= sr.Recognizer()

#configurar el microfono
    with sr.Microphone() as origen:

        #tiempo de espera
        r.pause_threshold = 0.9
        #informar que comenzo la grabacion
        print('ya puedes hablar')

        # almacenar como audio
        audio = r.listen(origen)
        try:
            #buscar en google
            pedido = r.recognize_google(audio, language= "es-MX")

            #prueba de ingreso
            print('dijiste: ' + pedido)

            #devolver pedido
            return pedido

        #en caso de no poder comprender audio
        except sr.UnknownValueError:
            #prueba de comprension de audio
            print('ups, yo no entender')

            #devolver error
            return 'sigo esperando'

        #en caso de no resolver pedido
        except sr.RequestError:
            # prueba de comprension de audio
            print('ups, sin servicio')

            # devolver error
            return 'sigo esperando'

        #error inesperado
        except:

            #prueba de comprensiond e audio
            print('ups, salio algo mal')

            #devolver error
            return 'Sigo esperando'

#funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    #encender el motorde pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)
    #pronunciarmensaje
    engine.say(mensaje)
    engine.runAndWait()


#informar el dia de la semana
def pedir_dia():
    #crear variable con datos del dia (hoy)
    dia = datetime.date.today()
    print(dia)
    #crear variable para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)
    #diccionario con nombres de dias
    calendario ={0:'Lunes',
                 1:' Martes',
                 2:'Miércoles',
                 3:'Jueves',
                 4:'Viernes',
                 5:'Sábado',
                 6:'Domingo'}

    #decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')

#informar que hora es
def pedir_hora():

    #crear variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'en este momento son las {hora.hour} horas con {hora.minute} minutos y  {hora.second} segundos'
    print(hora)
    #decir la hora
    hablar(hora)

#saludo inicial

def saludo_inicial():

    #crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour <6 or hora.hour> 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen dia'
    else:
        momento = 'Buenas tardes'

    # decir el saludo
    hablar(f'{momento}, soy justina, tu asistente personal. Por favor, dime en que te puedo ayudar')

#funcion central del asistente
def pedir_cosas():

    #activar saludo inicial
    saludo_inicial()

    #variable de corte
    comenzar = True

    #loop central
    while comenzar:

        #activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('con gusto, estoy abriendo youtube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Claro, estoy trabajando en ello')
            webbrowser.open('https://www.google.com')
            continue
        elif 'que dia es hoy' in pedido :
            pedir_dia()
            continue
        elif 'que hora es' in pedido:
            pedir_hora()
            continue
        elif 'buscar en wikipeadia' in pedido:
            hablar('buscandoló en wikipedia')
            pedido = pedido.replace('busca en wikipedia', ' ')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences =1)
            hablar('wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('estoy en ello')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1]
            cartera = {'apple':'APPLE',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'la encontré, el precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdon, pero no lo he encontrado')
                continue
        elif 'adiós' in pedido:
            hablar('Me voy a descansar, quedo al pendiente, patrón')
            break





pedir_cosas()











