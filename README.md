
# Automatic Waste Segregator
<a href="mailto:dev.dibyo@gmail.com"> ![Ask Me Anything](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg?longCache=true&style=plastic)</a> [![made-with-python](https://img.shields.io/badge/Made%20with-Python-blue.svg?longCache=true&style=plastic)](https://www.python.org/) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg?longCache=true&style=plastic)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE) ![PyPI - Status](https://img.shields.io/pypi/status/Django.svg?style=plastic) <a href="https://github.com/boudhayan-dev/Automatic-Waste-Segregator/graphs/contributors">![Contributor](https://img.shields.io/badge/Contributors-3-orange.svg?longCache=true&style=plastic)</a>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;<a href="https://github.com/boudhayan-dev/Automatic-Waste-Segregator/tree/v.01"><img src="https://img.shields.io/badge/Version-0.1-brightgreen.svg?longCache=true&style=for-the-badge"></a>&emsp;<a href="https://github.com/boudhayan-dev/Automatic-Waste-Segregator/tree/v.02"><img src="https://img.shields.io/badge/Version-0.2-red.svg?longCache=true&style=for-the-badge"></a>
<br>

###### Welcome to the Automatic Waste Segregator project !
<p>
	In today's world, it is important that waste items are treated properly before they are dumped into landfills for decomposition. For efficient decomposition, proper segregation needs to take place. Current waste management practices involve sorting the waste materials in the central facility. If the sorting procedure takes place at the source of garbage production, then their efficiency will increase a lot. However, relying on human beings to segregate their waste items does not work well in the long run as human beings are lazy and become complacent with time. Therefore, an automatic solution is proposed that can perform the task of segregation with great accuracy, without human assistance.<br><br>
	Automatic Waste Segregator is a portable waste segregator system that identifies and separates waste materials into biodegradable and non-biodegradable categories. It uses Machine Learning to identify the type of waste. The entire system is operated using Raspberry Pi 3 developement board. Additional feature of remote monitoring is also implemented. The sys admin can monitor multiple devices and the type of waste processed by them in real-time, using a web application. 
	<br><br>
	The interacting subsystems are as follows:
	<br><br>
	<span>&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;</span>
	<img src="images/block_diagram.JPG" align="center" height="400px" width="500px">

</p>
<br>

## Dependency


##### Hardware Requirements:


- Raspberry Pi 3B.
- Pi Camera.
- PCA9685 servo motor driver.
- MG995 servo motor.
- IR sensors x2.
- 16x2 LCD display module.
- Power supply - 5V,2A.


##### Software Requirements:


- Python 3.
- Python Dependencies:
    - Rpi.GPIO
	- picamera library.
	- OpenCV.
	- Flask.
	- multiprocessing, multithreading.
	- google-cloud.
	- time.
	- os.
	- socket
- Twilio SMS API.
- Google Cloud VM.
- Tensorflow for Poets.


<br>

## Releases

There are 2 versions of the system:<br>

<table align="center">
	<tr>
		<td width="400px">&emsp;&emsp;&emsp;&emsp;&emsp;<a href="https://github.com/boudhayan-dev/Automatic-Waste-Segregator/tree/v.01"><img src="images/v1.0.jpeg" height="200px" width="160px"></a></td>
		<td width="600px">
			&emsp;&emsp;<a href="https://github.com/boudhayan-dev/Automatic-Waste-Segregator/tree/v.01">Version 0.1</a><br><br>
			<ul>
				<img src="images/checked.png"> Segreagtes waste into 2 categories.<br>
				<img src="images/checked.png"> Provides Live monitoring via Web Application.<br>
				<img src="images/checked.png"> User Notification via SMS.
			</ul>
		</td>
	</tr>
	<tr>
		<td width="400px">&emsp;&emsp;&emsp;&emsp;&emsp;<a href="https://github.com/boudhayan-dev/Automatic-Waste-Segregator/tree/v.02"><img src="images/v2.0.jpeg" height="220px" width="160px"></a></td>
		<td width="600px">
			&emsp;&emsp;<a href="https://github.com/boudhayan-dev/Automatic-Waste-Segregator/tree/v.02">Version 0.2</a><br><br>
			<ul>
				<img src="images/checked.png"> Segreagtes waste into 2 categories.<br>
				<img src="images/checked.png"> Robotic arm that picks up waste by itself.<br>
				<img src="images/checked.png"> Wheels that move the device in a predetermined path.
			</ul>
		</td>
	</tr>
</table>
<br><br>

## Feedback

<table align="center">
	<tr>
		<td width="500px">&emsp;&emsp;&emsp;&emsp;&emsp;<img src="images/feedback1.png" width="280px" height="250px"></td>
		<td width="500px">&emsp;&emsp;&emsp;&emsp;&emsp;<img src="images/feedback2.png" width="280px" height="250px"></td>
	</tr>
	<tr>
		<td width="500px">&emsp;&emsp;&emsp;&emsp;&emsp;<img src="images/feedback3.png" width="280px" height="250px" align="center"></td>
		<td width="500px">&emsp;&emsp;&emsp;&emsp;&emsp;<img src="images/feedback4.png" width="280px" height="250px"></td>
	</tr>
</table>
<br><br>

## Contributors

<table>
	<tr>
		<td><a href="https://github.com/boudhayan-dev"><img src="images/contributor1.png"></a></td>
		<td><a href="https://github.com/chinmay4382"><img src="images/contributor2.png"></a></td>
	</tr>
	<tr>
		<td><a href="https://www.linkedin.com/in/aishwarya-h-s-9b0b6a126/"><img src="images/contributor3.png"></a></td>
		<td><a href="https://github.com/aditya2301"><img src="images/contributor4.png"></a></td>
	</tr>
</table>
<br>

© All rights reserved.

