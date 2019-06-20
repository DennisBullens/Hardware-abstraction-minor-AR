# Hardware-abstraction-minor-AR
Repository for the course hardware abstraction of the minor AR

The tasks depends on two arduinos with a LED attached on pin 11.
One arduino should have a potentiometer attached to pin A0 (this is going to be **device A**).
The other arduino should have a servo attached on pin 9 (this is going to be **device B**).

## Task 1

For task 1 the **potentiometer** should provide the angle for the **servo**.
The maximum angle of the **potentiometer** is the maximum angle of the **servo**.
The intensity of the **LED on device A** should be proprotionally to increasing the value of the **potentiometer**.
The intensity of the **LED on device B** should be the opposite, the intensity should decrease when the value of the **potentiometer** is increased
THe arduinos should communicate through a laptop running ROS and with topics.

## Task 2

For task 2 the abstraction is the same as with task 1.
The **LED on device A** should turn on when the **potentiometer** has reached 90% of the maximum value or higher.
The **LED on device A** should turn of when 10% or less then the maximum value is reached.
The **LED on device B** should do the opposite of the LED attached on device a.
It should turn on when 10% or less of the maximum is reached,and it should turn off when 90% or higher is reached.
When 90% or higher is reached the **servo** should go to the maximum angle.
If 10% or less is reached the **servo** should go to minimal angle.
This should be done using services.

## Task 3

For task 3 the abstraction is different then the previous tasks.
**Device A** is normally not used in task 3, but it can be used. You should just comment and uncomment some lines in the actionclient.
**Device B** exists only of a **servo** which is controlled by the arduino.
The purpose of task 3 is to control the **servo** with the ros action library.
Since we couldn't use a action library in arduino, the arduino communicates with a python file thanks to subscribing and publishing to this python node.
In the client is a line to fill in the desired angle in the terminal. When you press enter after you have filled in the angle it waits till you press ENTER again. After this the **servo** will go to the desired angle.
