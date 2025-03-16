# VR2 Hash - MK11
Python [re-implementation of the VR2 Hash](/proper/Hasher.py) used in MK11
[Reimplements a custom variant](/proper/MersenneTwister.py) of [MT19937](https://en.wikipedia.org/wiki/Mersenne_Twister) as well since it's used for generating the Seed Table.

[Proper](/proper) contains the re-implementations in Python, while the other folders contain the RAW direct from assembly remake.

# Behavior of VR2
First the game uses MT19937 with an initial seed set in the state array's first index.
After that, the game generates 8 random seeds, one a combination of System Time multiplied with Epoch time, and 7 pure randoms.
These 9 seeds are used to generate the state array.

Once the State Array is created, the game creates an array of size 2 Million that is full of randoms generated from the MT object.
4 Indices are then randomly select (MT%2 Million) and a random XOR key to encrypt the 4 indices (Security measure, not optimization).

During hashing, the game uses 4 keys created from the 4 indices ^ with the next indices.
Example:
```
Indices 1^2 9^10 17^18 55^56
```
These 4 keys are then used to hash the string to ensure consistency with the game server.

After you login, the 4 indices' bytes are changed (possibly XORed with the desired key). So for the example above only indices 1 9 17 and 55 are changed.
The XOR result for each index will now result in 4 consistent keys that do not change across runs.

# Possible Shortcuts
Shortcut 1:
No need to remake the MT, can just use `random`


Shortcut 2:
No need to generate the 2 Million Records and the XOR key, can simply immediately generate 8 random ints.

Shortcut 3:
Perhaps no need to generate the 8 random ints, can just use the key retrieved from the server `MK11.exe+B1B075`, eliminating the need for the random generation process.