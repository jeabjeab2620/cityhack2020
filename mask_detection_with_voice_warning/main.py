import datetime
import sys
sys.path.append("../")
import re
import atlas_utils.video as video
import socket

from atlas_utils.camera import Camera
from atlas_utils import presenteragent
from acl_model import Model
from acl_resource import AclResource
from vgg_ssd import VggSsd
import math

MODEL_PATH = "../model/yolo3_resnet18.om"
MODEL_WIDTH = 640
MODEL_HEIGHT = 352
MASK_DETEC_CONF="../scripts/mask_detection.conf"
CAMERA_FRAME_WIDTH = 1280
CAMERA_FRAME_HEIGHT = 720

def main():
    acl_resource = AclResource()
    acl_resource.init()
    #Create an object to perform detection preprocessing, postprocessing and so on
    detect = VggSsd(acl_resource, MODEL_WIDTH, MODEL_HEIGHT)
    #Load the pre-trained model from path
    model = Model(MODEL_PATH)
    #Connect to the Presenter Server according to the config file    
    chan = presenteragent.presenter_channel.open_channel(MASK_DETEC_CONF)
    if chan == None:
        print("Open presenter channel failed")
        return
    #Start the Pi camera on the Atlas 200DK, input argument for the camera port(0 or 1)
    cap = Camera(0)
	
    while True:
        #Read an image frame from the camera
        image = cap.read()
        if image is None:
            print("read None image, break")
            break

        #Image preprocessing
        model_input = detect.pre_process(image)
        if model_input == None:
            print("Pre process image failed")
            break
        
        #Send the data to the model for detection
        result = model.execute(model_input)
        if result is None:
            print("execute mode failed")
            break
        
        #Post-process the detection result
        jpeg_image, detection_list = detect.post_process(result, image)
        for i in range(len(detection_list)):     
	    #Print the detection result, the detection box coordinates,
	    #detected label, confidence
            print(detection_list[i].box.lt.x, 
                  detection_list[i].box.lt.y, 
                  detection_list[i].box.rb.x, 
                  detection_list[i].box.rb.y, 
                  detection_list[i].result_text, 
                  detection_list[i].confidence)
##############################################################################################################################################################
            d = math.sqrt(pow(detection_list[i].box.lt.x - detection_list[i].box.rb.x,2)+pow(detection_list[i].box.lt.y - detection_list[i].box.rb.y,2)) 

            if (d > 600):
                msg = detection_list[i].result_text
                bytesToSend = str.encode(msg)
                serverAddressPort = ("192.168.1.22", 20001)
                bufferSize = 1024
                UDPClientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                UDPClientSocket.sendto(bytesToSend,serverAddressPort)
##############################################################################################################################################################

        if jpeg_image == None:
            print("The jpeg image for present is None")
            break
	#Send the result to the Present Server to display onto the browser
        chan.send_detection_data(CAMERA_FRAME_WIDTH, CAMERA_FRAME_HEIGHT,
                                 jpeg_image, detection_list)  
        
if __name__ == '__main__':
    main()

