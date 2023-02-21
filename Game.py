"""
Este es el codigo del proyecto del juego de Christopher Rodriguez
para ayuda use el comado de Documentacion()
"""
# Importación de los moduclos y bibliotecas necesarias
from tkinter import *
from pygame import *
import pygame, threading, time, os, sys, random
sys.setrecursionlimit(10**6)

print(__doc__)


marcador1=True
marcador2=True
marcador3=True
marcador4=True
marcador5=True
presion1=False
presion2=False
presion3=False
cambio_de_marcha=False
tiempo_de_marcha=1
velocidadmin=10
velocidadactual=10
velocidadmax=15
nivel=0.04
speed=0.04
ganar=True
Perdio= False
puntos=0
PuntosFinales=0
distancia=0
sobrepasos=0
player= "car1.png"
UsuarioNombre= "Anonymous"


pygame.mixer.init()

#Funcion para reproducir sonido
def PlayTheme():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("Adjuntos/Theme.wav")
    pygame.mixer.music.play(loops=-1)

#Funcion para para la reproducción de sonido
def StopMusic():
    pygame.mixer.music.stop()

def Marcha1():
    #pygame.mixer.music.stop()
    pygame.mixer.music.load("Adjuntos/Marcha1.wav")
    pygame.mixer.music.play(loops=-1)
    
def Marcha2():
    #pygame.mixer.music.stop()
    pygame.mixer.music.load("Adjuntos/Marcha2.wav")
    pygame.mixer.music.play(loops=-1)

def Marcha3():
    #pygame.mixer.music.stop()
    pygame.mixer.music.load("Adjuntos/Marcha3.wav")
    pygame.mixer.music.play(loops=-1)

def Marcha4():
    #pygame.mixer.music.stop()
    pygame.mixer.music.load("Adjuntos/Marcha4.wav")
    pygame.mixer.music.play(loops=-1)

#Funcion para el velocimetro   
def Velocidad1(Juego):
    """
    Esta función se engarca de ir aumentando la velocidad o disminuir dependiendo de si se acelera o si se dejo de acelerar 

    Parametros: 
    Juego: Es la ventana donde el usuario interactua con el juego
        Es utilizada para crear el Label donde se mostrara la velocidad
    
    El primer while se ejecuta mientras no se haya alcanzado la velocidad max de la marcha actual y mientras la w sigue siendo presionada
    en caso contrario se ejecuta el segundo while que bajara la velocidad hasta llegar el min de la marcha actual
    La variable tiempo se encarga que el tiempo de espera para volver a ejecutar el while siempre sea el mismo.
    Mientras el usuario mantega la w apretada la velocidad ira aumentando a un 1km/h en caso contrario ira disminuyendo a 1km/h
    A la vez la variable global speed ira disminuyendo de formar proporcional en caso de ir aumentado la velocidad, en caso contrario
    ira aumentado proporcionalmente.

    Return:
        No se retorna
    """
    global  velocidadactual, speed
    
    while presion1==True and velocidadactual<velocidadmax and ganar:
            tiempo=(velocidadmax-velocidadactual)*(tiempo_de_marcha/(velocidadmax-velocidadmin))
            velocidadactual+=1
            Velocidad=Label(Juego, text=(str(velocidadactual) + "km/h"), bg="lavender")
            Velocidad.place(x=258,y=702)
            Velocidad.update()
            speed=speed-(speed/30)
            time.sleep(tiempo/((velocidadmax-velocidadactual)+0.0001))
           

    while presion1==False and velocidadactual>velocidadmin and ganar:
            tiempo=(velocidadmax-velocidadactual)*(tiempo_de_marcha/(velocidadmax-velocidadmin))
            velocidadactual-=1
            Velocidad=Label(Juego, text=(str(velocidadactual) + "km/h"), bg="lavender")
            Velocidad.place(x=258,y=702)
            Velocidad.update()
            speed=speed+(speed/29)
            time.sleep(tiempo/((velocidadmax-velocidadactual)+0.0001))
            


        
       
def Freno(Juego,tiempo,canvas):
    """
    Esta función se encarga de bajar la velocidad hasta el minimo si se desea

    Parametros:
    Juego: Es la ventana donde el usuario interactua con el juego
        Es utilizada para crear el LAbel donde se mostrarar la velocidad
    Tiempo: Tiene el valor de la velocidad actual en el momento de empezar a frenar menos 10 y el resultado divide a 2.
        Es utilizada para la velocidad min se alcance en 2 seg

    La función se seguira llamando a si misma hasta que el usurio deje de frenar o hasta que se llegue a la velocidad minima.
    Cuando la velocidad llega a la mitad de la velocidad de la marcha actual se crar un rectangulo como indicador, y al llegar
    a la velocidad minima se crea otro rectangulo como indicador. 

     Return:
        No se retorna
    """
    global speed, velocidadactual
    
    if presion2==True and velocidadactual!=10 and ganar:
        velocidadactual=velocidadactual-1

        if velocidadactual <= (velocidadmin-15) or velocidadactual==13:
            canvas.create_rectangle(203,727,228,702,fill="red1",tag="Red2")
            canvas.update()
        
        if velocidadactual==10:
            canvas.create_rectangle(230,727,255,702,fill="red1",tag="Red3")
            canvas.update()
    
        Velocidad=Label(Juego, text=(str(velocidadactual) + "km/h"), bg="lavender")
        Velocidad.place(x=258,y=702)
        Velocidad.update
        speed=speed+(speed/29)
        time.sleep(tiempo)
        Freno(Juego,tiempo,canvas)

