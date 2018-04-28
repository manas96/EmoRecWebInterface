import sys
import cv2
import random
import math
import numpy as np
import dlib
import itertools
from sklearn.svm import SVC
from sklearn.externals import joblib
import matplotlib.pyplot as plt
from matplotlib import patches
import os
from multiprocessing import Queue
import pickle

def get_landmarks(image):
    detections = detector(image, 1)
    for k,d in enumerate(detections): #For all detected face instances individually
        shape = predictor(image, d) #Draw Facial Landmarks with the predictor class
        xlist = []
        ylist = []
        for i in range(1,68): #Store X and Y coordinates in two lists
            xlist.append(float(shape.part(i).x))
            ylist.append(float(shape.part(i).y))
            
        xmean = np.mean(xlist)
        ymean = np.mean(ylist)
        xcentral = [(x-xmean) for x in xlist]
        ycentral = [(y-ymean) for y in ylist]

        landmarks_vectorised = []
        for x, y, w, z in zip(xcentral, ycentral, xlist, ylist):
            landmarks_vectorised.append(w)
            landmarks_vectorised.append(z)
            meannp = np.asarray((ymean,xmean))
            coornp = np.asarray((z,w))
            dist = np.linalg.norm(coornp-meannp)
            landmarks_vectorised.append(dist)
            landmarks_vectorised.append((math.atan2(y, x)*360)/(2*math.pi))

        data['landmarks_vectorised'] = landmarks_vectorised
    if len(detections) < 1: 
        data['landmarks_vectorised'] = "error"

def getFeed(s):
    try:
        return int(s)
    except ValueError:
        return s

def run(inputCamera, fSkip):
    dirname, filename = os.path.split(os.path.abspath(__file__))


    global emotions, data, clf, faceDet, faceDet_two, faceDet_three, faceDet_four, detector, predictor
    emotions = ["anger","disgust", "happiness", "neutral", "sadness", "surprise"] #Emotion list
    data = {}
    clf = joblib.load(dirname + "/data/EmoRecogFacial.pkl")

    faceDet = cv2.CascadeClassifier(dirname + "/data/haarcascade_frontalface_default.xml")
    faceDet_two = cv2.CascadeClassifier(dirname + "/data/haarcascade_frontalface_alt2.xml")
    faceDet_three = cv2.CascadeClassifier(dirname + "/data/haarcascade_frontalface_alt.xml")
    faceDet_four = cv2.CascadeClassifier(dirname + "/data/haarcascade_frontalface_alt_tree.xml")

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(dirname + "/data/shape_predictor_68_face_landmarks.dat")




    # MAIN LOOP

    skipframe=24
    try:
        skipframe = int(fSkip)
    except ValueError:
        pass

    video_capture = cv2.VideoCapture(getFeed(inputCamera)) #Webcam object
    proc_frame = np.zeros((350,350,3), np.uint8)

    frameCounter = []
    angerProb = []
    disgustProb = []
    happinessProb = []
    neutralProb = []
    sadnessProb = []
    surpriseProb = []

    anger_patch = patches.Patch(color='blue', label="Anger")
    disgust_patch = patches.Patch(color='green', label="Disgust")
    happiness_patch = patches.Patch(color='red', label="Happiness")
    neutral_patch = patches.Patch(color='cyan', label="Neutral") 
    sadness_patch = patches.Patch(color='magenta', label="Sadness") 
    surprise_patch = patches.Patch(color='yellow', label="Surprise")




    plt.show()
    plt.legend(handles=[anger_patch, disgust_patch, happiness_patch, neutral_patch, sadness_patch, surprise_patch])

    axes = plt.gca()
    axes.set_xlim(0,100)
    axes.set_ylim(0,100)
    (angL,disL,hapL,neuL,sadL,surpL,) = axes.plot(frameCounter, angerProb,'b-',
                                                 frameCounter, disgustProb,'g-',
                                                 frameCounter, happinessProb, 'r-',
                                                 frameCounter, neutralProb, 'c-',
                                                 frameCounter, sadnessProb, 'm-',
                                                 frameCounter, surpriseProb, 'y-')

    counter = 0

    while True:
       
        counter += 1
        ret, orig_frame = video_capture.read()
        if ret == False:
            break
        if( counter % skipframe == 0):
            frame = orig_frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face = faceDet.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
            face_two = faceDet_two.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
            face_three = faceDet_three.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
            face_four = faceDet_four.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
            if len(face) == 1:
                facefeatures = face
            elif len(face_two) == 1:
                facefeatures = face_two
            elif len(face_three) == 1:
                facefeatures = face_three
            elif len(face_four) == 1:
                facefeatures = face_four
            else:
                facefeatures = ""

            for (x, y, w, h) in facefeatures: #get coordinates and size of rectangle containing face
                frame = frame[y:y+h, x:x+w] #Cut the frame to size
                #CHECK IF RESIZING IS NEEDED
                try:
                    frame = cv2.resize(frame, (350, 350)) #Resize face so all images have same size
                except:
                    pass #If error, pass file
            
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            clahe_image = clahe.apply(frame)

        
            get_landmarks(clahe_image)

            if data['landmarks_vectorised'] == "error":
                print("No face detected")
            else:
                pred = []
                pred.append(data['landmarks_vectorised'])
                npar = np.array(pred)
                dist = clf.decision_function(npar)
                result = emotions[clf.predict(npar)[0]]
                prob = clf.predict_proba(npar) * 100
                # print("dist : " + str(dist))
                print("prob : " + str(prob) + "%")
                print("frame : " + str(counter/skipframe) + ", emotion : " + result)

                ##############
                #### PLOT ####
                ##############
            
                 #sending data to webpage
                #["anger","disgust", "happiness", "neutral", "sadness", "surprise"]
                transmitArray = prob[0][0], prob[0][1], prob[0][2], prob[0][3], prob[0][4], prob[0][5], counter/skipframe
                #                   a           d           h                n         sad          sur     frame

                with open('testfile', 'wb') as fp:
                    pickle.dump(transmitArray, fp)
                #------------------------------


                frameCounter.append(counter/skipframe)
                angerProb.append(prob[0][0])
                disgustProb.append(prob[0][1])
                happinessProb.append(prob[0][2])
                neutralProb.append(prob[0][3])
                sadnessProb.append(prob[0][4])
                surpriseProb.append(prob[0][5])

                angL.set_xdata(frameCounter)
                angL.set_ydata(angerProb)
                
                disL.set_xdata(frameCounter)
                disL.set_ydata(disgustProb)
            
                hapL.set_xdata(frameCounter)
                hapL.set_ydata(happinessProb)
            
                neuL.set_xdata(frameCounter)
                neuL.set_ydata(neutralProb)
            
                sadL.set_xdata(frameCounter)
                sadL.set_ydata(sadnessProb)
            
                surpL.set_xdata(frameCounter)
                surpL.set_ydata(surpriseProb)

            
                plt.draw()
                plt.pause(1e-17)
                
            proc_frame = frame
            cv2.putText(proc_frame, "frame : "+str(counter/skipframe), (30,30), cv2.FONT_HERSHEY_PLAIN, 1.5, 255)
            
            
        cv2.imshow("original_feed", orig_frame) #Display the frame
        cv2.imshow("processed_feed", proc_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break        


if __name__ == '__main__':
    run(sys.argv[1],sys.argv[2])