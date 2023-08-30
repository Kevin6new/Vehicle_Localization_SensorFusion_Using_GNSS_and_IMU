import matplotlib.pyplot as plt
import pandas as pd
from pylab import *
from scipy import *
from scipy import *
import numpy as np
import seaborn as sb

fixed_df=pd.read_csv(r'/home/kevin32/catkin_ws/src/lab4/boston_tour-imu.csv')
unfix_df=pd.read_csv(r'/home/kevin32/catkin_ws/src/lab4/boston_tour-gps.csv')

east=unfix_df['.UTM_easting'].to_numpy()
north=unfix_df['.UTM_northing'].to_numpy()

acc_x=fixed_df['.IMU.linear_acceleration.x'].to_numpy()
acc_x=acc_x-acc_x[0]

time=unfix_df[".Header.stamp.secs"].to_numpy()
time=time-time[0]
timed=fixed_df[".Header.stamp.secs"].to_numpy()


imu_speed=integrate.cumtrapz(timed,acc_x)
imu_speed=imu_speed-imu_speed[0]
imu_speed=np.append(imu_speed,imu_speed[0])
timed=timed-timed[0]
gps_speed=[]

sb.set_theme(style="darkgrid")
sb.set_palette("dark")

for i in range(len(time)-1):
	if((time[i]-time[i+1])==0):
		gps_speed.append(0)
	else:
		gps_speed.append((math.sqrt(pow((east[i]-east[i+1]),2) + pow((north[i]-north[i+1]),2)))/(time[i]-time[i+1]))

gps_speed=np.array(gps_speed) 
gps_speed=np.append(gps_speed,gps_speed[0])

plt.figure()
plt.plot(timed,imu_speed, label='Estimated velocity from IMU',color='#22a7f0') 
sb.lineplot(x=time,y=-(gps_speed), label='Estimated velocity from GPS',color='#de6e56',errorbar=None)
plt.xlabel('Time(s)')
plt.ylabel('Velocity(m/s)')
plt.legend()
plt.title('Velocity vs Time')
plt.show()

imu_speed=integrate.cumtrapz(timed,acc_x)
imu_speed=imu_speed-imu_speed[0]
imu_speed=np.append(imu_speed,imu_speed[0])
imu_speed=imu_speed-np.mean(imu_speed)

plt.figure()
sb.lineplot(x=timed,y=imu_speed,label='Intergrated velocity from IMU',color='#c80064',errorbar=None)
plt.plot(time,-(gps_speed), label='Estimated velocity from GPS',color='#de6e56') 
plt.xlabel('Time(s)')
plt.ylabel('Velocity(m/s)')
plt.legend()
plt.title('Velocity vs Time after Adjustment')

cFit=np.polyfit(timed,imu_speed, 2);
x_Val=np.linspace(min(imu_speed), max(imu_speed),50897);
y_VAl=np.polyval(cFit,x_Val);
yDiff=imu_speed-y_VAl

plt.figure()
sb.lineplot(x=timed,y=yDiff, label='Intergrated velocity from IMU',color='green',errorbar=None)
sb.lineplot(x=x_Val,y=y_VAl, label='Best Fit Line used for Adjustment',color='yellow',errorbar=None)
plt.plot(time,-(gps_speed), label='Estimated velocity from GPS',color='#de6e56') 
plt.xlabel('Time(s)')
plt.ylabel('Velocity(m/s)')
plt.legend()
plt.title('Velocity vs Time after Adjustment')
plt.show()
























