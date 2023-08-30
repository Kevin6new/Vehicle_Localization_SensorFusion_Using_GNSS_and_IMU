import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sb

sb.set_palette("dark")
fixed_df=pd.read_csv(r'/home/kevin32/catkin_ws/src/lab4/circles-imu.csv')
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
sb.scatterplot(data=fixed_df, x=magx_obtained, y=magy_obtained,color='#a57c1b')
plt.xlabel('Magnetometer measurement in X (gauss)')
plt.ylabel('Magnetometer measurement in Y (gauss)')
plt.title('Magnetometer before calibration')
plt.show()

magx_correct=magx_obtained
magy_correct=magy_obtained

magx_correct=magx_obtained-Xoffset
magx_correct=magx_correct*scale_x

magy_correct=magy_obtained-Xoffset
magy_correct=magy_correct*scale_y

sb.scatterplot(x=magx_correct, y=magy_correct,color='#54bebe')
plt.xlabel('Magnetometer measurement in X (gauss)')
plt.ylabel('Magnetometer measurement in Y (gauss)')
plt.title('Magnetometer corrected for Soft Iron and Hard Iron')
plt.show()

