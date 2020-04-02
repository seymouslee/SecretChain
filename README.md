# SecretChain

Run this program in Python2.7 and install these packages:
- requests
- flask

now grab 2 computers that are connected to the same network.
To find the IPv4 address for each of the pc: run cmd > type in "ipconfig" > search for IPv4 address.

Run the same program on both of the computers.

Assuming (for your own PCs, find the IPv4 in cmd):
PC-A: 192.168.0.169:5000
PC-B: 192.168.0.105:5000
(port 5000 is set by the program)

1. after running the program, open up your browser
2. on PC-A, run command "localhost:5000/blocks" to see the orignal blockchain. There should only be 4 of them.
3. on PC-A, run "localhost:5000/addNode?name=test"
    - note that test is the name of the new block, replace test with whatever you want.
    - run "localhost:5000/blocks" to check if the new block has been added.
4. on PC-A, run "192.168.0.169:5000/addPeer"
    - 192.168.0.169 is the address of my own PC-B computer
5. on PC-B, run "localhost:5000/blocks" should have the test block added from PC-A


Project Demo:
- "Query and receive the response of the latest block between two nodes"
1. run command "localhost:5000/latest"

- "Query and receive the response of the timestamp a particular block"
1. run command "localhost:5000/queryTime?Index=1"
    - 1 in the example being the block index you're searching for.
    
- just searching for a block in general:
1. run command "localhost:5000/query?Index=1"
    shows all the details for the block
