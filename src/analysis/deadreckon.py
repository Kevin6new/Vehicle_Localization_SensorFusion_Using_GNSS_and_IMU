import pandas as pd
from pylab import *
from scipy import *
import numpy as np
import seaborn as sb

fixed_df=pd.read_csv(r'/home/kevin32/catkin_ws/src/lab4/boston_tour-imu.csv')
unfix_df=pd.read_csv(r'/home/kevin32/catkin_ws/src/lab4/boston_tour-gps.csv')

magx_obtained=fixed_df['.MagField.magnetic_field.x'].to_numpy()
magy_obtained=fixed_df['.MagField.magnetic_field.y'].to_numpy()

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

east=unfix_df['.UTM_easting']
east=east-east[0]
north=unfix_df['.UTM_northing']
north=north-north[0]

acc_x=fixed_df['.IMU.linear_acceleration.x'].to_numpy()
acc_x=acc_x-acc_x[0]

acc_y=fixed_df['.IMU.linear_acceleration.y'].to_numpy()
acc_y=acc_y-acc_y[0]

time=unfix_df[".Header.stamp.secs"].to_numpy()
time=time-time[0]
timed=fixed_df[".Header.stamp.secs"].to_numpy()
timed=timed-timed[0]

gyr_z=fixed_df['.IMU.orientation.z'].to_numpy()
gyr_z=gyr_z-gyr_z[0]
vel_x=integrate.cumtrapz(timed,acc_x)
vel_y=integrate.cumtrapz(timed,acc_y)

Fs=40
Fs_off=1/Fs
a,b=signal.butter(1,Fs_off)
filt_vel_x=signal.filtfilt(a,b,acc_x)
filt_vel_y=signal.filtfilt(a,b,acc_y)

sb.set_theme(style="darkgrid")
sb.set_palette("dark")

cal_acc_y=gyr_z*filt_vel_x

plt.figure()
sb.lineplot(x=timed,y=cal_acc_y, label='Calculated y-acceleration',color='#48b5c4',errorbar=None)
sb.lineplot(x=timed,y=acc_y, label='Observed y-acceleration',color='#b04238',errorbar=None)
plt.xlabel("Time(s)")
plt.ylabel('Acceleration (m/s2)')
plt.title("Comparing wX' and y acceleration")
plt.legend()
plt.show()
vel_x=np.append(vel_x,vel_x[0])
vel_y=np.append(vel_y,vel_y[0])

y_calc=np.multiply(vel_y,np.cos((correct_yaw_rad)))
x_calc= np.multiply(vel_x,np.sin((correct_yaw_rad)))

x=integrate.cumtrapz((x_calc),timed)
y=integrate.cumtrapz((y_calc),timed)

x=x-x[0]
y=y-y[0]

plt.figure()
sb.scatterplot(x=east,y=north,label='Gps Path',color='#48b5c4')
sb.scatterplot(x=x,y=y,label='Path Calculated from IMU',color='#b04238')
plt.xlabel("Easting(m)")
plt.ylabel('Northing(m)')
plt.title("Comparing path between GPS and IMU")
plt.legend()
plt.show()








