#Funcion para generar los carros aleatoriamente
def Aparicion_de_enemigos(Juego, canvas, posiciones, enemigo):
    """
    Esta función se encarga de posicionar a los carros aleatoriamente

    Parametros:
    Juego: Es la ventana donde el usuario interactua con el juego
        Este parametro solo se pasa al hilo encargado de mover a los carros.

    Canvas: Es donde se almancena los carros con sus respectivas posiciones.
        Es utilizada para mover a los carros y se pasa al hilo encargado de mover a los carros.

    Posiciones: Es una lista donde se almacena 3 posiciones en el eje x.
        Es utilizada para que las variables posicion1, posicion2, y posicion3 tomen un valor aleatorio de la lista.
    
    Enemigo: Es una lista con los stings de cada carro.
        Es utilizada para que las variavles enemigo 1 y enemigo tome un valor aleatorio.

    Cuando la funcion es llamada le asigna un valor aleatorio a posicion1 y luego elimina el valor tomado de la lista
    para que posicion2 tome un valor diferente, y este se vuelve a eliminar para que finalmente posicion3 tome un valor
    restante. Luego enemigo1 se le asigna un string aleatorio de alguno de los 3 carros y se elimina para que enimigo 2
    tome un valor distinto. Finalmente a cantidad se le asigna un valor entre 0 y 2. Dependiendo del valor de cantidad
    se llamar a ningun carro o solo 1 o a 2 carros. Luego pasa un intervalo aleatorio de tiempo entre 7 a 12 segundos
    y se vuelve a llamar a la funcion, los unicos parametros que se cambiaron fuerons posiones y enemigo, por lo que se 
    tienen que regresar a sus valores originales.
        
     Return:
        No se retorna
    """
  
    if ganar:
        posicion1=random.choice(posiciones)
        posiciones=EliminaElemento(posiciones,posicion1,[])
        posicion2=random.choice(posiciones)
        posicion3=EliminaElemento(posiciones,posicion2,[])[0]
        enemigo1=random.choice(enemigo)
        enemigo=EliminaElemento(enemigo,enemigo1,[])
        enemigo2=random.choice(enemigo)
        cantidad=random.randint(0,2)
        canvas.moveto("Enemigo1",posicion1,-132)
        canvas.moveto("Enemigo2",posicion2,-132)
        canvas.moveto("Enemigo3",posicion3,-132)   
        if cantidad==1:
            T6(Juego,canvas,enemigo1)
        elif cantidad==2:
            T6(Juego,canvas,enemigo1)
            T6(Juego,canvas,enemigo2)
        time.sleep(random.randint(7,12))
        Aparicion_de_enemigos(Juego,canvas,[200,280,370],["Enemigo1","Enemigo2","Enemigo3"])
    

#Funcion para mover a los npc.
def MoverEnemigos(Juego,canvas,enemy):
    """
    Esta función se encarga de mover a los carros

    Parametros:
     Juego: Es la ventana donde el usuario interactua con el juego
        Es utilizada para crear el Label donde se muestran cuando se sobrepasa a un carro.
    
    Canvas: Es donde se almancena los carros con sus respectivas posiciones.
        Es utilizada para mover a los carros e ir verificando sus posiciones.
    
    Enemy: Es un string 
        Se utiliza para localizar al carro deseado
    
    Cuando se llama la función se le asigna a posicion actual del jugadro y a enemigo se le asigna la posicion
    actual del carro que se desea mover. El primer condicional verifica si el usuario aun no a perdido y si el
    carro no ha llegado al limite de la carretera. El segundo condicional verifica si la posicion de la parte 
    trasera del carro que se esta moviendo es igual a la parte delantera del jugador. El segundo el primer elif
    verifica si el lateral derecho del carro que se dea mover es igual al lateral izquierdo del juagor. Y el 
    segundo elif verifica si el lateral izquierdo del carro que se dea mover es igual al lateral derecho del
    jugador. Si se cumple alguno de los 3 ultimos condicionales se produce un choque y el jugador pierde. 
    Mientras no se cumplan la función se siguira llamando así misma hasta que el carro que se desea mover llegue
    al limite de la pista. Cuando la posición del carro que se mueve en el eje "y" es igual al del jugador se 
    aumenta en 1 la cantidad de carros sobrepasados.

    Return:
        No se retorna nada
    """
    global ganar, Perdio, sobrepasos

    posicion=canvas.coords("Jugador")
    enemigo=canvas.coords(enemy)
    
    if enemigo[1]<=700 and ganar:

        if enemigo[0]<=posicion[0]+22<=enemigo[0]+50 and enemigo[1]<=posicion[1]+5<=enemigo[1]+115 or \
            enemigo[0]<=posicion[0]+5<=enemigo[0]+50 and posicion[1]+10==enemigo[1]+115 or \
                enemigo[0]<=(posicion[0]+40)<=enemigo[0]+50 and posicion[1]+10==enemigo[1]+115:

                ganar=False
                Perdio= True

        elif posicion[0]+45==enemigo[0]+5 and posicion[1]+115>=enemigo[1]>=posicion[1] or \
            posicion[0]+45==enemigo[0]+5 and posicion[1]+115>=enemigo[1]+115>=posicion[1]:

            ganar= False
            Perdio= True

        elif enemigo[0]+45==posicion[0]+5 and enemigo[1]+115>=posicion[1]>=enemigo[1] or \
            enemigo[0]+45==posicion[0]+5 and enemigo[1]+115>=posicion[1]+115>=enemigo[1]:

            ganar=False
            Perdio= True
        
        if enemigo[1]==posicion[1]:

            sobrepasos+=1
            Carrors_Soprepasados=Label(Juego, text=("Carros sobrepasado:" + str(sobrepasos)), bg="lavender")
            Carrors_Soprepasados.place(x=100, y=750)
            Carrors_Soprepasados.update()


        
        canvas.move(enemy, 0, 6)
        time.sleep(speed)
        MoverEnemigos(Juego,canvas,enemy)
   


