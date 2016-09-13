from collections import defaultdict
#virtual blocks are numbered from 0 to 499
#virtual disk has key as disk and returns list of virtual block
virtualdisk_block=defaultdict(list)

#size of each virtual disk mapping
virtualdisk_size={}
checkpoint_no=0;
#list contain second copy for all block
# 0 if second copy, -1 if no copy 
second_copy=[]
for i in range(0,500):
	second_copy.append(-1);

#list of free blocks
free_blocks=[]
for i in range(0,500):
	free_blocks.append(i);

#list for each block if it free or not
# 1 if it is free else 0
virtualblock_status=[]
for i in range(0,500):
	virtualblock_status.append(1);

#give physical disk details corresponding to  
def virtualblock_physical(block_no):
	if(block_no<300):
		return (0,block_no)
	else:
		return(1,block_no-300)

#disk A
disk_A=[];
for i in range(0,300):
	disk_A.append(bytearray(100));

#disk B
disk_B=[]
for i in range(0,200):
	disk_B.append(bytearray(100));	

#getting id for new virtual disk
def get_newdisk_id():
	max_till_now1=-1
	global virtualdisk_size
	for key in virtualdisk_size:
		print key
		if(key>max_till_now1):
			max_till_now1=key
	return (max_till_now1+1)	