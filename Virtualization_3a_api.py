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
	return True
def create_disk(id,no_blocks):
	return 	id
def disk_read(id,block_no,offset,data):
	return data
def disk_write(id,block_no,offset,data):
	return true
def delete_disk(id):
	return true			
