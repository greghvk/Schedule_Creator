from schedule_penalty_calculators import *

def shift_lines(schedule):
    new_schedule = schedule.copy()
    numbers = np.random.randint(0,len(workers[0]),2)
    temp = new_schedule[numbers[0],:].copy()
    new_schedule[numbers[0],:]=new_schedule[numbers[1],:]
    new_schedule[numbers[1],:]=temp
    return new_schedule
    
def shift_columns(schedule):
    new_schedule = schedule.copy()
    numbers = np.random.randint(0, days_in_interval*3,2)
    temp = schedule[:,numbers[0]].copy()
    new_schedule[:,numbers[0]]=new_schedule[:,numbers[1]]
    new_schedule[:,numbers[1]]=temp
    return new_schedule
    
def cut_shift(schedule):
    working_days = np.argwhere(schedule)
    new_schedule = schedule.copy()
    if len(working_days)>0:
        d=np.random.randint(0,len(working_days))
        x = working_days[d]
        x1 = x[0]
        x2 = x[1]
        new_schedule[x1, x2]=0
    return new_schedule
    
def add_shift(schedule):
    working_days = np.argwhere(abs(1-schedule))
    new_schedule=schedule.copy()
    if len(working_days)>0:
        d=np.random.randint(0,len(working_days))
        x = working_days[d]
        x1 = x[0]
        x2 = x[1]
        new_schedule[x1,x2]=1
    return new_schedule

def move_shift(schedule):
    new_schedule = schedule.copy()    
    chosen_worker = np.random.randint(0,len(workers[0]))
    
    temp1 = schedule[chosen_worker, 0]
    new_schedule[int(chosen_worker),1:] = new_schedule[int(chosen_worker),:-1]
    new_schedule[int(chosen_worker),-1] = temp1
    
    return new_schedule

def shift_shifts(schedule):
    new_schedule = schedule.copy()
    try:
        off_days = np.argwhere(abs(1-schedule))
        working_days = np.argwhere(schedule)

        dp=np.random.randint(0,len(working_days))
        dw=np.random.randint(0,len(off_days))

        xp = working_days[dp]
        xp1 = xp[0]
        xp2 = xp[1]
        new_schedule[xp1, xp2] = 0

        xw = off_days[dw]
        xw1 = xw[0]
        xw2 = xw[1]
        new_schedule[xw1, xw2] = 1
    except: 
        return schedule
    return new_schedule

def optimize_schedule(schedule):
    temporary = schedule.copy()
    penalties = check_penalties(schedule,workers_availability,workers_preferences)
    biggest_penalty = penalties.index(max(penalties))
    
    #Depending on type of biggest penalty, how new schedule is made will be chosen
    solution_change_type = {0:[3],#Gap between shifts
              1:[0,1,4], #Required experience per shift
              2:[3,5], #Too much shifts per interval per worker
              3:[1,2,5], #Not enough shifts per interval per worker
              4:[2,4,5], #Workers amount per shift
              5: [0,1,3,4,5], #Workers availability
              6: [0,1,2,3], #Workers satisfaction
              7: [0,2,3,4,5]# Work frequency
                  }[biggest_penalty]

    x = np.random.choice(solution_change_type)
    
    if x==0 or x==1:
        temporary = shift_columns(temporary)
    if x==1:
        temporary = shift_lines(temporary)
    if x==2:
        temporary = add_shift(temporary)
    if x==3:
        temporary = cut_shift(temporary)
    if x==4:
        temporary = move_shift(temporary)
    if x==5:
        temporary = shift_shifts(temporary)
 
    return temporary