# -------------
# CS 143B - FALL 2020 - UNIVERSITY OF CALIFORNIA, IRVINE
# NAME : VAANYA GUPTA
# STUDENT_ID : 92052177
# NET_ID : vaanyag
# -------------

def create_init():
    # -------------
    # Initializes:
    # PCB[16], RCB[4] and Ready List RL with priority levels
    # It also creates PCB[0] (with priority = 0)
    # -------------
    global RL, PCB, RCB, destroy_count, current_running, error, in_count
    PCB = []
    for i in range(16):
        PCB.append(None)
    RCB = [{'state' : 1, 'waitlist' : [], 'inventory' : 1},{'state' : 1, 'waitlist' : [], 'inventory' : 1},
    {'state' : 2, 'waitlist' : [], 'inventory' : 2},{'state' : 3, 'waitlist' : [], 'inventory' : 3}]
    PCB_str = {}  #{'state' = -1, 'parent' = -1, 'children' = [], 'resources' = {} }
    RL = []
    destroy_count = 0
    current_running = 0
    PCB[0] = {'state' : 1, 'parent' : -1, 'children' : [], 'resources' : {}, 'p': 0 }
    RL.append(0)
    in_count += 1
    print ('PCB[0] initialized')

def create(p):
    # -------------
    # Creates a new process with priority 'p' 
    # -------------
    global current_running, RL, PCB, RCB, error
    found = False
    for i in range (len(PCB)):
        # p = "priority"
        if PCB[i]==None and p in ['1','2']:
            p = int(p)
            found = True
            allocation = {'state' : 1, 'parent' : current_running, 'children': [], 'resources': {},'p':p}
            PCB[current_running]['children'].append(i)
            RL.append(i)
            PCB[i] = allocation
            print ("Process ",i," created")
            scheduler()
            break
    if not found:
        error = 1
        print ("*error* - max processes reached")

def check_destroy(j):
    # -------------
    # It checks if j is current running process
    # or is one of the decendents of current running process
    # and then calls the destroy function
    # -------------
    global error
    check_j = True
    list_j = []
    list_j = list(PCB[current_running]['children'])
    list_j.append(current_running)
    if j not in list_j:
        check_j = False
    if j == 0:
        check_j = False
    if check_j:
        destroy(j)
    else:
        error = 1
        print ("*error* - j not the current running or its decendents")

def destroy(j):
    # -------------
    # Destroys the process j if it exists along 
    # with its children and grandchildren (if any)
    # -------------
    global current_running, RL, PCB, RCB, destroy_count, parent_list, error
    
    parent_list.append(j)
    if PCB[j]!=None:
        children = PCB[j]['children']
        # Destroy all children of j
        for k in children:
            destroy(k)
        # Remove j from waitlist
        resources = PCB[j]['resources'].copy()
        for i in range (len(RCB)):
            wait = RCB[i]['waitlist']
            for k in range(len(wait)):
                for l,m in wait[k].items():
                    if l == j:
                        RCB[i]['waitlist'].pop(k)
        # Remove j from reading list 
        if j in RL:
            RL.remove(j)
        # Release all the resources of j
        for r,k in resources.items():
            current_running = j
            release(r,k)
        PCB[j] = None
        destroy_count+=1
   
    else:
        error = 1
        print ("*error* - j doesn't exist")

def print_destroy_count():
    # -------------
    # Outputs the total number of processes destroyed 
    # -------------
    global destroy_count, parent_list
    print (destroy_count, 'processes destroyed: ',parent_list)
    # Remove j from the children list of its parent process
    remove_parent()
    scheduler()

def remove_parent():
    # -------------
    # Remove j from the children list of its parent process when destroy is called 
    # -------------
    global parent_list, PCB
    for i in parent_list:
        for j in range(len(PCB)):
            if PCB[j]!=None and i in PCB[j]['children']:
                PCB[j]['children'].remove(i)
    parent_list = []

def request(r,k):
    # -------------
    # Request k units of r resource
    # -------------
    global current_running, RL, PCB, RCB, error
    # Checks the capacity of r and k; and if current process != 0 to prevent deadlock
    check = False 
    if k in [1,2,3] or k in ['1','2','3']:
        k = int(k)            
        check = True
    if r in ['0','1','2','3'] and current_running!=0 and check: 
        r = int(r)
        k = int(k)
        # If resource is available then allocate the resource to the process
        if RCB[r]['state'] !=0 and RCB[r]['state'] >= k:
            RCB[r]['state'] -= k
            PCB[current_running]['resources'][r] = k
            print ('resource ',r," allocated")
            print ("process ", current_running, "running")
        else:
            # if requested > inventory - *error*
            if k <= RCB[r]['inventory']:
                PCB[current_running]['state'] = 0
                RL.remove(current_running)
                RCB[r]['waitlist'].append({current_running: k})
                print ("process ", current_running, "blocked")
                scheduler()
            # else add process to the waitlist 
            else:
                print ('*error* - requested more units than inventory')
                error = 1
    else:
        print ('*error* - r entered is wrong or current is 0')
        error = 1

