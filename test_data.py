# bigdata warehouse

import numpy as np
import pandas as pd
from funclib import find_repeat, locOutFac

#data = pd.read_csv('Report_3_5_2020__3_18_2020.csv')
#data = pd.read_csv('Report_3_19_2020__3_22_2020.csv')
data = pd.read_csv('Report_3_25_2020__3_26_2020.csv')


# 0 - 6
do = np.array([
    # 3
    data['PlantDO.PLCB.Tank3.Grid3.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank3.Grid4.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank3.Grid5.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank3.Grid6.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank3.Grid7.DO.MeterReadings'],
    # 4
    data['PlantDO.PLCB.Tank4.Grid3.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank4.Grid4.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank4.Grid5.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank4.Grid6.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank4.Grid7.DO.MeterReadings'],
    # 5
    data['PlantDO.PLCB.Tank5.Grid3.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank5.Grid4.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank5.Grid5.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank5.Grid6.DO.MeterReadings'],
    data['PlantDO.PLCB.Tank5.Grid7.DO.MeterReadings'],])


# 0 - 100
airflow = np.array([
    # 3
    data['PlantDO.PLCB.Tank3.Grid3.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank3.Grid4.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank3.Grid5.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank3.Grid6.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank3.Grid7.Airflow.MeterReadings'],
    # 4
    data['PlantDO.PLCB.Tank4.Grid3.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank4.Grid4.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank4.Grid5.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank4.Grid6.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank4.Grid7.Airflow.MeterReadings'],
    # 5
    data['PlantDO.PLCB.Tank5.Grid3.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank5.Grid4.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank5.Grid5.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank5.Grid6.Airflow.MeterReadings'],
    data['PlantDO.PLCB.Tank5.Grid7.Airflow.MeterReadings'],])


# 0 - 600~800
valvePosition = np.array([
    # 3
    data['PlantDO.PLCB.Tank3.Grid3.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank3.Grid4.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank3.Grid5.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank3.Grid6.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank3.Grid7.Airflow.ValvePositionReadings'],
    # 4
    data['PlantDO.PLCB.Tank4.Grid3.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank4.Grid4.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank4.Grid5.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank4.Grid6.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank4.Grid7.Airflow.ValvePositionReadings'],
    # 5
    data['PlantDO.PLCB.Tank5.Grid3.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank5.Grid4.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank5.Grid5.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank5.Grid6.Airflow.ValvePositionReadings'],
    data['PlantDO.PLCB.Tank5.Grid7.Airflow.ValvePositionReadings'],])

# specially for endless iteration
all = np.concatenate([do, airflow, valvePosition])

find_repeat(all[-15])
