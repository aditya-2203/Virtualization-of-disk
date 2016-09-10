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


Implementation:
_______________


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


Implementation:
_______________


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


Implementation:
_______________


