#module to copy the customer list.
import copy

#attribute getter for sorting the customer list according to the id.
from operator import attrgetter

# dictionary to track that a particular email have occured or not.
dict_email={}

# dictionary to track that a particular mobile have occured or not.
dict_mobile={}

# dictionary to save and retieve the immidiate parent index of emails in 
# customer list/may not be the actual parent/.
dict_email_parent={}

# dictionary to save and retieve the immidiate parent index of mobiles in 
# customer list/may not be the actual parent/.
dict_mobile_parent={}

# dictionary to track that a particular email and mobile combination has 
# occured or not.
dict_email_mobile={}

# list of customer objects
cust_list=list()

# dictionary to store which ids are needed to be merged in some other id
dict_id_merged={}

# variable to be assigned as ids to the emails and mobiles
global id
id=0

# variable to keep track of the index of customer object list
index=-1

inp=raw_input("Enter datafile:")
input_file=str(inp)
inp=raw_input("Enter outputfile:")
out_file=str(inp)

# customer class containing various attributes.
class customer:
    def __init__(self,sz,p_index,id,email,mobile_no):
        self.sz=sz
        self.p_index=p_index
        self.id=id
        self.email=email
        self.mobile_no=mobile_no
 
# function to do the union of two different id sets based on the size of both the sets
# if some element is found common in the two sets
def weighted_quick_union(parent_index1,parent_index2):
    while (parent_index1!=cust_list[parent_index1].p_index):
        parent_index1=cust_list[parent_index1].p_index
    while (parent_index2!=cust_list[parent_index2].p_index):
        parent_index2=cust_list[parent_index2].p_index
    if(parent_index1!=parent_index2):
        if(cust_list[parent_index1].sz < cust_list[parent_index2].sz):
            cust_list[parent_index1].p_index=cust_list[parent_index2].p_index
            cust_list[parent_index2].sz+=cust_list[parent_index1].sz
            return parent_index2,cust_list[parent_index1].id
        else:
            cust_list[parent_index2].p_index=cust_list[parent_index1].p_index
            cust_list[parent_index1].sz+=cust_list[parent_index2].sz
            return parent_index1,cust_list[parent_index2].id
    return parent_index1,cust_list[parent_index1].id
 
#function to implement the path compression to make every object point to its actual parent. 
def path_compression(flag,id_merged):
    if flag=='a':
        for i in range(len(cust_list)):
            j=i
            if(cust_list[i].id==id_merged):
                while(j!=cust_list[j].p_index):
                    j=cust_list[j].p_index
                cust_list[i].p_index=cust_list[j].p_index
                cust_list[i].id=cust_list[j].id
                
    if flag=='m':
        for i in range(len(cust_list)):
            j=i
            if(cust_list[i].id in dict_id_merged):
                while(j!=cust_list[j].p_index):
                    j=cust_list[j].p_index
                    cust_list[j].p_index
                cust_list[i].p_index=cust_list[j].p_index
                cust_list[i].id=cust_list[j].id

# function to write the output data to the output file.          
def write():
    cust_list_dup = copy.copy(cust_list)
    cust_list_dup.sort(key = attrgetter('id'))
    fh=open(out_file,'w+')
    fh.write("%-10s    %-30s                         %s\n"%("cust_id","email_id","mobile_no"))
    count=0
    for i in range(len(cust_list)):
        if i == 0 or cust_list_dup[i].id != cust_list_dup[i-1].id:
            count +=1
        fh.write("%-10s       %-40s     %s\n"%(str(cust_list_dup[i].id),cust_list_dup[i].email,cust_list_dup[i].mobile_no))
    fh.close()
    print ("Unique users:",count)

