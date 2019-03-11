from schedule_init import *

def check_availability(schedule, availability):
    conflicts = np.logical_and(schedule, availability)
    return sum(sum(conflicts))*10

def check_gaps(schedule):
    penalty = 0
    for worker in range(0,len(workers[0])):
        for day in range(0, days_in_interval*3-2):
            if np.sum(schedule[worker,day:day+3])>1:
                penalty=penalty+10
    return penalty

def check_experience(schedule):
    penalty = 0
    for day in range(0, days_in_interval*3):
        if np.sum(schedule[:,day])<shift_exp_required[0][day]:
            penalty = penalty + (shift_exp_required[0][day]-np.sum(schedule[:,day]))*1
    return penalty*100

def check_max_hours(schedule):
    penalty = 0
    for worker in range(0,len(workers[0])):
        if np.sum(schedule[worker, :])>24:
            penalty = penalty + abs(np.sum(schedule[worker, :])-21)*10
    return penalty*1

def check_min_hours(schedule):
    penalty = 0
    for worker in range(0,len(workers[0])):
        if np.sum(schedule[worker, :])<18:
            penalty = penalty + abs(np.sum(schedule[worker, :])-21)*10
    return penalty*1

def check_workers_per_shift_amount(schedule):
    penalty = 0
    for day in range(0, days_in_interval*3):
        if np.sum(schedule[:,day])<2 or np.sum(schedule[:,day])>3:
            penalty = penalty+10
    return penalty*1

#This penalty is calculated by getting deviation of workers satisfaction
def check_satisfaction(schedule, preferences):
    
    satisfactions = np.zeros(np.shape(schedule)[0])
    for worker in range(0,len(workers[0])):
        satisfactions[worker]=sum(schedule[worker, :]*preferences[worker,:])
    deviation = np.std(satisfactions)
    return deviation*100

#This penalty is calculated by getting deviation of work frequency between everyone
def check_frequency(schedule):
    avgDays = []
    streakDays = []
    for worker in range(0,len(workers[0])):
        streak = 0
        for day in range(0, days_in_interval*3-2,3):
            if np.sum(schedule[worker,day:day+3])>1:
                streak = streak + 1
            elif (streak>0):
                streakDays.append(streak)
                streak = 0
            else:
                streak = 0
        avgDays.append(np.mean(streakDays))
    return np.std(avgDays)*100

def check_penalties(schedule, availability, preferences):
    return [check_gaps(schedule),check_gaps(schedule),check_max_hours(schedule),check_min_hours(schedule),check_workers_per_shift_amount(schedule),check_availability(schedule, availability),check_satisfaction(schedule, preferences), check_frequency(schedule)]

def print_penalties(schedule, availability, preferences):
    text=""
    penalties = check_penalties(schedule, availability, preferences)
    
    for i in range(len(estimators)):
        text = text + str(i) + "." + str(estimators[i]) + " - "+ str(penalties[i]) + "\n"
        
    text = text +('Shifts amount of every worker:')+"\n"
    for worker in range(0,len(workers[0])):
        text = text + str(sum(schedule[worker, :])) + "\n"
    
    return text 

def objective_func(schedule, availability,preferences):
    return sum(check_penalties(schedule,availability,preferences))

