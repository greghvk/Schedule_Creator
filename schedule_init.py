import numpy as np
import pandas as pd
get_ipython().run_line_magic('matplotlib', 'inline')
import docx

import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')

    #every worker has preferences for specific shift (default range is 0.9 to 1.1)
def generate_preferences():
    pref_spectrum = [0.9, 1, 1.1]
    pref = np.zeros((len(workers[0]), 3))
    for i in range(0, len(workers[0])):
        pref[i]=np.random.permutation(pref_spectrum)
    return np.tile(pref,days_in_interval)


    #generowanie macierzy dostępności pracowników (każdy może wybrać 9 niedostępnych zmian w miesiącu)
    
def verify_availability(grafik):
    freeDays = grafik.shape[0]-grafik.sum(axis=0)
    
    for i in freeDays:
        if i == 0: return 0 
    return 1
    
def generate_availability():
    availabilties = np.ones(np.shape(schedule))
    for pracownik in range(0,len(workers[0])):
        for i in range(9):
            niedostepna_zmiana = np.random.randint(0, 3*days_in_interval)
            availabilties[pracownik, niedostepna_zmiana]=0
    
    
    return abs(1-availabilties)

def parameters_from_file():
    """TODO possibility to read starting parameters from a file"""
    #Possibility to read starting schedule from a file
    schedule_df = pd.read_csv("./schedule.csv", index_col=0)
    schedule = schedule.as_matrix()
    #Possibility to read worker preferences from a file
    workers_preferences_df = pd.read_csv("workers_preferences.csv", index_col=0)
    workers_preferences = workers_preferences_df.as_matrix()
    #Possibility to read workers availability from a file
    workers_availability_df=pd.read_csv("workers_availability.csv", index_col=0)
    workers_availability = workers_availability_df.as_matrix()
    if(weryfikacjaDostepnosci(workers_availability)==0):
        raise Exception('Pracownicy zablokowali dostepnosc!!!')
#Defining default variables

workers = ['Alice Adam Eve Jenn Jack David Greg Janice Beth Saul'.split()]
shifts = ['E L N'.split()] #Early, late and night shifts
days_in_interval = 30 #Here we will generate Schedule for interval of one month
which_verison = 0 #Variable used by raport generators
estimators = {0:'Gap between shifts',
                 1: 'Required experience per shift',
                 2: 'Too much shifts per interval per worker',
                 3: 'Not enough shifts per interval per worker',
                 4: 'Workers amount per shift',
                 5: 'Workers availability',
                 6: 'Workers satisfaction',
                 7: 'Work frequency'}



      
#experience vector generation (uniform distribution between 0.1 and 0.9)
workers_experience = 0.9*np.random.rand(1, len(workers[0]))+0.1

#required experience per shift generation (uniform distribution between 0.6 and 1.2)
shift_exp_required = 0.6*np.random.rand(1, days_in_interval*3)+0.6

#generate random Schedule (normal distribution with relevant parameters)
schedule = 0.03*np.random.rand(len(workers[0]),3*days_in_interval)+0.48
schedule = schedule.round()
starting_schedule = schedule.copy()


#Create random starting availability
workers_availability = generate_availability()
while verify_availability(workers_availability)==0:
    workers_availability = generate_availability

#Create random starting preferences
workers_preferences = generate_preferences()

#Create df version of parameters
shift_exp_required_df = pd.DataFrame(shift_exp_required)
schedule_df = pd.DataFrame(schedule, index=workers[0])
workers_preferences_df = pd.DataFrame(workers_preferences, index=workers[0])
workers_availability_df = pd.DataFrame(workers_availability, index=workers[0])
workers_experience_df = pd.DataFrame(workers_experience, columns=workers[0])

#Save starting parameters to a file
shift_exp_required_df.to_csv('shift_exp_required.csv')
workers_availability_df.to_csv("workers_availability.csv")
workers_preferences_df.to_csv("workers_preferences.csv")
    