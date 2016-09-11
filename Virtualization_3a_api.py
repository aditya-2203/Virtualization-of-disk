import Virtualization_3a_helper as disks
import random
def read_data(data,block_no,offset,length):
	if(offset+length>=100):
		print "invalid length"
		data=null
		return
	if(block_no>=500):
		print "invalid block number"
		data=null
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
		data=null;
		return;
	data="".join(map(chr,temp_byte))				
	return data
def write_data(block_no,offset,data):
	if(offset+len(data)>=100):
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
	if(block_no not in free_blocks):
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
	if number < 10:		
		#Data is read from duplicate copy.
		dblock_no = disks.second_block[block_no]
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
		data = read_write(data,block_no,offset,length)
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
