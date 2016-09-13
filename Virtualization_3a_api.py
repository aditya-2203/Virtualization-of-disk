import Virtualization_3a_helper as disks
import random
def read_data(data,block_no,offset,length):
	if(offset+length>100):		#Removed the equality condition
		print "invalid length"
		data=None	#null is not defined in python.
		return
	if(block_no>=500):
		print "invalid block number"
		data=None
		return	
	(disk_id,block_id)=disks.virtualblock_physical(block_no)
	data=""
	temp_byte=[]
	if(disk_id==0):
		for i in range(offset,offset+length):
			temp_byte.append(disks.disk_A[block_id][i]);
	elif(disk_id==1):
		for i in range(offset,offset+length):
			temp_byte.append(disks.disk_B[block_id][i]);
	else:
		print "invalid block no"
		data=None
		return
	data="".join(map(chr,temp_byte))				
	return data
def write_data(block_no,offset,data):
	if(offset+len(data)>100):	 #Removed the equality condition.
		print "invalid length"
		return False
	if(block_no>=500):
		print "invalid block number"
		data=null
		return False
	(disk_id,block_id)=disks.virtualblock_physical(block_no)
	length=len(data)
	list_bytes=list(bytearray(data))
	print list_bytes		
	if(disk_id==0):
		for i in range(offset,offset+length):
			disks.disk_A[block_id][i]=list_bytes[i-offset]
	elif(disk_id==1):
		for i in range(offset,offset+length):
			disks.disk_B[block_id][i]=list_bytes[i-offset]
	else:
		print "invalid block no"
		return False;
	if(block_no in disks.free_blocks):
		disks.free_blocks.remove(block_no)
		disks.virtualblock_status[block_no]=0;				
	return True
def create_disk(id,no_blocks):
	id=disks.get_newdisk_id()
	if(len(disks.free_blocks)<no_blocks):
		print "do not have that much of space."
		return -1;
	disks.virtualdisk_size[id]=no_blocks
	disks.virtualdisk_block[id]=disks.free_blocks[0:no_blocks]
	for i in range(0,len(disks.virtualdisk_block[id])):
		disks.virtualblock_status[disks.virtualdisk_block[id][i]]=0
	disks.free_blocks=disks.free_blocks[no_blocks:]		
	return 	id

def disk_read(id,block_no,offset,data,length):
	#Simulate the random error.
	number  =  random.randint(0,100)
	block_no = disks.virtualdisk_block[id][block_no-1]	#Get the virtual block.
	if number < 10:		
		#Data is read from duplicate copy.
		dblock_no = disks.second_copy[block_no]
		disks.second_copy[block_no]=-1		
		data = read_data(data,dblock_no,offset,length)
		#Pick up another block for replication.
		if len(disks.free_blocks) == 0:
			print "No space for replicating data, data space full !!"
			return False	
		else:
			pblock_no = disks.free_blocks[0]
		#Retrieve block data from duplicate block. 		
		block_data = read_data(data,dblock_no,0,100)
		if not(write_data(pblock_no,0,block_data)):
			return False
		#Mapping between duplicate block and new block.
		disks.second_copy[dblock_no] = pblock_no
	else:
		#Data is read from primary block number.
		data = read_data(data,block_no,offset,length)
	return data

def disk_write(id,block_no,offset,data):
	#List the first virtual blockid from given (diskid,blockno).
	if block_no <= len(disks.virtualdisk_block[id]):
		vblock_id1 = disks.virtualdisk_block[id][block_no-1]
	else:
		print 'disk id %d does not have block_id %d'%(id,block_no)
		return False
	#Write the data in virtual block.
	if not(write_data(vblock_id1,offset,data)):
		return False
	#Find the second block to copy the given data.
	if len(disks.free_blocks) == 0:
		print "No space for replicating data, data space full !!"
		return False
	else:
		vblock_id2 = disks.free_blocks[0]
	#Write data in duplicated block.
	if not(write_data(vblock_id2,offset,data)):
		return False
	#Create a mapping if above steps donot fail.
	disks.second_copy[vblock_id1] = vblock_id2	
	return True

def delete_disk(id):
	if(id not in disks.virtualdisk_size):
		print "no disk to delete"
		return False
	for i in range(0,len(disks.virtualdisk_block[id])):
		disks.free_blocks.append(disks.virtualdisk_block[id][i])
		disks.virtualblock_status[disks.virtualdisk_block[id][i]]=1
		if(disks.second_copy[disks.virtualdisk_block[id][i]]!=-1):
			disks.free_blocks.append(disks.second_copy(disks.virtualdisk_block[id][i]))	
			#disks.virtualdisk_block[disks.virtualdisk_block[id][i]]=1
			disks.second_copy[disks.virtualdisk_block[id][i]]=-1
	del disks.virtualdisk_size[id]
	del disks.virtualdisk_block[id]						
	return True


def TestWrite():
	data = "i m well under 100 characters"
	next = "Well under 4 years"
	write_data(1,50,data)
	write_data(1,54,next)
	print read_data(data,1,40,70),' Case 1'
	print read_data(data,9,10,80),' Case 2'
	print read_data(data,1,50,30),' Case 3'
	print 1 in disks.free_blocks,disks.virtualblock_status[1]
	create_disk(0,5)
	create_disk(5,5)
	disk_write(1,4,45,next)	
	print disks.second_copy[9],read_data(data,9,10,80),'Case 4',read_data(data,disks.second_copy[9],60,20)
	print disk_read(1,4,50,data,30),'Case 6'
	print read_data(data,12,0,100),'Case 7'	
	print data
	print disks.virtualdisk_block[0],disks.virtualdisk_block[1],2 in disks.free_blocks

import pickle	
def create_checkpoint():
	id=disks.checkpoint_no;
	disks.checkpoint_no+=1;
	filename="checkpoint_"+str(id)+"_";
	pickle.dump(disks.virtualdisk_block,open(filename+"virtualdisk_block","wb"));
	pickle.dump(disks.second_copy,open(filename+"second_copy","wb"));
	pickle.dump(disks.free_blocks,open(filename+"free_blocks","wb"));
	pickle.dump(disks.virtualblock_status,open(filename+"virtualblock_status","wb"));
	pickle.dump(disks.disk_A,open(filename+"disk_A","wb"));
	pickle.dump(disks.disk_B,open(filename+"disk_B","wb"));
	return id;
def restore_checkpoint(id):
	filename="checkpoint_"+str(id)+"_";
	disks.virtualdisk_block=pickle.load(open(filename+"virtualdisk_block","rb"));
	disks.second_copy=pickle.load(open(filename+"second_copy","rb"));
	disks.free_blocks=pickle.load(open(filename+"free_blocks","rb"));
	disks.virtualblock_status=pickle.load(open(filename+"virtualblock_status","rb"));
	disks.disk_A=pickle.load(open(filename+"disk_A","rb"));
	disks.disk_B=pickle.load(open(filename+"disk_B","rb"));

TestWrite()