#Funcion para eliminar un elemento ya tomado aleatoriamente       
def EliminaElemento(lista,elemento,resultado):
    if lista==[]:
        return resultado
    elif lista[0]==elemento:
        return EliminaElemento(lista[1:],elemento,resultado)
    else:
        resultado+=[lista[0]]
        return EliminaElemento(lista[1:],elemento,resultado)

        
    
#Funciones para mover las lineas
def Moverlineas(Juego,canvas):
    global ganar, distancia
   
    posicion=canvas.coords("linea1")
    posicion2=canvas.coords("linea3")
    posicion3=canvas.coords("Arbol")
    MetroPs=0.5/(700/6)
    if int(distancia)!=7 and ganar:
        
        if posicion[1]>=700:
            canvas.move("linea1",0,-1485)
            canvas.move("linea2",0,-1485)
           

        if posicion2[1]>=700:
            canvas.move("linea3",0,-1485)
            canvas.move("linea4",0,-1485)
        
        if posicion3[1]>=700:
            canvas.move("Arbol",0,-700)
            

        canvas.move("linea1",0, 6)
        canvas.move("linea2",0, 6)
        canvas.move("linea3",0, 6)
        canvas.move("linea4",0, 6)
        canvas.move("Arbol",0, 6)
        distancia+=MetroPs
        distan=str(round(distancia,1))+" km"
        Kilometros=Label(Juego,text= ("Kilometros Recorridos: " + distan), bg="lavender")
        Kilometros.place(x=435,y=732)
        Kilometros.update
        canvas.update()
        time.sleep(speed)
        Moverlineas(Juego, canvas)

    elif Perdio:
        #Juego.withdraw()
        StopMusic()
        Derrota(Juego)
    else:
        ganar=False
        StopMusic()
        Pantalla_Ganadora(Juego)

def Tiempo_de_Juego(Juego,tiempo):
    global puntos

    if ganar:
        puntos+=1
        tiempo+=1
        Tiempo=Label(Juego, text= "Tiempo de juego: " + str(tiempo) + " segundos", bg="lavender")
        Tiempo.place(x=5, y=702)
        Tiempo.update
        time.sleep(1)
        Tiempo_de_Juego(Juego,tiempo)

