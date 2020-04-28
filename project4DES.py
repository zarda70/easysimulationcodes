import ciw
import math
import random


arrival_rate = input("Enter the arrival rate: ")                                        # inputs
service_rate = input("Enter the service rate: ")
capacity = input("Enter the queue capacity (00 for infinity): ")
while str.isdigit(capacity) == False:                                                   # check for non integer values
    print("What kind of input is this??? INTEGER ONLY (/¯◡ ‿ ◡)/¯ ~ ┻━┻")
    capacity = input("Enter the queue capacity (00 for infinity): ")
outputs = input("how many customers data will be printed?: ")
simulation_run_time = input("Enter the run time of the simulation (minutes): ")


if capacity == "00":                                                                    # infinite queue capacity
    capacity = math.inf

else:
    capacity = int(capacity)


N = ciw.create_network(                                                                 # creating the environment
    arrival_distributions=[ciw.dists.Exponential(int(arrival_rate))],                   # arrival rate (Lambda)
    service_distributions=[ciw.dists.Exponential(int(service_rate))],                   # service rate (Mü)
    number_of_servers=[1],                                                              # how many servers will be
    queue_capacities=[capacity]                                                         # queue capacity

)


ciw.seed(random.seed)                                                                   # setting a random seed for random simulation results
Q = ciw.Simulation(N)                                                                   # Simulating the created environment

Q.simulate_until_max_time(int(simulation_run_time), progress_bar=True)                  # Q.simulate_until_max_Customers can be used instead of time limitation

recs = Q.get_all_records()                                                              # holding the values

waits = [r.waiting_time for r in recs]                                                  # creating arrays for the data
arrival_date = [r.arrival_date for r in recs]
serv_start = [r.service_start_date for r in recs]
serv_end = [r.service_end_date for r in recs]
serviceTimes = [r.service_time for r in recs]
queueSize = [r.queue_size_at_arrival for r in recs]
node = [r.destination for r in recs]

meanTimeOnSystem = (sum(waits) / len(waits) + (sum(serviceTimes) / len(serviceTimes)))  # calculating the average values which will be printed
mean_wait = sum(waits)/len(waits)
mean_queue_size = sum(queueSize) / len(queueSize)
meanCustomerOnSystem = (sum(waits) + len(waits)) / len(waits)

cantEnter = len(Q.rejection_dict[1][0])                                                 # Customers who can't enter the system because of queue capacity (if the capacity is not infinite)
totalCustomer = len(arrival_date)                                                       # Total customer on the system

print("Total number of customers: ", len(arrival_date))
print("Number of customers who cannot enter system: ", cantEnter, "===> ", "%",(100*cantEnter) / totalCustomer)
print("Average waiting at queue: ", mean_wait," minutes =====> ", mean_wait*60, " seconds")
print("Average time in system: ", meanTimeOnSystem, "minutes =====> ", meanTimeOnSystem*60, " seconds")
print("Average queue size: ", mean_queue_size)
print("Average customer on system:", meanCustomerOnSystem)

if int(outputs) > 0:                                                                    # Printing the outputs
    print("  arrival date           service start          service time           waiting           service end           queue size at arrival")

    for i in range(int(outputs)):
        print(i, round(arrival_date[i], 5),"              ", round(serv_start[i], 5),"              ", round(serviceTimes[i], 5), "              ", round(waits[i], 5), "              ", round(serv_end[i], 5), "              ", queueSize[i] )
