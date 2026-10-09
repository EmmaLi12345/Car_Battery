def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it.
    '''
    global cur_temp # in degrees Celsius
    global cur_charge # in percentage points
    global cur_time # in minutes
    global good_battery_health
    cur_time = 0
    good_battery_health = True
    cur_charge = 50
    cur_temp = 20

def simulate_activity(activity, duration):
    global cur_temp, cur_charge, cur_time, good_battery_health
    fast_time = 0 
    slow_time = 0 
    dead_time = 0 
    idle_time = 0 
    slow_charge = False 
    dead = False
    if activity == "charge":
        if cur_temp < 40 and cur_charge < 80 and good_battery_health:
            time_cur_temp = (40 - cur_temp) / 0.5        #max amount of time we can charge until it reaches its limit
            time_cur_charge = (80 - cur_charge) / 3
            if time_cur_temp <= time_cur_charge:
                fast_time = time_cur_temp
            else:
                fast_time = time_cur_charge
            if fast_time >= duration: 
                fast_time = duration
            else: 
                slow_time = duration - fast_time
                slow_charge = True
            cur_charge += fast_time * 3 
            cur_temp += fast_time * 0.5
        else: 
            slow_time = duration 
            slow_charge = True 

        if slow_charge == True:
            time_cur_charge = (100 - cur_charge) / 1
            if time_cur_charge >= slow_time:
                time_cur_charge = slow_time 
            cur_temp += 0.25 * time_cur_charge 
            cur_charge += 1 * time_cur_charge

            if time_cur_charge < slow_time:
                cur_temp = (slow_time - time_cur_charge) * 0.25

    elif activity == "use":
        dead = False
        if cur_charge > 0:
            time_cur_charge = cur_charge / 2 
            if time_cur_charge >= duration: 
                time_cur_charge = duration 
            else: 
                dead_time = duration - time_cur_charge 
                dead = True

            cur_charge -= time_cur_charge * 2 
            cur_temp += time_cur_charge 

        else: 
            dead_time = duration
            dead = True

        if dead == True and cur_temp > 0: 
            time_cur_temp = cur_temp 
            if dead_time >= time_cur_temp:
                dead_time = time_cur_temp
            cur_temp -= 1 * dead_time 

        dead = False 
    elif activity == "idle":
        if cur_charge > 0 and cur_temp > 0:
            time_cur_charge = cur_charge / 0.5
            time_cur_temp = cur_temp / 1

            idle_time = time_cur_charge

        if idle_time >= duration: 
            idle_time = duration 
        else: 
            dead_time = duration - idle_time
            dead = True

        cur_charge -= idle_time * 0.5

        cur_temp -= idle_time  

        if cur_temp < 0: 
            cur_temp = 0

    else: 
        dead_time = duration
        dead = True

    if dead == True and cur_temp > 0: 
        time_cur_temp = cur_temp / 1 
        if dead_time >= time_cur_temp:
            dead_time = time_cur_temp
        cur_temp -= 1 * dead_time 

    dead = False 



def duration_fast_charge_possible():
    global cur_temp, cur_charge, cur_time, good_battery_health #do we need global? 
    if cur_temp < 40 and cur_charge < 80 and good_battery_health:
        time = (80 - cur_charge) / 3  
        return time
    
def get_cur_temp():
    return float(cur_temp)

def get_cur_charge():
    return float(cur_charge)

def get_cur_battery_health():
    return bool(good_battery_health)

def charge_time_needed(minutes):
    pass
if __name__ == '__main__':
    initialize()
    print(duration_fast_charge_possible()) # 10
    print(charge_time_needed(50)) # 30
    simulate_activity("charge",30)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 30
    simulate_activity("use",50)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 80
    simulate_activity("use",10)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 70
    simulate_activity("charge",100)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 95
    simulate_activity("idle",100)
    print(get_cur_charge()) # 50
    print(get_cur_temp()) # 0
    print(get_cur_battery_health()) # True
    print(duration_fast_charge_possible()) # 10
    simulate_activity("charge",80)
    print(get_cur_charge()) # 90
    print(get_cur_temp()) # 22.5
    print(get_cur_battery_health()) # False
    simulate_activity("use",40)
    print(get_cur_charge()) # 10
    print(get_cur_temp()) # 62.5
    simulate_activity("charge",80)
    print(get_cur_charge()) # 80
    print(get_cur_temp()) # 82.5
    initialize()
    # add your tests here