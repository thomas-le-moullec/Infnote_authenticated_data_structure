from src import client
from src import server
from src import merkle_tree

if __name__ == '__main__':
    mt = merkle_tree.MerkleTree()
    client = client.Client()
    server = server.Server()
