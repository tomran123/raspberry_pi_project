mycar.py is a program written by me in raspberry pi. In this program, the car can carry out functions such as movement, intelligent driving, and infrared obstacle avoidance. All functions are realized through buttons. I will introduce all the functions in this readme file. Functions:

1. The initial speed of the car is 40. The up key on the keyboard can increase the speed by 10 and the down key can decrease the speed by 10.

2. The w key controls the car to move forward, the a key controls the car to turn counterclockwise, the d key controls the car to turn clockwise, the s key controls the car to move backward, the q key controls the car to move forward to the left, the e key controls the car to move forward to the right, and the z key Control the car to go to the left and rear, the c key controls the car to go to the right and rear, the t key controls the car to go to the left, and the u key controls the car to go to the right.

3. The car's camera has four modes. Press the number 1 button for the original camera, the number 2 button for the black and white image, the number 3 button for the binary image, and the number 4 button for the final image based on the binary image. The upper third of the image is painted black, which is also the image used by the car's first intelligent driving mode to determine the direction.

4. Press the numeric key 0 to turn on the first intelligent driving mode of the car. The principle is to analyze the binary image in the fourth mode and compare the white areas of the left and right images to determine whether to turn left or right. Or move forward; it is also equipped with infrared obstacle avoidance. When an obstacle is detected in front, the car will stop until the obstacle disappears.

5. Press the numeric key 9 to turn on the car’s second intelligent driving mode, deep learning. In this mode, we collected 4,000 training sets and 1,000 test set data, and conducted nearly 100 rounds of training, with an accuracy rate of 91%; It is also equipped with infrared obstacle avoidance.

6. Press the c key to take pictures, the esc key to exit the program, and the p key to turn on/off the camera.

   
mycar.py是raspberry pi里面的一个我编写的程序，在这个程序里，小车可以进行移动，智能驾驶，红外避障等功能，所有的功能是通过按键实现的，这个readme文件里我介绍一下所有的功能：

1.车的初始速度是40, 键盘的上键可以让速度增加10，下键速度减少10。

2.w键控制小车前进，a键控制小车逆时针转，d键控制小车顺时针转，s键控制小车后退，q键控制小车向左前方走，e键控制小车向右前方走，z键控制小车向左后方走，c键控制小车向右后方走，t键控制小车向左走，u键控制小车向右走。

3.小车的摄像头有四种模式，按数字1键是原摄像头，数字2键是黑白图像，数字3键是经过二值化的图像，数字4键是在二值化的基础上，将最上面三分之一的图像涂成黑色的图像，也是小车第一种智能驾驶模式进行判断方向的图像。

4.按数字键0开启小车的第一种智能驾驶模式，原理是通过分析第4种模式下二值化的图像，比较左边和右边图像白色的面积，从而判断应该是左转，右转，还是前进；同时还配备了红外避障，当检测出前方有障碍物时，小车会停下直到障碍物消失。

5.按数字键9开启小车的第二种智能驾驶模式，深度学习，这个模式我们收集了4000个训练集和1000个测试集数据，并且进行了近100轮的训练，正确率为91%；同时也配备了红外避障。

6.按c键可以进行拍照，esc键可以退出程序，p键可以打开/关闭摄像头
