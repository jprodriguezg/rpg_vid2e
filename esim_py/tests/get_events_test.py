
import esim_py
import matplotlib.pyplot as plt
import numpy as np
import os, csv
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

def show_events_by_polarity(events, width, height):
    event_image = np.zeros((height,width,3), np.uint8)

    for ii in range(0, len(events)):
        if events[ii][3] == 1 :
            event_image[int(events[ii][1]),int(events[ii][0])] = [255,0,0]
        else:
            event_image[int(events[ii][1]),int(events[ii][0])] = [0,0,255]

    return event_image 


Cp, Cn = 0.1, 0.1
refractory_period = 1e-4
log_eps = 1e-3
use_log = True
H, W = 180, 240
H, W = 352, 640

image_folder = os.path.join(os.path.dirname(__file__), "data1/images/imgs/")
timestamps_file = os.path.join(os.path.dirname(__file__), "data1/images/timestamps.txt")
save_event_image_folder = os.path.join(os.path.dirname(__file__), "data1/images/event_imgs/")
save_events_folder = os.path.join(os.path.dirname(__file__), "data1/images/")

esim = esim_py.EventSimulator(Cp, 
                              Cn, 
                              refractory_period, 
                              log_eps, 
                              use_log)


esim.setParameters(0.4, 0.4, 0.001, log_eps, use_log)
events = esim.generateFromFolder(image_folder, timestamps_file)


writer_events = csv.writer(open(save_events_folder+"events.txt", 'w'), delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
print("Events will be saved in : "+save_events_folder+"events.txt")
print("Event frames will be saved in : "+save_event_image_folder)

for i in range(0, len(events)):
    data_row = []
    data_row.append(events[i][2])
    data_row.append(int(events[i][0]))
    data_row.append(int(events[i][1]))
    if (events[i][3] == 1):
        data_row.append(1)
    else:
        data_row.append(0)
    writer_events.writerow(data_row)

# Generate event frames
n_ = 500
iterations = int(len(events)/n_)

for ii in range(iterations):
    if ((ii+1)*n_>len(events)):
        event_image = show_events_by_polarity(events[ii*n_:len(events)-1], W, H)
    else:
        event_image = show_events_by_polarity(events[ii*n_:(ii+1)*n_], W, H)
    cv2.imwrite(save_event_image_folder+str(ii).zfill(5)+".png", event_image)
    #imgplot = plt.imshow(event_image)
    #plt.show()


