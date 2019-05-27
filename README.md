# Hardware-abstraction-minor-AR
Repository for the course hardware abstraction of the minor AR

The tasks depends on two arduinos with a LED attached on pin 11. One arduino should have a potentiometer attached to pin A0.
The other arduino should have a servo attached on pin 9.

## Task 1

For task 1 the **potentiometer** should provide the angle for the **servo**.
The maximum angle of the **potentiometer** is the maximum angle of the **servo**.
The intensity of the **LED on device a** should be proprotionally to increasing the value of the **potentiometer**.
The intensity of the **LED on device b** should be the opposite, the intensity should decrease when the value of the **potentiometer** is increased
THe arduinos should communicate through a laptop running ROS and with topics.

## Task 2

For taks 2 the abstraction is the same as with task 1.
The **LED on device a** should turn on when the **potentiometer** has reached 90% of the maximum value or higher.
The **LED on device a** should turn of when 10% or less then the maximum value is reached.
The **LED on device b** should do the opposite of the LED attached on device a.
It should turn on when 10% or less of the maximum is reached,and it should turn off when 90% or higher is reached.
When 90% or higher is reached the **servo** should go to the maximum angle.
If 10% or less is reached the **servo** should go to minimal angle.
This should be done using services.
