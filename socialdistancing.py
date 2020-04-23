#!/usr/bin/env 
import cv2
import numpy as np
import requests
ip_request = requests.get('https://get.geojs.io/v1/ip.json')
my_ip = ip_request.json()['ip']  # ip_request.json() => {ip: 'XXX.XXX.XX.X'}
geo_request_url = 'https://get.geojs.io/v1/ip/geo/' + my_ip + '.json'
geo_request = requests.get(geo_request_url)
geo_data = geo_request.json()
print(geo_data)
import geocoder
g = geocoder.ip('me')
print(g.latlng)
#from geolocation.main import GoogleMaps
#from geolocation.distance_matrix.client import DistanceMatrixApiClient
#google_maps = GoogleMaps(api_key="AIzaSyD92L-EVe-FNGj7wpqyFJVGbkXJwoEkX0o")
#my_location = location.first() # returns only first location.

#print(my_location.city)
#print(my_location.route)
#print(my_location.street_number)
#print(my_location.postal_code)


#for administrative_area in my_location.administrative_area:
#print(“{}: {} ({})”.format(administrative_area.area_type,
#administrative_area.name, administrative_area.short_name))
#print(my_location.country) print(my_location.country_shortcut)

#print(my_location.formatted_address)

#print(my_location.lat) print(my_location.lng)
# reverse geocode

#lat = 40.7060008 lng = -74.0088189

#my_location = google_maps.search(lat=lat, lng=lng).first()
#changing -----------PARAMETERS----------- according to camera height
motion_area=250#900 for common 250 vtest1
crowd_area=450 #above number 2500 vtest 1500vtest2 700/450vtest1
crowdwidth,crowdheight = (8,8)    #w,h 8 vtest1 50 others 150 vtest
person_distance=  8 #vtest 60 vtest2 75 vtest1 10
area_test=[]
#yet to find exact relation--------END---------
#testing parameters
#y,u,j,p=(0,0,0,0)
#end of testing

#print(y)
#y=y+1
cap = cv2.VideoCapture('vtest1.mp4')
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter("output.mp4", fourcc, 5.0, (1280,720))
#newly added
x,y,w,h,c=(0,0,0,0,0)
#end
ret, frame1 = cap.read()
ret, frame2 = cap.read()
#newly added
def distance(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5
#end
#print(frame1.shape())
#for timestamp

#for timestamp end
while cap.isOpened():
    #print(u)
    #u=u+1
    l=[]
    m=[]
    n=[]
    try:
        diff = cv2.absdiff(frame1, frame2)
    except:
        print("Video complted")
        break
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        #print(j)
        #j=j+1
        if cv2.contourArea(contour) < motion_area:
            area_test.append(cv2.contourArea(contour))
            continue
        if cv2.contourArea(contour) > crowd_area:#please find the best possible number
        
            if w<crowdwidth and h<crowdheight : 
                pass        
            else:
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 0, 255), 2)
                # millis = cap.get(cv2.CV_CAP_PROP_POS_MSEC)
                #print(millis)
        else:
            pass
            cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2) 
        mid = (int((x+x+w)/2),int((y+y+h)/2))
        l.append(mid)
        cv2.putText(frame1, "Status: {}".format('Movement min. trigger 60px'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 3)
        #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
    for i in range(0,len(l)):
        for j in range(0,len(l)):
            if((i==j)):
                pass
            else:
                #print(p)
                #p=p+1
                #frame1=cv2.line(frame1,l[i],l[j],[0,255,0],1)
                n.append((i,j))
                m.append(distance(l[i],l[j]))
                if(min(m)<person_distance): 
                    c=m.index(min(m))
                    frame1=cv2.line(frame1,l[n[c][0]],l[n[c][1]],[255,0,0],2)
    image = cv2.resize(frame1, (1280,720))
    out.write(image)
     
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 13:
        cap.release()
        break
print(area_test)
#if(cv2.waitKey()==13):
    #cap.release()
out.release()
cv2.destroyAllWindows()
#cap.release()
#out.release()