def Luces_verdes(canvas,Juego):
    """
    Esta función se encarga de ir encendiendo la luces de la marcha

    Parametros:
    canvas: 

    Juego: Es la ventana donde el usuario interactua con el juego
        Solo se usa como parametro para enviarla al hilo que se encarga aumenta o disminuir velocidades.

    Cuando se llama la función a la variable tiempo se le asigna el valor del tiempo que se durara en llegar
    en llegar a la velocidad maxima de la marcha actual. Luegoe se verifica que no se haya alcanzado los 70km/h
    Luego se verifica que no se haya hecho el cambio de marcha antes de tiempo y tambien que aun se este acelerando,
    los mismo para las 2 siguientes verificaciones. En caso de que no se cumplan algunas de las 3 verificaciones anterioes,
    se hace un verificacion adicional para saber si el usuario hizo el cambio de marcha antes de tiempo, en caso contrario 
    solo se cambia el valor de marcador1 a True. Y en el ultima verifación se pregunta si el usuario hizo el cambio de marcha,
    en caso contrario pierde.


    """
    global ganar, Perdio, marcador1
    global cambio_de_marcha

    cambio_de_marcha=False
    marcador1=False
    tiempo=(velocidadmax-velocidadactual)*(tiempo_de_marcha/(velocidadmax-velocidadmin))
    T1(Juego)
    if velocidadactual!=70:
        canvas.create_rectangle(426,727,451,702,fill="lawn green",tag="square1")
        canvas.update()
        time.sleep(tiempo*(1/2))
        if presion1 and cambio_de_marcha==False and ganar:
            canvas.create_rectangle(399,727,424,702,fill="lawn green",tag="square2")
            canvas.update()
            time.sleep(tiempo*(3/10))

            if presion1 and cambio_de_marcha==False and ganar:
                canvas.create_rectangle(372,727,397,702,fill="lawn green",tag="square3")
                canvas.update()
                time.sleep(tiempo*(1/5))

                if presion1 and cambio_de_marcha==False and ganar:
                    canvas.create_rectangle(345,727,370,702,fill="lawn green",tag="square4")
                    canvas.update()
                    time.sleep(1)
                    if cambio_de_marcha:
                        cambio_de_marcha=False
           
                        marcador1=True
                        
                        canvas.delete("square1")
                        canvas.delete("square2")
                        canvas.delete("square3")
                        canvas.delete("square4")
                        canvas.update()
               
                    elif presion1 or ((velocidadactual==velocidadmin) and velocidadmin!=10) :
                        Perdio=True
                        ganar=False

                elif cambio_de_marcha==True:
                    cambio_de_marcha=False
                    marcador1=True
              
                    reduccion=velocidadactual-velocidadmin
                    cambio=int(velocidadactual - (reduccion* (random.randint(1,100)/100)))
                    MalCambio(Juego,cambio)

                else:
                    marcador1=True
          
            elif cambio_de_marcha==True:
                cambio_de_marcha=False
                marcador1=True
                
                reduccion=velocidadactual-velocidadmin
                cambio=int(velocidadactual - (reduccion* (random.randint(1,100)/100)))
                MalCambio(Juego,cambio)
            
            else:
                marcador1=True
    

        elif cambio_de_marcha==True:
            cambio_de_marcha=False
          
            marcador1=True
           
            reduccion=velocidadactual-velocidadmin
            cambio=int(velocidadactual - (reduccion* (random.randint(1,100)/100)))
            MalCambio(Juego,cambio)

        else:
            marcador1=True
    

def MalCambio(Juego,cambio):
    global velocidadactual, speed, cambio_de_marcha, presion1

    if velocidadactual!=cambio:
        velocidadactual=velocidadactual-1
        Velocidad=Label(Juego, text=(str(velocidadactual) + "km/h"), bg="lavender")
        Velocidad.place(x=258,y=702)
        Velocidad.update
        speed=speed+(speed/29)
        MalCambio(Juego,cambio)
    cambio_de_marcha=False
    presion1=False
  


def Pantalla_Ganadora(Juego):
    global PuntosFinales

    PuntosFinales+= int(round(100 +100%puntos,0))
    print(PuntosFinales)
    Victoria=Toplevel(bg="green")
    Victoria.title("Victoria")
    Victoria.minsize(400,400)
    Victoria.resizable(width=NO, height=NO)
    Menu=Button(Victoria,text="Menu Principal", command= lambda: (Menu_Principal(Juego,Victoria))) 
    Menu.place(x=50, y=100)
    Siguiente_Nivel=Button(Victoria, text="Siguiente Nivel", command= lambda: (Siguiente(Juego,Victoria)) ) 
    Siguiente_Nivel.place(x= 150, y= 100)


def Derrota(Juego):
    Derrota=Toplevel(bg="red")
    Derrota.title("Derrota")
    Derrota.minsize(400,400)
    Derrota.resizable(width=NO, height=NO)
    Menu=Button(Derrota,text="Menu", command= lambda: (Menu_Principal(Juego,Derrota)) )
    Menu.place(x=50, y=100)
    VolverJugar=Button(Derrota, text="Volver a jugar", command= lambda: (VolverAJugar(Juego,Derrota)) ) 
    VolverJugar.place(x= 150, y= 100)
    

def Mover_Derecha(canvas):
    global ganar, Perdio

    posicion=canvas.coords("Jugador")

    if ganar and presion3 and marcador4==False:
        canvas.move("Jugador",10,0)
        if (posicion[0]+40)>440:
            ganar=False
            Perdio=True
            canvas.move("Jugador",10,0)
        time.sleep(0.05)
        Mover_Derecha(canvas)


def Mover_Izquierda(canvas):
    global ganar, Perdio
 
    posicion=canvas.coords("Jugador")

    if ganar and presion3 and marcador5==False:
        canvas.move("Jugador",-10,0)
        if (posicion[0])<160:
            ganar=False
            Perdio=True
            canvas.move("Jugador",-10,0)
        time.sleep(0.05)
        Mover_Izquierda(canvas)

#Hilos para cada funcion necesaria        

def T1(Juego):
    t1=threading.Thread(target=Velocidad1,args=(Juego,))
    t1.start()



