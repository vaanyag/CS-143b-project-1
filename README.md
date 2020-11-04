# PROJECT 1 : PROCESS AND RESOURCE MANAGER

### **<ins>ABOUT</ins>**
A process and resource manager program written in python language. It is a basic manager with extended functionalities which includes process with different priorities, scheduling according to the priority and resources having multiple identical units. It has 6 main operations - create, destory, request, release, timeout and scheduler; and some helper functions to make the code readable and presentable. 

### **<ins>HOW TO RUN THE PROGRAM</ins>**
There is a input.txt file from where the program reads the commands line by line and prints the output to output.txt file. 
- The input.txt, project1.py should be in the same directory. 
- To run the program: 
    - Make sure that the current directory is the same as the directory of input.txt and project1.py
    - Enter the command python project1.py in the terminal [if the current python version is set to 3] otherwise use python3 project1.py
    - After the command is entered, output.txt file is generated automatically and saved in the same directory as input.txt and project1.py
- The output.txt file contains the output of the program

### **<ins>FUNCTIONS</ins>**
**<ins>CREATE</ins>**
- **create_init()** : Initializes: PCB[16], RCB[4] and Ready List RL with priority levels. It also creates PCB[0] (with priority = 0) 
- **create(p)** : Creates a new process with priority 'p' 

**<ins>DESTROY</ins>**
- **destroy(j)** : Destroys the process j if it exists along with its children and grandchildren (if any) 
- **check_destroy(j)**[<ins>Helper function of destroy()</ins>] : It checks if j is current running process or is one of the decendents of current running process and then calls the destroy function 
- **print_destroy_count()**[<ins>Helper function of destroy()</ins>] : Outputs the total number of processes destroyed 
- **remove_parent()**[<ins>Helper function of destroy()</ins>] : Remove j from the children list of its parent process when destroy is called 
    
**<ins>REQUEST</ins>**
- **request(r,k)** : Request k units of r resource 

**<ins>RELEASE</ins>**
- **release(r,k)** : Releases k units of resource r 

**<ins>TIMEOUT</ins>**
- **timeout()** : Moves the current process to the end of the reading list and call the scheduler  

**<ins>SCHEDULER</ins>**
- **scheduler()** : To perform context switch and schedule according to the priority 

**<ins>MANAGE INPUT AND OUTPUT</ins>**
- **write_in_file()** : Writes the output in the output file 
- **menu()** : Calls the appropriate function according to the command in the input file  

### **<ins>AUTHOR</ins>**
VAANYA GUPTA
