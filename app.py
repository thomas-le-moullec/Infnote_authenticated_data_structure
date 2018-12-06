from src import client
from src import server
from src.mt_tools import Encode, MtTools


def server_simple_insertion_and_reset(serverFullNode):
    first_posts = ["a", "b", "c"]
    serverFullNode.mt.add_leaf(first_posts, True)
    serverFullNode.mt.build_tree()
    serverFullNode.mt.print_tree()
    serverFullNode.mt.reset_tree()


def server_demo_merkle_root(serverFullNode):
    posts = ["Hello", "World", "Nice", "New"]
    serverFullNode.mt.update_tree(posts, True)
    serverFullNode.mt.print_tree()
    left = Encode.sha256(Encode.sha256("Hello") + Encode.sha256("World"))
    right = Encode.sha256(Encode.sha256("Nice") + Encode.sha256("New"))
    my_merkle =  Encode.sha256(left + right)
    print("HandCompute merkle root:" + str(my_merkle))
    if my_merkle == serverFullNode.mt.get_merkle_root():
        print("Merkle is correctly computed !")
    else:
        print("Merkle is not correctly computed !")


def server_demo_update_merkle_root(serverFullNode):
    new_post = ["NewPost", "Last"]
    serverFullNode.mt.update_tree(new_post, True)
    serverFullNode.mt.print_tree()
    one = Encode.sha256(Encode.sha256("Hello") + Encode.sha256("World"))
    second = Encode.sha256(Encode.sha256("Nice") + Encode.sha256("New"))
    third = Encode.sha256(one + second)
    fourth = Encode.sha256(Encode.sha256("NewPost") + Encode.sha256("Last"))
    my_merkle = Encode.sha256(third + fourth)
    print("HandCompute merkle root:" + str(my_merkle))
    if my_merkle == serverFullNode.mt.get_merkle_root():
        print("Merkle updated is correctly computed !")
    else:
        print("Merkle updated is not correctly computed !")


def server_demo_valid_data(serverFullNode):
    path = serverFullNode.mt.get_proof_by_index(1)  # Get the proof_hashes for the post number 1
    print("Proof for index 1:" + str(path))
    result = MtTools.validate_proof(path, Encode.sha256("World"), serverFullNode.mt.get_merkle_root())
    if result:
        print("The post 'World' is correctly checked within the tree")
    else:
        print("The post 'World' is not in the tree")


def server_demo_not_valid_data(serverFullNode):
    path = serverFullNode.mt.get_proof_by_index(1)  # Get the proof_hashes for the post number 1
    print("Proof for index 1:" + str(path))
    result = MtTools.validate_proof(path, Encode.sha256("NotInTheTreeData"), serverFullNode.mt.get_merkle_root())
    if result:
        print("The post 'NotInTheTreeData' is correctly checked within the tree")
    else:
        print("The post 'NotInTheTreeData' is not in the tree")


def two_full_node_demo(server1, server2):
    first_post = "Previous Post"
    second_post = "Last Post"
    third_post = "third post"
    wrong_post = "Wrong post"

    # Reset the data structure
    server1.reset_data()

    # Insert a first correct post
    server1.mt.add_leaf(first_post, True)
    server1.mt.build_tree()
    result_first_post = server2.add_post(first_post, server1.mt.get_merkle_root(), True)
    if result_first_post:
        print("Full Node 2 has correctly accepted post:'"+first_post+"' !")
    else:
        print("Full Node 2 has not accepted post:'" + first_post + "' !")

    #  Insert a new Correct Post
    server2.mt.update_tree(second_post, True)
    result_second_post = server1.add_post(second_post, server2.mt.get_merkle_root(), True)
    if result_second_post:
        print("Full Node 1 has correctly accepted post:'"+second_post+"' !")
    else:
        print("Full Node 1 has not accepted post:'" + second_post + "' !")

    #  Insert a Incorrect post
    server2.mt.update_tree(third_post, True)
    result_third_post = server1.add_post(wrong_post, server2.mt.get_merkle_root(), True)
    if result_third_post:
        print("Full Node 1 has correctly accepted post:'"+wrong_post+"' - This is an error !!")
    else:
        print("Full Node 1 has not accepted post:'" + wrong_post + "' - This is the correct logic")

def test_server(serverFullNode):
    server_simple_insertion_and_reset(serverFullNode)  # Insert 3 posts, display the tree and reset it.
    server_demo_merkle_root(serverFullNode)
    server_demo_update_merkle_root(serverFullNode)
    server_demo_valid_data(serverFullNode)
    server_demo_not_valid_data(serverFullNode)
    new_server = server.Server()
    two_full_node_demo(serverFullNode, new_server)


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