def T2(Juego,tiempo,canvas):
    t2=threading.Thread(target=Freno,args=(Juego,tiempo,canvas))
    t2.start()



def T3(Juego ,canvas):
    t3=threading.Thread(target=Moverlineas, args=(Juego, canvas))
    t3.start()

def T4(canvas,Juego):
    t4=threading.Thread(target=Luces_verdes,args=(canvas,Juego))
    t4.start()


def T5(Juego, tiempo):
    t5=threading.Thread(target=Tiempo_de_Juego, args=(Juego, tiempo))
    t5.start()

def T6(Juego,canvas,enemigo):
    t6=threading.Thread(target=MoverEnemigos, args=(Juego,canvas,enemigo))
    t6.start()

def T7(canvas):
    t7=threading.Thread(target=Mover_Derecha, args=(canvas,))
    t7.start()

def T8(canvas):
    t8=threading.Thread(target=Mover_Izquierda, args=(canvas,))
    t8.start()

def T9(Juego,canvas):
    t9=threading.Thread(target=Aparicion_de_enemigos, args=(Juego,canvas, [200,280,370],["Enemigo1","Enemigo2","Enemigo3"]))
    t9.start()

#Esta funcion es para cargar las diferentes imagenes
def cargarImagen(nombre): 
    ruta = os.path.join('Adjuntos/',nombre) #Se le indica el lugar donde buscar la imagen y el nombre de la imagen
    imagen = PhotoImage(file=ruta) #Se crea lad imagen  
    return imagen


