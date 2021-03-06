#!/usr/bin/python

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class image_receive:

    def __init__(self):
        #--- Suscriptor del topico de la camara
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/kobuki/camara_principal/image_raw",Image,self.callback)

    def callback(self,data):  #--- Callback del suscriptor
    
        #--- Lectura del grame y conversion usando bridge
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        #--- Si se recibe un frame valido se dibuja un circulo y un text
        (rows,cols,channels) = cv_image.shape
        print("Tenemos {} filas y {} columnas y {} canales desde la camara".format(rows,cols,channels))
        if cols > 20 and rows > 20:
            #--- Circle
            cv2.circle(cv_image, (640,360), 70, 255, 2)
            
            #--- Text
            text = "Imagen recibida"
            cv2.putText(cv_image, text, (350, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, [0,0,200], 5)

        #--- Mostramos el frame recibido
        cv2.imshow("Imagen capturada", cv_image)
        cv2.waitKey(3)

#----Funcion Main
def main():
    #--- Creacion del objeto de la clase anteriormente creada
    ic = image_receive()
    
    #--- Inicializacion del nodo
    rospy.init_node('image_receive', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")
     
    cv2.destroyAllWindows()

if __name__ == '__main__':
        main()