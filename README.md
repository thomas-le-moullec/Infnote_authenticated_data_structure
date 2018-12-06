# Infnote_authenticated_data_structure
Merkle tree implementation - Light node client with limited storage and a Full node server which is storing the entire merkle tree.

### Project structure:
* app.py offer a simple example of the implementation of the merkle tree. Full Node and Light Node implementation
* merkle_tree.py contains the entire logic of the merkle tree implementation
* mt_tools contain the common methods and logic that can be used by a Full node and a Light Node.
* encryption.py is a simple encapsulation of cryptography functions used for hash.
* server.py is a simplify full node
* client.py is a simplify light node

### Run the tests
In project root folder:
python -m unittest tests/merkle_tree_test.py
Currently 11 tests

### TO DO:
* For the light node, we need the function to update the proof hashes to prepare the next post check.

#### Rights and License:
GNU GENERAL PUBLIC LICENSE - Check LICENSE file