#La ventana para el juego
class Mecanicas:

    def __init__(self):
        global marcador1, marcador2, marcador3, marcador4, marcador5, presion1, presion2, presion3, \
            cambio_de_marcha, tiempo_de_marcha, velocidadmin, velocidadactual, velocidadmax, nivel, \
                speed, ganar, Perdio, distancia, sobrepasos, player, UsuarioNombre

        marcador1= True
        marcador2= True
        marcador3= True
        marcador4= True
        marcador5= True
        presion1= False
        presion2= False
        presion3= False
        cambio_de_marcha= False
        tiempo_de_marcha= 1
        velocidadmin= 10
        velocidadactual= 10
        velocidadmax= 15
        speed= nivel
        ganar= True
        Perdio = False      
        distancia= 0
        sobrepasos= 0
        
        self.Juego=Toplevel()
        Screenwidth= str(int(Inicio.winfo_screenwidth()/2)-300)
        Screenheight= str(int(Inicio.winfo_screenheight()/2)-390)
        size = "600x780+"+Screenwidth+"+"+Screenheight
        self.Juego.geometry(size)
        self.Juego.resizable(width=False,height=False)
        self.canvas=Canvas(self.Juego,width=600,height=780,background="white")
        self.canvas.place(x=0,y=0)

        self.canvas.create_rectangle(-2,700,165,0,fill="green")
        self.canvas.create_rectangle(165,700,255,0,fill="grey")
        self.canvas.create_rectangle(255,700,345,0,fill="grey")
        self.canvas.create_rectangle(345,700,435,0,fill="grey")
        self.canvas.create_rectangle(435,700,600,0,fill="green")
        self.canvas.create_rectangle(254,700,256,0,fill="yellow")
        self.canvas.create_rectangle(344,700,346,0,fill="yellow")

        lineas=cargarImagen("1.png")
        self.canvas.create_image(155,3,image=lineas,anchor=NW,tag="linea1")
        self.canvas.create_image(435,3,image=lineas,anchor=NW,tag="linea2")
        self.canvas.create_image(155,-785,image=lineas,anchor=NW,tag="linea3")
        self.canvas.create_image(435,-785,image=lineas,anchor=NW,tag="linea4")

        avatar=cargarImagen(player)
        car1=cargarImagen("car1.png")
        car2=cargarImagen("car2.png")
        car3=cargarImagen("car3.png")
        arbol=cargarImagen("arbol.png")

        self.canvas.create_image(200,-132,image=car1,anchor=NW,tag="Enemigo1")
        self.canvas.create_image(280,-132,image=car2,anchor=NW,tag="Enemigo2")
        self.canvas.create_image(370,-132,image=car3,anchor=NW,tag="Enemigo3")
        self.canvas.create_image(280,438,image=avatar,anchor=NW,tag="Jugador")
        self.canvas.create_image(575,0,image=arbol,anchor=NW,tag="Arbol")

        self.canvas.create_rectangle(0,780,600,700,fill="lavender")

        self.canvas.create_rectangle(345,727,370,702,outline="lawn green")
        self.canvas.create_rectangle(372,727,397,702,outline="lawn green")
        self.canvas.create_rectangle(399,727,424,702,outline="lawn green")
        self.canvas.create_rectangle(426,727,451,702,outline="lawn green")

        self.canvas.create_rectangle(230,727,255,702,outline="red1")
        self.canvas.create_rectangle(203,727,228,702,outline="red1")
        self.canvas.create_rectangle(176,727,201,702,outline="red1")
        
        NombreUsuario=Label(self.Juego, text=("Jugador:" + UsuarioNombre), bg="lavender")
        NombreUsuario.place(x=240, y=730)
        Velocidad=Label(self.Juego, text=(str(velocidadactual)+"km/h"), bg="lavender")
        Velocidad.place(x=258,y=702)
        Kilometros=Label(self.Juego,text="Kilometros Recorridos: 0 km", bg="lavender")
        Kilometros.place(x=435, y= 732)
        Carrors_Soprepasados=Label(self.Juego, text="Carros sobrepasado: 0", bg="lavender")
        Carrors_Soprepasados.place(x=100, y=750)
        Tiempo=Label(self.Juego, text= "Tiempo de juego: 0 segundos", bg="lavender")
        Tiempo.place(x=5, y=702)
        Marcha=Label(self.Juego, text= "Marcha actual: " + str(tiempo_de_marcha), bg="lavender")
        Marcha.place(x=240, y=750)
        Tiempo.update()

        self.canvas.grid()

        Marcha1()
        T3(self.Juego, self.canvas) 
        T5(self.Juego, 0)
        T9(self.Juego, self.canvas)

        self.Juego.bind("d",self.right)
        self.Juego.bind("a",self.left)
        self.Juego.bind("w",self.Acelerar)
        self.Juego.bind("s",self.Frenar)
        self.Juego.bind("e",self.Cambiar_Marcha)
        self.Juego.bind("<KeyRelease>",self.Libera)
        self.Juego.mainloop()
        self.Juego.deiconify()

    def mover_mouse(self,evento):
        self.Juego.title(str(evento.x)+"/"+str(evento.y))
        
    def presion_mouse(self,evento):
        self.canvas.create_oval(evento.x-5,evento.y-5,evento.x+5,evento.y+5,fill="red")


    def Acelerar(self,evento):
        global presion1
       
        if marcador1 and presion2==False and velocidadactual!=70 and ganar:
            presion1=True
            T4(self.canvas,self.Juego)


    def Cambiar_Marcha(self,evento):
        global cambio_de_marcha, marcador3
      
        if marcador3:
            marcador3= False
            cambio_de_marcha= True
        
    
    def Frenar(self,evento):
        global presion2, marcador2
        
        if marcador2 and presion1==False and velocidadactual!=10 and ganar:
            self.canvas.create_rectangle(176,727,201,702,fill="red1",tag="Red1")
            self.canvas.update()
            presion2=True
            tiempo= 2/(velocidadactual-10)
            marcador2=False
            T2(self.Juego,tiempo,self.canvas)

        elif marcador2 and presion1==False and velocidadactual==10 and ganar:
            self.canvas.create_rectangle(176,727,201,702,fill="red1",tag="Red1")
            self.canvas.create_rectangle(203,727,228,702,fill="red1",tag="Red2")
            self.canvas.create_rectangle(230,727,255,702,fill="red1",tag="Red3")
            self.canvas.update()
    
    

    def Libera(self,evento):
        global  marcador1, marcador2, marcador3, marcador4, marcador5, presion1, presion2, presion3,\
        tiempo_de_marcha, velocidadmax, velocidadmin
    
    
        if evento.keysym=="w" and ganar:
            time.sleep(0.001)
            presion1=False
           
            self.canvas.delete("square1")
            self.canvas.delete("square2")
            self.canvas.delete("square3")
            self.canvas.delete("square4")
            self.canvas.update()

            if velocidadactual==15:
                tiempo_de_marcha=2
                velocidadmax=45
                velocidadmin=15
                Marcha=Label(self.Juego, text= "Marcha actual: " + str(tiempo_de_marcha), bg="lavender")
                Marcha.place(x=240, y=750)
                Marcha.update
                Marcha2()
                

            elif velocidadactual==45:
                tiempo_de_marcha=3
                velocidadmax=70
                velocidadmin=45
                Marcha=Label(self.Juego, text= "Marcha actual: " + str(tiempo_de_marcha), bg="lavender")
                Marcha.place(x=240, y=750)
                Marcha.update

                Marcha3()

            elif velocidadactual==70:
                tiempo_de_marcha=4
                velocidadmin=70
                Marcha=Label(self.Juego, text= "Marcha actual: " + str(tiempo_de_marcha), bg="lavender")
                Marcha.place(x=240, y=750)
                Marcha.update

                Marcha4()
                
            
        elif evento.keysym=="s" and ganar:
            marcador2=True
            presion2=False
            marcador1=True
            self.canvas.delete("Red1")
            self.canvas.delete("Red2")
            self.canvas.delete("Red3")
            self.canvas.update()
            if velocidadactual<70 and velocidadactual>45:
                tiempo_de_marcha=3
                velocidadmax=70
                velocidadmin=45
                Marcha=Label(self.Juego, text= "Marcha actual: " + str(tiempo_de_marcha), bg="lavender")
                Marcha.place(x=240, y=750)
                Marcha.update
                Marcha3()

            elif velocidadactual<45 and velocidadactual>15:
                tiempo_de_marcha=2
                velocidadmax=45
                velocidadmin=15
                Marcha=Label(self.Juego, text= "Marcha actual: " + str(tiempo_de_marcha), bg="lavender") 
                Marcha.place(x=240, y=750)
                Marcha.update
                Marcha2()

            elif velocidadactual<15:
                tiempo_de_marcha=1
                velocidadmax=15
                velocidadmin=10
                Marcha=Label(self.Juego, text= "Marcha actual: " + str(tiempo_de_marcha), bg="lavender")
                Marcha.place(x=240, y=750)
                Marcha.update
                Marcha1()
        
        

        elif evento.keysym=="d" and ganar:
            marcador4=True
            presion3=False
           

        elif evento.keysym=="a" and ganar:
            marcador5=True
            presion3=False
           
        
        elif evento.keysym=="e" and ganar:
            marcador3=True

    def right(self,evento):
        global  marcador4, marcador5, presion3

        if marcador4 and marcador5 and presion3==False:
            marcador4=False
            presion3=True
            T7(self.canvas)

    def left(self,evento):
        global marcador4, marcador5, presion3
  
        if marcador5 and marcador4 and presion3==False:
            marcador5=False
            presion3=True
            T8(self.canvas)
                

    
    
