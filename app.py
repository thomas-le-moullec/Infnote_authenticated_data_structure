from src import client
from src import server
from src.mt_tools import Encode, MtTools


def server_simple_insertion_and_reset(server):
    first_posts = ["a", "b", "c"]
    server.mt.add_leaf(first_posts, True)
    server.mt.build_tree()
    server.mt.print_tree()
    server.mt.reset_tree()


def server_demo_merkle_root(server):
    posts = ["Hello", "World", "Nice", "New"]
    server.mt.update_tree(posts, True)
    server.mt.print_tree()
    left = Encode.sha256(Encode.sha256("Hello") + Encode.sha256("World"))
    right = Encode.sha256(Encode.sha256("Nice") + Encode.sha256("New"))
    my_merkle =  Encode.sha256(left + right)
    print("HandCompute merkle root:" + str(my_merkle))
    if my_merkle == server.mt.get_merkle_root():
        print("Merkle is correctly computed !")
    else:
        print("Merkle is not correctly computed !")


def server_demo_update_merkle_root(server):
    new_post = ["NewPost", "Last"]
    server.mt.update_tree(new_post, True)
    server.mt.print_tree()
    one = Encode.sha256(Encode.sha256("Hello") + Encode.sha256("World"))
    second = Encode.sha256(Encode.sha256("Nice") + Encode.sha256("New"))
    third = Encode.sha256(one + second)
    fourth = Encode.sha256(Encode.sha256("NewPost") + Encode.sha256("Last"))
    my_merkle = Encode.sha256(third + fourth)
    print("HandCompute merkle root:" + str(my_merkle))
    if my_merkle == server.mt.get_merkle_root():
        print("Merkle updated is correctly computed !")
    else:
        print("Merkle updated is not correctly computed !")


def test_server(server):
    server_simple_insertion_and_reset(server)  # Insert 3 posts, display the tree and reset it.
    server_demo_merkle_root(server)
    server_demo_update_merkle_root(server)
    path = server.mt.get_proof_by_index(1)  # Get the proof_hashes for the post number 1
    print("Proof for index 1:" + str(path))
    result = MtTools.validate_proof(path, Encode.sha256("World"), server.mt.get_merkle_root())
    if result:
        print("The post 'World' is correctly checked within the tree")
    else:
        print("The post 'World' is not in the tree")


def test_client_server(client, server):
    # Peer just added a new post
    first_message_hash = Encode.sha256("a")
    server.mt.update_tree(first_message_hash)
    # client check validity of data within its own 'light merkle tree'
    print(str(client.add_post(first_message_hash, server.mt.get_merkle_root())))

    second_message_hash = Encode.sha256("b")
    server.mt.update_tree(second_message_hash)
    print(str(client.add_post(second_message_hash, server.mt.get_merkle_root())))


if __name__ == '__main__':
    client = client.Client()  # Light Node
    serverFullNode = server.Server()  # Full Node
    test_server(serverFullNode)  # Test posts insertion within the server
    #test_client_server(client, serverFullNode)  # Test the data validation logic between client and server
