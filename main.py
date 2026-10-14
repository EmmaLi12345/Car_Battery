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
    bad = False #used to determine if a battery JUST turned bad 

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
            time_3 = cur_time + fast_time + time_90 #take timestamp of most recent time of hitting 90

            if health_count >= 3 and (time_3 - time_1) < 360: #when battery health becomes bad 
                good_battery_health = False 
                bad = True 



        if slow_charge == True: #slow charge 
            if good_battery_health == True: #can charge to full 
                time_cur_charge = (100 - cur_charge) / 1
            elif bad == True: #just turned bad -> it can still charge up to 90 but no more
                time_cur_charge = (90 - cur_charge) / 1
                if time_cur_charge < 0: 
                    time_cur_charge = 0
            else: #had bad battery health from before, so capped at 80 
                time_cur_charge = (80 - cur_charge) / 1
                if time_cur_charge < 0: #ensure time_cur_charge does not fall below 0 
                    time_cur_charge = 0
            if time_cur_charge >= slow_time: #take the smaller value 
                time_cur_charge = slow_time 
            cur_temp += 0.25 * time_cur_charge 
            cur_charge += 1 * time_cur_charge

            if time_cur_charge < slow_time: #temp can continue increasing even when charge is capped 
                cur_temp += (slow_time - time_cur_charge) * 0.25



    elif activity == "use":
        dead = False #check if there is charge 
        if cur_charge > 0: #there is charge 
            time_cur_charge = cur_charge / 2 
            if time_cur_charge >= duration: #takes the smaller value 
                time_cur_charge = duration 
            else: #battery still runs for a while even after it is dead 
                dead_time = duration - time_cur_charge  
                dead = True

            cur_charge -= time_cur_charge * 2 
            cur_temp += time_cur_charge 

        else: #battery starts dead 
            dead_time = duration
            dead = True

        if dead == True and cur_temp > 0: #calculates temperature decrease (battery is dead)
            time_cur_temp = cur_temp 
            if dead_time >= time_cur_temp: #takes the smaller value 
                dead_time = time_cur_temp
            cur_temp -= 1 * dead_time 

        dead = False 

    elif activity == "idle":
        if cur_charge > 0: 
            time_cur_charge = cur_charge / 0.5 #longest it can stay idle 

            idle_time = time_cur_charge

        if idle_time >= duration: #takes the smaller value 
            idle_time = duration 
        else: #battery will continue running even when it is dead 
            dead_time = duration - idle_time 
            dead = True

        cur_charge -= idle_time * 0.5 

        cur_temp -= idle_time  

        if cur_temp < 0: #ensure temp is always above or equal to 0 
            cur_temp = 0

        if dead == True and cur_temp > 0: #calculates temperature decrease (battery is dead)
            time_cur_temp = cur_temp / 1 
            if dead_time >= time_cur_temp: #takes the smaller value 
                dead_time = time_cur_temp
            cur_temp -= 1 * dead_time

    else: #command not charge, use, or idle 
        return 

    cur_time += duration #timestamp 



def duration_fast_charge_possible(): 
    if cur_temp < 40 and cur_charge < 80 and good_battery_health: #ensure conditions for fast charge are met 
        fast_time = (80 - cur_charge) / 3 
        temp_time = (40 - cur_temp) / 0.5 
        if fast_time > temp_time: #take the smaller value 
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
    charge_needed = minutes * 2 #how much charge needed to run for minutes 

    if cur_charge >= charge_needed: #code after this will only run if cur_charge < charge_needed
        return 0
    if charge_needed > 100: #not possible 
        return None 

    if good_battery_health == False: #cannot fast charge or go beyond 80 
        if charge_needed > 80: 
            return 
        elif charge_needed <= 80: 
            return (charge_needed - cur_charge) / 1 

    elif good_battery_health == True: #can go through fast charge 
        fast_time_temp_limit = (40 - cur_temp) / 0.5 #time allowed for fast charge based on temp 

        if fast_time_temp_limit < 0: #ensure it does not fall below 0 
            fast_time_temp_limit = 0 

        charge_temp_limit = cur_charge + fast_time_temp_limit * 3 #charge reached if charged until temp = 40 

        if charge_temp_limit >= charge_needed and charge_needed <= 80: #just needs fast charge 
            return (charge_needed - cur_charge) / 3 

        elif charge_needed <= 80: #temp stops it from fast charging 
            slow_time = charge_needed - charge_temp_limit #time it would take to slow charge to the required percentage 
            return fast_time_temp_limit + slow_time 

        else: 
            fast_time = (80 - cur_charge) / 3 #time it would take to fast charge based on charge 
            if fast_time_temp_limit < fast_time: #take smaller value 
                fast_time = fast_time_temp_limit 
            if fast_time < 0: #ensure does not fall below 0 
                fast_time = 0 

            slow_time = charge_needed - (cur_charge + fast_time * 3) #how long does it need to slow charge 

            if charge_needed > 90: 
                after_fast = 90 - cur_charge - fast_time * 3 #how long it takes to reach 90 

                if after_fast < 0: 
                    after_fast = 0 

                if health_count >= 2 and cur_time + fast_time + after_fast - time_2 < 360: #if battery health goes bad 
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