def Lose(Juego):
    global ganar
    ganar=False
    Juego.close()

def Menu_Principal(Juego,Victoria):
    PlayTheme()
    Juego.withdraw()
    Victoria.withdraw()
    Contenido= LeerArchivo()
    Posicion=VerificaPosicion(Contenido,1)

    if Posicion<8:
        Borrar=open("Puntos.txt","w")
        Borrar.close()
        NuevaTabla(Posicion,1,Contenido)

    Inicio.deiconify()

def VolverAJugar(Juego,Derrota):
    Juego.withdraw()
    Derrota.withdraw()
    Mecanicas()

def Siguiente(Juego,Victoria):
    global nivel
    nivel= nivel - (nivel*0.125)
    Juego.withdraw()
    Victoria.withdraw()
    print (nivel)
    Mecanicas()

def Mercedez():
    global player
    player="car1.png"
    canvas.moveto(Seleccion, 100, 235)

def RedBull():
    global player
    player="car2.png"
    canvas.moveto(Seleccion, 412, 235)
    

def Ferrari():
    global player
    player="car3.png"
    canvas.moveto(Seleccion, 240, 235)

def Sorpresa():
    global player
    player="pato.png"
    canvas.moveto(Seleccion,250, 475,)

def Jugar(Nombre):
    global UsuarioNombre
    global nivel
    global puntos
    global PuntosFinales
    nivel= 0.04
    PuntosFinales= 0
    puntos= 0
    if Nombre!="":
        UsuarioNombre=Nombre
    else:
        UsuarioNombre="Anonymous"
    
    Inicio.withdraw()

    Mecanicas()

def LeerArchivo():
    archivo=open("Puntos.txt")
    Contenido=archivo.readlines()
    archivo.close()
    return Contenido
    


def VerificaPosicion(Contenido,Contador):
    if Contenido==[]:
        return Contador
    
    elif int(Contenido[0].split(",")[2].split("\n")[0])<PuntosFinales:
        return Contador

    else:
        Contador+=1
        return VerificaPosicion(Contenido[1:], Contador)


def Escribir(dato):
    archivo=open("Puntos.txt","a")
    archivo.write(dato+"\n")
    archivo.close

def NuevaTabla(Posicion,Contador,Tabla):
    global UsuarioNombre
    global PuntosFinales
    if Contador!=8:
        if Posicion==Contador:
            Escribir(str(Contador) + ")" + "," + UsuarioNombre + "," + str(PuntosFinales))
            Contador+=1
            return NuevaTabla(Posicion,Contador,Tabla)
        else:
            Usuario=Tabla[0].split(",")[1]
            Puntaje=Tabla[0].split(",")[2].split("\n")[0]
            Escribir(str(Contador) + ")" + "," + Usuario + "," + Puntaje)
            Contador+=1
            return NuevaTabla(Posicion, Contador, Tabla[1:])
    
#Funcion para la tabla
def Tabla():
    Tabla=Toplevel(bg="Blue")#Se define la ventana
    Tabla.title("Salón de la fama")#Se le indica el titulo a la ventana
    Tabla.resizable(width=NO,height=NO)#Se restringe el tamaño
    Puntajes= Transformar(LeerArchivo(),[])
    TablaAux(0,0,8,2,Puntajes, Tabla)
    Tabla.mainloop()

def Transformar(Tabla,Resultado):
    if Tabla==[]:
        return [["Jugadores", "Puntaje"]] + Resultado
    else:
        Resultado= Resultado + [[Tabla[0].split(",")[0] + " " + Tabla[0].split(",")[1], Tabla[0].split(",")[2].split("\n")[0]]]
        return Transformar(Tabla[1:],Resultado)

