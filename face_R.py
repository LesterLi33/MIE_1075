
import face_recognition
import cv2
import os
import numpy as np
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
work_dir="D:/graduate/mie1075/"
# Load a sample picture and learn how to recognize it.
# zicheng_image = face_recognition.load_image_file(work_dir+"known people/zicheng wang.jpg")
# zicheng_face_encoding = face_recognition.face_encodings(zicheng_image)[0]
# Path to the folder containing your images
image_folder = "D:/graduate/mie1075/known people"
known_face_encodings =[]
known_face_names = []
# Loop through all files in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(('.jpg', '.png', '.jpeg')):  # check if the file is an image
        # Construct the full image path
        image_path = os.path.join(image_folder, filename)
        
        # Load the image file
        image = face_recognition.load_image_file(image_path)
        
        # Find all face locations in the image
        # face_locations = face_recognition.face_locations(image)
        known_face_encodings.append(face_recognition.face_encodings(image)[0])
        print(filename.split('.')[0])
        known_face_names.append(filename.split('.')[0])
print(len(known_face_names))
        
# Create arrays of known face encodings and their names
# known_face_encodings = [
#     zicheng_face_encoding
    
# ]
# known_face_names = [
#     "Zicheng Wang"
    
# ]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            threshold = 0.35  # Adjust the threshold value to suit your needs
            print(face_distances[best_match_index])
            if face_distances[best_match_index] <= threshold:
            # If the distance is within the threshold, it's considered a match
                name = known_face_names[best_match_index]


            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)
    
    # get key
    key = cv2.waitKey(1) & 0xFF
    # Hit 'q' on the keyboard to quit!
    if key == ord('q'):
        break

    # Hit 'space' on the keyboard to save image!
    if key == ord(' '):
        #new_image = face_recognition.load_image_file("known people/zicheng.jpg")
        ret, frame = video_capture.read()
        while True:
            
            cv2.imshow('Video', frame)
            key = cv2.waitKey(1) & 0xFF

            # Hit 'n' on the keyboard to abandon this frame
            if key == ord('n'):
                break

            # Hit 'y' on the keyboard to use this frame as your picture
            if key == ord('y'):
                name = input("Type your name: ")
                print(name)
                cv2.imwrite(work_dir+'known people/'+name+'.jpg',frame)
                length = len(known_face_encodings)
                known_image = face_recognition.load_image_file(work_dir+'known people/'+name+'.jpg')
                known_face_encod = face_recognition.face_encodings(known_image)[0]
                known_face_encodings.append(known_face_encod)
                known_face_names.append(name)
                break
                
                

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()