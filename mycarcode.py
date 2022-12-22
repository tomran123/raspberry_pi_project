import cv2
import time
import torch
from CAR import CAR
import numpy as np
import infrad_avoid
from tracks_training import Net

# 调用模型，输入原始图片，输出运动状态

def auto_drive_with_nn(image: np.ndarray):
    with torch.no_grad():
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_LINEAR)  # 缩放成 224 * 224
        image = np.transpose(image, (2, 0, 1))  # 将RGB通道移到最前面
        image = image.reshape(1, 3, 224, 224)  # 重塑成 batch_size * channel * width * height 形式
        image = torch.tensor(image / 255, dtype=torch.float).to(device)  # 将值从 0-255 映射到 0-1 并转成 tensor
        outputs = net(image)
        _, predicted = torch.max(outputs.data, 1)
        moving_status = predicted.item()
        return moving_status

if __name__=="__main__":
    infrad_avoid.setup()
    clbrobot = infrad_avoid.LOBOROBOT()
    speed = 40
    tspeed = speed - 0
    car = CAR()
    thresh= 110
    frame_mode = 0
    is_open = True
    is_auto_notopen = True
    is_deeplearning = False
    #car.set_servo_angle(10,0)
    #car.set_servo_angle(9,180)



    device = torch.device("cpu")
    net = Net().to(device)
    net.train(False)
    net.load_state_dict(torch.load(f"parameters/resnet18_e50.pth", map_location=device))




    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("cannot open camera")
        exit()
    is_camera_open = True

    while True:
        SR_2 = infrad_avoid.GPIO.input(infrad_avoid.SensorRight)
        SL_2 = infrad_avoid.GPIO.input(infrad_avoid.SensorLeft)
        if is_camera_open:
            ret, frame=capture.read()
            if not ret:
                print("cannot recieve a frame")
                break
        height, width,_ = frame.shape

        grayframe = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        ret, bwframe = cv2.threshold(grayframe, thresh, 255, cv2.THRESH_BINARY)
        clean_frame = cv2.dilate(bwframe, (500, 500), iterations=10)
        _, clean_frame = cv2.threshold(clean_frame, thresh, 255, cv2.THRESH_BINARY)
        clean_frame = cv2.erode(clean_frame, (300, 300), iterations=10)
        clean_frame[:height // 3, :] = 0


        if frame_mode >= 1 or frame_mode < 1:
            outputframe=frame
        if frame_mode >= 2:
            outputframe= grayframe
        if frame_mode >= 3:
            outputframe= bwframe
        if frame_mode >=4:
            outputframe = clean_frame


            
          #文字+线
        if is_open:
            text_image = cv2.putText(outputframe, "speed=%d" %speed, (31,47), cv2.FONT_HERSHEY_SIMPLEX,
                                     1, (0, 0, 255), 2) #放的位置，字体，字体大小，颜色，厚度
            #cv2.line(text_image, (0,height//2), (width, height//2), (255, 0, 0), 2)
            #cv2.line(text_image, (width//2, 0), (width//2, height), (255, 0, 0), 2)
            cv2.imwrite("photos/5_text.jpg", text_image)
    
            
            
        cv2.imshow("camera",outputframe)
        key = cv2.waitKey(1)
        if key == ord("9"):
            is_deeplearning = not is_deeplearning
        if key == ord("0"):
            is_auto_notopen = not is_auto_notopen
        if ord("1") <= key <= ord("8"):
            frame_mode = key - 48
        if key == ord("j"):
            thresh -= 10
        if key == ord("k"):
            thresh +=10
        if key == 82:
            speed = speed + 10
        if key == 84:
            speed = speed - 10


        #深度学习
        if is_deeplearning is True:
            moving_status = auto_drive_with_nn(frame)

            if moving_status == 0:
                car.turn_right(speed, 0)
            elif moving_status == 1:
                car.t_down(speed,0)
            elif moving_status == 2:
                car.turn_Left(speed, 0)
            continue


        #自动驾驶
        if is_auto_notopen is False:
            if SL_2 == False or SR_2 == False:
                car.t_stop(0)
            else:
                n_left_bottom_black = np.sum(clean_frame[320:, :320] == 0)
                n_right_bottom_black = np.sum(clean_frame[320:, 320:] == 0)

                if n_left_bottom_black >= 15000:
                    car.turn_Left(tspeed, 0)
                    #cv2.imwrite(time.strftime("2/%Y.%m.%d_%H.%M.%S_2.jpg"), frame)
                    outputframe = cv2.putText(outputframe, f"auto turn right",
                                              (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)

                elif n_right_bottom_black >= 15000:
                    car.turn_right(tspeed, 0)
                    outputframe = cv2.putText(outputframe, f"auto turn left",
                                              (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 3)
                    #cv2.imwrite("./training_tracks/1/{}.jpg".format(time.time()), frame)
                else:
                    car.t_down(speed, 0)

                    #cv2.imwrite(time.strftime("0/%Y.%m.%d_%H.%M.%S_0.jpg"), frame)
                    outputframe = cv2.putText(outputframe, f"auto move forward",
                                              (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            continue

        if key == -1:
            continue
        print(key)
        


        if key == ord("y"):
            is_open = not is_open
     

        if key == ord("p"):
            is_camera_open = not is_camera_open


        if key == ord("w"):
            print("press w ")
            car.t_down(speed, 0)
            #cv2.imwrite(time.strftime("./training_tracks/1/%Y.%m.%d_%H.%M.%S.%02d_0.jpg"), frame)
            #cv2.imwrite("./training_tracks/1/{}.jpg".format(time.time()), frame)
        if key == ord("a"):
            print("press a")
            car.turn_right(speed, 0)
            #cv2.imwrite(time.strftime("./training_tracks/0/%Y.%m.%d_%H.%M.%S.%02d_0.jpg"), frame)
            #cv2.imwrite("./training_tracks/0/{}.jpg".format(time.time()), frame)
        if key == ord("s"):
            print("press s")
            car.t_up(speed, 0)
        if key == ord("d"):
            print("press d")
            car.turn_Left(speed, 0)
            #cv2.imwrite(time.strftime("./training_tracks/2/%Y.%m.%d_%H.%M.%S.%02d_0.jpg"), frame)
            #cv2.imwrite("./training_tracks/2/{}.jpg".format(time.time()), frame)
        if key == ord(" "):
            print("press space")
            car.t_stop(0)
        if key == ord("q"):
            print("press q")
            car.backward_right(speed, 0)
        if key == ord("e"):
            print("press e")
            car.backward_left(speed, 0)
        if key == ord("z"):
            print("press z")
            car.forward_right(speed, 0)
        if key == ord("c"):
            print("press c")
            car.forward_left(speed, 0)
        if key == ord("t"):
            print("press right botton")
            car.move_left(speed, 0)
        if key == ord("u"):
            print("press left botton")
            car.move_right(speed, 0)










        if key == ord("c"):
            filename = time.strftime("%Y.%m.%d_%H.%M.%S.jpg")
            cv2.imwrite(filename,outputframe)
        if key == 27:
            break


    capture.release()
    cv2.destroyAllWindows()