def TablaAux(fila, columna, filamax, columnamax, Puntajes, Tabla):
    if fila<filamax:
        Celda=Entry(Tabla,width=20,fg="black",bg="sky blue",font=("Arial",15,"bold"))
        Celda.grid(row=fila, column= columna)
        Celda.insert(END, Puntajes[fila][columna])
        columna+=1
        if columna<columnamax:
            TablaAux(fila, columna, filamax, columnamax, Puntajes, Tabla)
        else:
            fila+=1
            columna=0
            TablaAux(fila, columna, filamax, columnamax, Puntajes, Tabla)


def Mi_foto():
    Me=Toplevel()
    Me.minsize(450,736)
    Me.resizable(width=NO,height=NO)
    Me.title("Yo")
    imagen=cargarImagen("integrante.png")
    Fondo=Label(Me,image=imagen)
    Fondo.place(x=-2,y=-2)
    Me.mainloop()

def Acerca():
    About=Toplevel()
    About.title("Acerca")
    About.minsize(600,315)
    About.resizable(width=NO, height=NO)
    Tec=cargarImagen("tec.png")
    Fondo=Label(About, image= Tec)
    Fondo.place(x=-2, y=-2)
    Nombre=Label(About,text="Nombre: Christopher David Rodríguez Cordero",font=("Arial",11))
    Nombre.place(x=10,y=10)
    Carnet=Label(About,text="Carnet: 2022040771", font=("Arial",11))
    Carnet.place(x=10,y=45)
    Carrera=Label(About,text="Carrera: CE, Curso: Taller de Programación", font=("Arial",11))
    Carrera.place(x=10,y=80)
    Profesor=Label(About,text="Profeso: Jason Leiton", font=("Arial",11))
    Profesor.place(x=10,y=215)
    Version=Label(About,text="Version: 1.0, Ultima modificación: 12/05/2022", font=("Arial",11))
    Version.place(x=10,y=250)
    Yo=Button(About, text= "Foto del integrante", command=Mi_foto)
    Yo.place(x=350, y=10)
    About.mainloop()
    
def Close():
    StopMusic()
    Inicio.destroy()



#Funcion para la autodocumentacion:

def Documentacion():
    print("Documentacion de Velocidad1: ")
    help(Velocidad1)
    print("Documentacion de Freno: ")
    help(Freno)
    print("Documentacion de Aparicion de enemigos")
    help(Aparicion_de_enemigos)
    print("Documentacion de MoverEnemigos")
    help(MoverEnemigos)
    print("Documentacion de Luces Verdes")
    help(Luces_verdes)
    



#Ventana Principal

Inicio=Tk()
PlayTheme()
Screenwidth= str(int(Inicio.winfo_screenwidth()/2)-256)
Screenheight= str(int(Inicio.winfo_screenheight()/2)-256)
size = "512x512+"+Screenwidth+"+"+Screenheight
Inicio.title("Simulador de Formula 1")
Inicio.geometry(size)
Inicio.resizable(width=NO, height=NO)
canvas=Canvas(Inicio,width=512,height=780)
imagen=cargarImagen("menu.png")
canvas.create_image(-2, -2, image=imagen, anchor=NW)

Nombre=Label(Inicio,text="Nombre",bg="blue", fg="white")
Nombre.place(x= 230, y=2)
Nombre_del_usuario=Entry(Inicio, width=20, bg="white")
Nombre_del_usuario.place(x=195, y=50)

Opciones=Menu(Inicio)
Opciones.add_command(label= "Salón de la fama",command=Tabla)
Opciones.add_command(label= "Acerca", command= Acerca)
Inicio.config(menu= Opciones)
Escoger=Label(Inicio, text="Escoge tu vehiculo", font=(8))
Escoger.place(x=185, y=170)
Flecha=cargarImagen("flecha.png")

Seleccion=canvas.create_image(100, 235, image=Flecha, anchor=NW)

Carro1=Button(Inicio, text= "Mercedez", command= Mercedez)
Carro1.place(x=80, y=210)
Carro2=Button(Inicio, text= "RedBull", command= RedBull)
Carro2.place(x=400, y=210)
Carro3=Button(Inicio, text= "Ferrari", command= Ferrari)
Carro3.place(x=230, y=210)
Misterio=Button(Inicio, text= "(?)", command= Sorpresa)
Misterio.place(x=250, y=450)
Play=Button(Inicio, text="Jugar", command= lambda: Jugar(Nombre_del_usuario.get()))
Play.place(x=235, y= 100)
Salir=Button(Inicio, text="Salir", command= Close)
Salir.place(x=235, y= 400)
canvas.grid()

Inicio.mainloop()


""" 
Referencias:
diego moisset de espanes(Mayo 10, 2020), Tomado de: https://youtu.be/eM5azEv77ag
No author, No fecha, PythonTutorial, Tomado de: https://www.pythontutorial.net/tkinter/tkinter-event-binding/
gurusingh(Enero 27, 2022), GeeksforGeeks, Tomado de: https://www.geeksforgeeks.org/random-choices-method-in-python/




"""

