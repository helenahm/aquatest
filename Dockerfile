FROM python:3.7 
ADD ./aquatech_bonus.py .
ADD ./aquatech_maintask.py .
ADD ./DB/sensors.csv .
ADD ./DB/records.csv .
RUN pip install pandas==1.3.5 numpy==1.20.2 pytz==2020.1 pandarallel==1.6.5 matplotlib==3.2.2
#CMD [“python”, “./aquatech3.py”]