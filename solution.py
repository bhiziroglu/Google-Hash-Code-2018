import copy

def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)


firstline=0

R=0 #Number of rows
C=0 #Number of cols
F=0 #Number of vehicles
N=0 #Number of rides
B=0 #Bonus for starting on time
T=0 #Number of steps

real_rides = []

t1 = 'a_example.in'
t2 = 'b_should_be_easy.in'
t3 = 'c_no_hurry.in'
t4 = 'd_metropolis.in'
t5 = 'e_high_bonus.in'

with open(t5, 'rU') as f:
    for line in f:
        if firstline==0:
            tmp = line.split(' ')
            R=int(tmp[0])
            C=int(tmp[1])
            F=int(tmp[2])
            N=int(tmp[3])
            B=int(tmp[4])
            T=int(tmp[5])
            firstline=1
        else:
            tmp = line.split(' ')
            real_rides.append((int(tmp[4]),int(tmp[5].strip()),(int(tmp[0]),int(tmp[1])),(int(tmp[2]),int(tmp[3]))))

#('2', '9', ('0', '0'), ('1', '3'))

rides = copy.deepcopy(real_rides) # Deep copy is used to preserve the original indices of the rides
                                  # This is required for the creation of the output file
rides = sorted(rides, key = lambda x: int(x[0])) #Sort the rides according to their earliest start time

assigned_rides = {} #Assigned rides for F vehicles


fleet = [0]*F #number of free vehicles
next_free = [0]*F #Next free time for every vehicle
current_loc = [(0,0)]*F #Locations of the vehicles

for timestep in range(T):

    number_of_rides_possible = len(rides)

    if number_of_rides_possible==0:
        break

    for vehicle in range(F):
        if(fleet[vehicle]==0): #If vehicle is free
            next_ride = rides[0] #Next earliest ride
            distance_to_caller = manhattan_distance(current_loc[vehicle],next_ride[2])
            distance_of_trip = manhattan_distance(next_ride[2],next_ride[3])

            if(next_ride[1]-timestep>=distance_to_caller+distance_of_trip): # Can the vehicle make it?

                if(next_ride[0]-timestep-distance_to_caller <= distance_to_caller):
                    
                    fleet[vehicle]=1 #Vehicle is busy now

                    if vehicle in assigned_rides:
                        assigned_rides[vehicle].append(real_rides.index(next_ride))
                    else:
                        assigned_rides[vehicle] = [real_rides.index(next_ride)]

                    rides.pop(0) #Pop this ride so the others cant take it
                    current_loc[vehicle] = next_ride[3] #Vehicle's new location is the desination point
            
                    if(timestep+distance_to_caller<=next_ride[0]): #CASE 1 for wait time
                        next_free[vehicle] = next_ride[0] + distance_of_trip
                    else: #CASE 2 for wait time
                        next_free[vehicle] = timestep + distance_to_caller + distance_of_trip

    
    if(number_of_rides_possible==len(rides)): #If no vehicle took this ride, postpone it
        troll_ride = rides.pop(0)
        rides.insert(F,troll_ride) #F can be any number

    for vehicle in range(F):
        if(timestep>=next_free[vehicle]):
            fleet[vehicle]=0


#Save the result to the output file
with open('output', 'w') as f:
    for key in assigned_rides.keys():
        tmp = assigned_rides[key]
        tmp2 = ''+ str(len(tmp))
        for item in tmp:
            tmp2 = tmp2 + ' ' + str(item)
        tmp2+='\n'
        f.write(tmp2)
    f.close()