# function to make customer objects,add them to customer list and update the dictionaries 
# various condtions are present to verify the prexistance of email and mobile combinations.
def update(flag,user):
    global id
    global index
    global input_file
    global out_file
    u=user.split()
    u_id=0
    if (u[0] not in dict_email and u[1] not in dict_mobile):
            id=id+1
            index+=1
            if u[0]!='\\Z':
                dict_email[u[0]]=id
                dict_email_parent[u[0]]=index
            if u[1]!='\\Z':
                dict_mobile[u[1]]=id
                dict_mobile_parent[u[1]]=index
            if u[0]!='\\Z' or u[1]!='\\Z':
                s=u[0]+u[1]
                dict_email_mobile[s]=1
            cust_object=customer(1,index,id,u[0],u[1])
            cust_list.append(cust_object)
            u_id=id
           
    elif (u[0] in dict_email and u[1] not in dict_mobile):
            index+=1
            if u[1]!='\\Z':
                dict_mobile[u[1]]=dict_email[u[0]]
                dict_mobile_parent[u[1]]=dict_email_parent[u[0]]
            if u[0]!='\\Z' or u[1]!='\\Z':
                s=u[0]+u[1]
                dict_email_mobile[s]=1
            cust_list[dict_email_parent[u[0]]].sz+=1
            cust_object=customer(1,dict_email_parent[u[0]],dict_email[u[0]],u[0],u[1])
            cust_list.append(cust_object)
            u_id=cust_list[dict_email_parent[u[0]]].id
         
    elif (u[0] not in dict_email and u[1] in dict_mobile):
            index+=1
            if u[0]!='\\Z':
                dict_email[u[0]]=dict_mobile[u[1]]
                dict_email_parent[u[0]]=dict_mobile_parent[u[1]]
            if u[0]!='\\Z' or u[1]!='\\Z':
                s=u[0]+u[1]
                dict_email_mobile[s]=1
            cust_list[dict_mobile_parent[u[1]]].sz+=1
            cust_object=customer(1,dict_mobile_parent[u[1]],dict_mobile[u[1]],u[0],u[1])
            cust_list.append(cust_object)
            u_id=cust_list[dict_mobile_parent[u[1]]].id
          
    elif (u[0] in dict_email and u[1] in dict_mobile):
            if(dict_email[u[0]]!=dict_mobile[u[1]]):
                index+=1
                if u[0]!='\\Z' or u[1]!='\\Z':
                    s=u[0]+u[1]
                    dict_email_mobile[s]=1
                parent_index1=dict_email_parent[u[0]]
                parent_index2=dict_mobile_parent[u[1]]
                parent_index3,id_merged=weighted_quick_union(parent_index1,parent_index2)
                dict_id_merged[id_merged]=1
                cust_list[parent_index3].sz+=1
                cust_object=customer(1,parent_index3,cust_list[parent_index3].id,u[0],u[1])
                cust_list.append(cust_object)
                u_id=cust_list[parent_index3].id
                path_compression(flag,id_merged)
          
            else:
                s=u[0]+u[1]
                if(s not in dict_email_mobile):
                    index+=1
                    cust_list[dict_mobile_parent[u[1]]].sz+=1
                    cust_object=customer(1,dict_email_parent[u[0]],dict_email[u[0]],u[0],u[1])
                    cust_list.append(cust_object)
                    u_id=cust_list[dict_mobile_parent[u[1]]].id
                    if u[0]!='\\Z' or u[1]!='\\Z':
                        s=u[0]+u[1]
                        dict_email_mobile[s]=1
               
                    
    return u_id
# function to add new user or to check the existence and retrieving the id 
# and if required update the dictionaries through calling the update function.
def adduser():
    #import pdb
    #pdb.set_trace()
    inp=raw_input("Enter email_id without starting space:")
    u_email=str(inp)
    inp=raw_input("Enter mobile_no:")
    u_mobile=str(inp)
    user1=str(u_email)+str(u_mobile)
    user=str(u_email)+" "+str(u_mobile)
    if user1 in dict_email_mobile:
        u=user.split()
        if u[0] in dict_email and u[1] in dict_mobile:
            parent_index=dict_email_parent[u[0]]
            u_id=cust_list[parent_index].id
            print("User already exists with id:",u_id)
            return 
        if u[0] in dict_email and u[1] not in dict_mobile:
            parent_index=dict_email_parent[u[0]]
            u_id=cust_list[parent_index].id
            print("User already exist with id:",u_id)
            return 
        if u[0] not in dict_email and u[1] in dict_mobile:
            parent_index=dict_mobile_parent[u[1]]
            u_id=cust_list[parent_index].id
            print("User already exist with id:",u_id)
            return 
    else:
        u_id=update('a',user)
        write()
        print("Database has been updated\nNew id:",u_id)
        return
  
def print_list(x):
    for i in range(len(cust_list)):
        if(cust_list[i].id==x):
            print (str(cust_list[i].email)+"        "+str(cust_list[i].mobile_no))
        
# first function which will run,will read the data file and call other functions 
# accordingly for updation of the database.
def main():
    global id
    global index
    global input_file
    global out_file
    try:
        fh=open(input_file,"r")
    except:
        print("Entered file does not exist")
        exit()
    for line in fh:
        line=line.rstrip()
        u_id=update('p',line)
    path_compression('m',-1)
    fh.close()
    write()
    o='y'
    while o=='y':
        c='n'
        inp=raw_input("press y to enter other user else n:")
        c=str(inp)
        while c=='y' :
            adduser()
            inp=raw_input("Press y to enter other user else n:")
            c=str(inp)
        q='n'
        inp=raw_input("press y to see some id list else n:")
        q=str(inp)
        while q=='y':
            inp=raw_input("Enter id:")
            x=int(inp)
            print_list(x)
            inp=raw_input("press y to see some id list else n:")
            q=str(inp)
        inp=raw_input("Want to do ony other operation y/n:")
        o=str(inp)
            
if __name__ == "__main__":
    main()

                
                
                
                
                
                
                
           
                
 