import Virtualization_3a_helper as disks
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
	if(block_no in free_blocks):
		free_blocks.remove(block_no)
		virtualblock_status[block_no]=0;				
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
def disk_read(id,block_no,offset,data):
	return data
def disk_write(id,block_no,offset,data):
	return true
def delete_disk(id):
	if(id not in disks.virtualdisk_size):
		print "no disk to delete"
		return False
	for i in range(0,len(disks.virtualdisk_block[id])):
		disks.free_blocks.append(disks.virtualdisk_block[id][i])
		disks.virtualblock_status[disks.virtualdisk_block[id][i]]=1
		if(disks.second_copy[disks.virtualdisk_block[id][i]]!=-1):
			disks.free_blocks.append(disks.second_copy(disks.virtualdisk_block[id][i]))	
			disks.virtualdisk_block[disks.virtualdisk_block[id][i]]=1
			disks.second_copy[disks.virtualdisk_block[id][i]]=-1
	del disks.virtualdisk_size[id]
	del disks.virtualdisk_block[id]						
	return True
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