def release(r,k):
    # -------------
    # releases k units of resource r
    # -------------
    global current_running, RL, PCB, RCB, error
    # checks k and r
    check = True
    if r not in [0,1,2,3] :
        check = False
    if k not in [0,1,2,3]:
        check = False
    # checks if the current process had resource r allocated 
    if check and (r in PCB[current_running]['resources'].keys()):
        # checks if the units released is less or equal to allocated 
        if k<=PCB[current_running]['resources'][r]:
            RCB[r]['state'] += k
            count = 0 
            # once released, checks the waitlist of r and unblocks the process if the units are sufficient
            # no partial allocation
            while (RCB[r]['waitlist']!=[]) and RCB[r]['state']>0:
                for j,k in RCB[r]['waitlist'][0].items():
                    if RCB[r]['state'] >= k:
                        RCB[r]['state'] -= k
                        if PCB[j]['resources']!={} and r in PCB[j]['resources'].keys():
                            PCB[j]['resources'][r] += k
                        else:
                            PCB[j]['resources'][r] = k
                        PCB[j]['state'] = 1
                        RCB[r]['waitlist'].pop(0)
                        RL.append(j)
                        count+=1
                    else:
                        break
            scheduler()
           
        else:
            print ('*error* - r big')
            error = 1 
    else:
        print ('*error* - r not in resource list')
        error = 1

def timeout():
    # -------------
    # Moves the current process to the end of the reading list and call the scheduler 
    # -------------
    global current_running, RL, PCB, RCB
    RL.pop(0)
    RL.append(current_running)
    scheduler()

def scheduler():
    # -------------
    # To perform context switch 
    # -------------
    global current_running, RL, PCB, RCB 
    found = False
    index = -1
    for i in range(2,-1,-1):
        for j in range (len(PCB)):
            if PCB[j]!=None and j<len(RL):
                if PCB[RL[j]]['p'] == i :
                    current_running = RL[j]
                    found = True 
                    break
        if found:
            break
    for i in range(len(RL)):
        if RL[i]==current_running:
            index = i
    for i in range(index):
        remove_ = RL[0]
        RL.pop(0)
        RL.append(remove_)
    print ('Process ',current_running,' running')

def write_in_file():
    # -------------
    # Writes the output in the output file
    # -------------
    global error, current_running, in_count
    if error == 0:
        if in_count>0:
            f_o.write('\n'+str(current_running)+' ')
            in_count = 0
        else:
            f_o.write(str(current_running)+' ')
    else:
        f_o.write('-1')
            
    error = 0

def menu():
    # -------------
    # calls the appropriate function according to the command in the input file 
    # -------------
    global error
    if user_input[0:2] == 'cr':
        p = user_input[2::].strip()
        create(p)
        write_in_file()
        
    elif user_input[0:2] == 'de':
        
        j = user_input[2::].strip()
        if j.isdigit():
            j=int(j)
            if j>=0 and j<16:
                check_destroy(j)
                print_destroy_count()
            else:
                error = 1
                print ('*error* - j value wrong')
        else:
            error = 1
            print ('*error* - j is not an correct index')
        
        write_in_file()

    elif user_input[0:2] == 'rq':
        
        r = user_input[2::].strip()
        r = r.split(' ')
        if len(r) == 2:
            if r[1].isdigit():
                r[1] = int(r[1])
            request(r[0],r[1])
           
        else:
            error = 1
            print ("error - rq _ _ entered wrong value")
        
        write_in_file()

    elif user_input[0:2] == 'rl':
        
        r = user_input[2::].strip()
        r = r.split(' ')
        if len(r) == 2:
            if r[1].isdigit() and r[0].isdigit():
                r[1] = int(r[1])
                r[0] = int(r[0])
            release(r[0],r[1])
            
        else:
            print ("error - rl _ _ entered wrong value")
            error = 1
        write_in_file()

    elif user_input == 'to':
        timeout()
        write_in_file()

    elif user_input == 'in':
        create_init()
        write_in_file()

    elif user_input =='q':
        pass
    
    else:
        error = 1
        print ("*error* - incorrect input")
        write_in_file()

if __name__ == '__main__':
        
    error, PCB, RCB, PCB_str, RL, in_count, commands = 0, [], [], {}, [], -1, []
    destroy_count, current_running, parent_list = 0, 0, []
    f_i = open("input.txt","r")
    f_o = open("output.txt","w") 
    for command in f_i.readlines():
        if command !='\n':
            commands.append(command.strip())

    user_input = ''
    for i in commands:
        user_input = i
        menu()
    
    f_i.close()
    f_o.close()