def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it.
    '''
    global cur_temp # in degrees Celsius
    global cur_charge # in percentage points
    global cur_time # in minutes
    global health_count #counts the number of time goes over 90% 
    global good_battery_health #boolean for health battery 
    global time_1 #stores time 1 
    global time_2 #stores time 2 
    global time_3 #stores time 3 
    time_1 = 0 
    time_2 = 0 
    time_3 = 0 
    cur_time = 0
    health_count = 0
    good_battery_health = True
    cur_charge = 50
    cur_temp = 20

def simulate_activity(activity, duration):
    global cur_temp, cur_charge, cur_time, good_battery_health, health_count, time_1, time_2, time_3 
    fast_time = 0 
    slow_time = 0 
    dead_time = 0 
    idle_time = 0 
    slow_charge = False 
    dead = False
    bad = False 

    if activity == "charge": 
        time_cur_charge = 0 

        if cur_temp < 40 and cur_charge < 80 and good_battery_health == True: #check if can run fast charge 
            time_cur_temp = (40 - cur_temp) / 0.5 #max amt of time according to temp 
            time_cur_charge = (80 - cur_charge) / 3 #max amt of time according to charge 
            if time_cur_temp <= time_cur_charge: #take the smaller value 
                fast_time = time_cur_temp
            else:
                fast_time = time_cur_charge
            if fast_time >= duration: #take the smaller value 
                fast_time = duration
            else: 
                slow_time = duration - fast_time #figure out how long slow charge should be 
                slow_charge = True #have to undergo slow charge 
            cur_charge += fast_time * 3 
            cur_temp += fast_time * 0.5 
        else: 
            slow_time = duration #occur if fast charge cannot happen 
            slow_charge = True 

        
        if cur_charge + slow_time * 1 >= 90 and good_battery_health == True and slow_charge == True: 
            #run if battery health will be affected 
            
            time_90 = 90 - cur_charge #how long to 90% 

            if time_90 < 0: #ensure time_90 not below 0
                time_90 = 0

            health_count += 1 #charge beyond 90 

            time_1 = time_2 #move value to previous one 
            time_2 = time_3 
            time_3 = cur_time + fast_time + time_90 #take duration of new charge 

            if health_count >= 3 and (time_3 - time_1) < 360: #when battery health becomes bad 
                good_battery_health = False 
                bad = True 



        if slow_charge == True: #slow
            if good_battery_health == True: 
                time_cur_charge = (100 - cur_charge) / 1
            elif bad == True: 
                time_cur_charge = (90 - cur_charge) / 1
                if time_cur_charge < 0: 
                    time_cur_charge = 0
            else: 
                time_cur_charge = (80 - cur_charge) / 1
                if time_cur_charge < 0: 
                    time_cur_charge = 0
            if time_cur_charge >= slow_time:
                time_cur_charge = slow_time 
            cur_temp += 0.25 * time_cur_charge 
            cur_charge += 1 * time_cur_charge

            if time_cur_charge < slow_time:
                cur_temp += (slow_time - time_cur_charge) * 0.25



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
        if cur_charge > 0:
            time_cur_charge = cur_charge / 0.5

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
        return 


    if dead == True and cur_temp > 0: 
        time_cur_temp = cur_temp / 1 
        if dead_time >= time_cur_temp:
            dead_time = time_cur_temp
        cur_temp -= 1 * dead_time 

    dead = False 
    cur_time += duration 



def duration_fast_charge_possible():
    if cur_temp < 40 and cur_charge < 80 and good_battery_health:
        fast_time = (80 - cur_charge) / 3 
        temp_time = (40 - cur_temp) / 0.5 
        if fast_time > temp_time: 
            fast_time = temp_time  
        return fast_time
    else: 
        return None 
    
def get_cur_temp():
    return float(cur_temp)

def get_cur_charge():
    return float(cur_charge)

def get_cur_battery_health():
    return bool(good_battery_health)

def charge_time_needed(minutes):
    charge_needed = minutes * 2
    fast_charge = 0 

    if cur_charge >= charge_needed: #code after this will only run if cur_charge < charge_needed
        return 0
    if charge_needed > 100: 
        return None 

    if good_battery_health == False: 
        if charge_needed > 80: 
            return 
        elif charge_needed <= 80: 
            return (charge_needed - cur_charge) / 1

    elif good_battery_health == True: 
        fast_time_temp_limit = (40 - cur_temp) / 0.5 

        if fast_time_temp_limit < 0: 
            fast_time_temp_limit = 0 

        charge_temp_limit = cur_charge + fast_time_temp_limit * 3

        if charge_temp_limit >= charge_needed and charge_needed <= 80: 
            return (charge_needed - cur_charge) / 3 

        elif charge_needed <= 80: 
            slow_time = charge_needed - charge_temp_limit 
            return fast_time_temp_limit + slow_time 

        else: 
            fast_time = (80 - cur_charge) / 3 
            if fast_time_temp_limit < fast_time: 
                fast_time = fast_time_temp_limit 
            if fast_time < 0: 
                fast_time = 0 

            slow_time = charge_needed - (cur_charge + fast_time * 3)
            ###error for when it reaches 90 when bad battery health 

            if charge_needed > 90: 
                after_fast = 90 - cur_charge + fast_time * 3

                if after_fast < 0: 
                    after_fast = 0 

                if health_count >= 2 and cur_time + fast_time + after_fast - time_2 < 360: 
                    return None 

            return fast_time + slow_time 





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