Virtualization & Cloud Computing
================================

Part 1 : Disk Virtualization (Consolidation &  Partirioning)
============================================================
Objectives:
___________
1. Create two arrays for storing Blocks of disks A and B.
2. Block size is 100 bytes. Disk A has 200 blocks and Disk B has 300 Blocks.
3. Provide an API to a programmer so that it appear as one disk D of 500 blocks.
4. APIs could be Write / Read (block_No, block_inf) where block_no is 1..500.
5. Test it with random read / write of blocks.
6. Now create Disk of arbitrary size using an API CreateDisk(ID, No of blocks).
7. Now this ID is used to read and write blocks.
8. APIs could be Read/Write (ID, Block_No, Block_info,).
9. It should return success if Block no within defined limit, else error.
10. Should be able to Create multiple Disk of arbitrary size, till no more space is left.
11. DeleteDisk(ID) would delete the disk and space is released , which can then be used in subsequent Create Disk.
12. Test it using various creates/delete/read/write operations.
13. Arbitrary Create and Delete disk will create holes in the Disk array and you may have to use a different way to store blocks of array in case of fragmentation.

Design:
_______
Block_size : 100 bytes.
V : Array of size: 500 which acts as a virtual memory.
A, B : Actual disks of size 200 and 300 blocks respectively.
Api call Read_Block(block_no, data[, size, offset]): reads "size" bytes data from block "block_no" from V at offset "offset" and returns data into "data". Data size is typically the amount of data present in that block after offset. If size and offset are not given then bydefault size is the size of the block and offset is 0.
Api call Write_Block(block_no, data[, offset]): writes data "data" at offset "offset" into block "block_no" of V. If any data is present initially it simply overwrites it. If data size is more than that of the size left in that block after offset it gives an error saying "data size exceeds the block size". If offset is not given then it takes 0.
User can create multiple disks on top of it by specyfying disk ids viz. 1,2...k (for k number of disks) and the number of blocks which it would contain.
Api call Create_Disk(id, num_blocks): stores a list of blocks for that disk that maps to blocks of virtual disk which are free.
Free_Block_List: stores all the blocks which are free in V.
Map M1 : for mapping ith block of virtual space to blocks of actual disks A, B (consisting of 200 and 300 blocks respectively).
Actual data is stored in A,B.
Api call Delete_Disk(id): simply deletes the disk and corresponding blocks from virtual space V as well as actual disks A, B and adds the blocks to the free block list.
Api call Read_Block(disk_id, block_no, data[, size, offset]): reads data into "data" at offset "offset" from  block "block_no" of disk "disk_id" which the user created intially after checking if the disks exists otherwise throws an exception. Default values of size and offset are same as the previous Read_Block(...) api call.
Api call Write_Block(disk_id, block_no, data[, offset]): writes data "data" into block "block_id" of disk "disk_id" at offset "offset". Offset is by default 0. If disk "disk_id" does not exists then it throws an exception.
All cases of limitations on the values of all the data structures used are handled and throw corresponding exceptions and errors.

Implementation:
_______________
Refer code section.

Part 2: Disk Virtualization : Block Replication
===============================================

Objectives:
___________

1. This is an extension of part 1. Modify the code for part 1 to do Block Replication for providing reliable storage
2. Write each block in two locations, so that in case one copy is in error, block can be read from the 2nd copy.
3. The read operation should read from the first copy. In case it is in error, read from the 2nd copy.
4. Before returning the value to the user, create additional copy in some other location (donot rewrite the error block. Flag it as bad block and never use it again).
5. To simulate random read error, before reading a block generate a random number in the range 1-100. If the value is less than 10, assume reading the first copy has given an error.
6. Test the system by doing large no of read and writes and see what is going on in the background where blocks are stored.

Design:
_______
Basic design is same as the previous part except of the following changes.
Map M2: stores a mapping of (block_id1, block_id2) for replication. Both the blocks have the same data.
The primary block is one which is kept in the block list of a disk and by default read occurs from that.
In case of write first primary copy is written and then corresponding replica is written.
When there is an error reading from primary block, read is made from the corresponding replica and another copy is created before data is transferred to the useer and mapping M2 is updated by adding the new replica mapping and removing the old replica mapping.
For simulating the read error (we can't corrupt a block of our hard disk!) before reading a block we generated a random number in the range 1-100. If the value is less than 10, we assumed reading the first copy has given an error.

Implementation:
_______________
Refer code section.

Part 3: Disk Virtualization (Snapshotting)
==========================================

Objectives:
___________

1. This is an extension of part 1. Modify the code for 3.1 to take a Snap Shot of the current version of the virtual Disk and roll back if needed.
2. This feature lets the user create a checkpoint and then continue using the disk.
3. Any number of checkpoints may be created. The user may return to any checkpoint at any time.
4. API could be
  o Checkpoint (ID, No) No is the Checkpoint ID returned for later use.
  o Rollback (ID, Checkpoint_No) : Rolls back the virtual disk ID
5. Test by doing multiple checkpoints and rolling back to anyone.

Design:
_______
We dump the state of our model which includes the mappings and the data at the time when user requests a snapshot. Before dumping we track the id of the snapshot and append the dump file name with this id and whena user does a rollback we simply search for all the snapshots and model is rolled back to the state whose id is matched with what user has provided.

Implementation:
_______________
Refer code section.

