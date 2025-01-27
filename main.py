import json
import sys



def runSimulation(time,circuits,demands, switchesDictionary):

    # list of active 
    active_roads = [] 
    steps = 1
    for i in range(1, int(time) + 1):
        for demand in demands:
           if int(demand['end-time']) == i:
               getSwitches(circuits,demand,switchesDictionary, False, i, steps, active_roads)
               steps += 1

           if int(demand['start-time']) == i:
               getSwitches(circuits,demand,switchesDictionary, True, i, steps, active_roads)
               steps += 1
         
         

def setUpSwitch(switches, switchesDIC):
    for switch in switches:
        switchesDIC.update({switch : True})


    
def getSwitches(posible_circuits, demand, switchesDictionary, status, time, steps,active_roads):

    start_point = demand['end-points'][0]
    end_point = demand['end-points'][1]

    for circuits in posible_circuits:
        if circuits[0] == start_point and circuits[len(circuits) - 1] == end_point:
           switch = circuits[:]
           switch.remove(start_point)
           switch.remove(end_point)
           if  setSwitch(switch, status, switchesDictionary, start_point, end_point, time, steps,active_roads):
               break

def setSwitch(swiches, status, switchesDictionary, start_point, end_point,time, steps, active_roads):
    succes = False
    reserved = False
    already_free = False
    if status:
        for switch in swiches:
          
          if switchesDictionary[switch]:
              switchesDictionary[switch] = False
          else:
              reserved = True
              break
        if reserved:
            print(f'{steps}. igény foglalás: {start_point}<->{end_point} st:{time} - sikertelen')
        else:
            print(f'{steps}. igény foglalás: {start_point}<->{end_point} st:{time} - sikeres')
            road = [start_point,end_point]
            active_roads.append(road)

        succes = True
    else:
        for switch in swiches:
            if switchesDictionary[switch]:
                already_free = True
            switchesDictionary[switch] = True
        
        for i in active_roads:
            if i == [start_point,end_point]:
                print(f'{steps}. igény felszabadítás: {start_point}<->{end_point} st:{time}')
                active_roads.remove(i)
        succes = True
    return succes
    
   



def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f: # load file
            file = json.load(f)

            #load important datas
            time = int(file['simulation']['duration'])
            posible_circuits = file['possible-circuits']
            demands = file['simulation']['demands']
            switches = file['switches']


            #initialize and setup dictionary 
            switchesDictionary = {}
            setUpSwitch(switches, switchesDictionary)


            runSimulation(time,posible_circuits,demands, switchesDictionary)
  
    else:
        print("Nem megfelelő a parancssori argumentumok száma")

try:
    main()
except:
    print("Hiba történt a program futása során")

#<esemény sorszám>. <esemény név>: <node1><-><node2> st:<szimuálciós id > [- (sikeres|sikertelen)]