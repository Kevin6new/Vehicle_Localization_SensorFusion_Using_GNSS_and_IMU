import matplotlib.pyplot as plt
import pandas as pd
from pylab import *
from scipy import *
from scipy import *
import numpy as np
import seaborn as sb

fixed_df=pd.read_csv(r'/home/kevin32/catkin_ws/src/lab4/boston_tour-imu.csv')
magx_obtained=fixed_df['.MagField.magnetic_field.x'].to_numpy()
magy_obtained=fixed_df['.MagField.magnetic_field.y'].to_numpy()
time = fixed_df[".Header.stamp.secs"].to_numpy()
time=time-time[0]
sb.set_theme(style="darkgrid")
sb.set_palette("dark")
	
x_max=max(magx_obtained)
y_max=max(magy_obtained)
x_min=min(magx_obtained)
y_min=min(magy_obtained)

avg_delta_x =(x_max-x_min)/2
avg_delta_y =(y_max-y_min)/2
avg_delta=(avg_delta_x+avg_delta_y)/2

scale_x=avg_delta/avg_delta_x
scale_y=avg_delta/avg_delta_y

Xoffset=(x_max+x_min)/2 
Yoffset=(y_max+y_min)/2

magx_correct=magx_obtained
magy_correct=magy_obtained

magx_correct=magx_obtained-Xoffset
magx_correct=magx_correct*scale_x

magy_correct=magy_obtained-Xoffset
magy_correct=magy_correct*scale_y

obtained_yaw=np.arctan2(np.negative(magy_obtained), magx_obtained)
obtained_yaw_rad=np.unwrap(obtained_yaw)

correct_yaw=np.arctan2(np.negative(magy_correct), magx_correct)
correct_yaw_rad=np.unwrap(correct_yaw)

ax=plt.subplots()
ax=sb.lineplot(x=time,y=obtained_yaw_rad,label='Raw Yaw Angle',errorbar=None)
ax=sb.lineplot(x=time,y=correct_yaw_rad,label='Corrected Yaw Angle',color='#ffb400',errorbar=None)

plt.xlabel('Time(s)')
plt.ylabel('Yaw Angle(rad)')
plt.title('Raw Magnetometer Yaw & Corrected Magnetometer Yaw vs Time')
plt.legend()
plt.show()


ang_z=fixed_df['.IMU.angular_velocity.z']
gyro_yaw=integrate.cumtrapz(ang_z,time)
gyro_yaw=np.append(gyro_yaw,gyro_yaw[0])

ad=plt.subplots()
ad=sb.lineplot(x=time,y=correct_yaw, label='Magnetometer Yaw',color='black',errorbar=None) 
ad=sb.lineplot(x=time,y=gyro_yaw, label='Integrated Yaw from Gyro',color='#b30000',errorbar=None)

plt.xlabel('Time(s)')
plt.ylabel('Yaw Angle(rad)')
plt.legend()
plt.title('Magnetometer Yaw & Yaw Integrated from Gyro')

Fs=40
Fs_off=1/(Fs*5)
a,b=signal.butter(1,Fs_off)
yaw_filt_low=signal.filtfilt(a,b,gyro_yaw)
yaw_filt_low=np.append(yaw_filt_low,yaw_filt_low[0])

Fs_off=1/(Fs*0.5)
a,b= signal.butter(1,Fs_off)
yaw_filt_high= signal.filtfilt(a,b,gyro_yaw)
yaw_filt_high=np.append(yaw_filt_high,yaw_filt_high[0])
comp_filt_yaw= np.array(yaw_filt_low[:-1])*.2+np.array(gyro_yaw)*.8

au=plt.subplots()
au=sb.lineplot(x=time,y=(gyro_yaw+0.2),label='Yaw Obtained from IMU',color="#b04238",errorbar=None)
au=sb.lineplot(x=time,y=comp_filt_yaw,label='Complementary Filter Yaw',color='blue',errorbar=None) 
plt.legend()
plt.xlabel('Time(s)')
plt.ylabel('Yaw angle in radians')
plt.title('IMU yaw  vs. complimentory filter result')
plt.show()















