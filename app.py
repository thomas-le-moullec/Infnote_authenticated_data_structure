from src import client
from src import server
from src.encryption import Encode
from src import merkle_tree


def test_merkle_root(server):
    first_posts = ["a", "b", "c"]
    server.mt.update_tree(first_posts, True)
    server.mt.print_tree()
    server.mt.reset_tree()
    posts = ["Hello", "World", "Nice", "New"]
    server.mt.update_tree(posts, True)
    server.mt.print_tree()
    left = Encode.sha256(Encode.sha256("Hello") + Encode.sha256("World"))
    right = Encode.sha256(Encode.sha256("Nice") + Encode.sha256("New"))
    print("My merkle root:" + str(Encode.sha256(left + right)))
    newPost = ["NewPost", "Last"]
    server.mt.update_tree(newPost, True)
    server.mt.print_tree()
    one = Encode.sha256(Encode.sha256("Hello") + Encode.sha256("World"))
    second = Encode.sha256(Encode.sha256("Nice") + Encode.sha256("New"))
    third = Encode.sha256(left + right)
    fourth = Encode.sha256(Encode.sha256("NewPost") + Encode.sha256("Last"))
    print("My merkle root:" + str(Encode.sha256(third + fourth)))
    path = server.mt.get_proof_by_index(1)
    print("Proof for index 1:" + str(path))
    result = merkle_tree.validate_proof(path, Encode.sha256("World"), server.mt.get_merkle_root())
    print("Result:" + str(result))


if __name__ == '__main__':
    client = client.Client()  # Light Node
    server = server.Server()  # Full Node
    # Peer just added a new post
    first_message_hash = Encode.sha256("a")
    server.mt.update_tree(first_message_hash)
    # client check validity of data within its own 'light merkle tree'
    print(str(client.check_post(first_message_hash, server.mt.get_merkle_root())))
    # test_merkle_root(server)

    second_message_hash = Encode.sha256("b")
    server.mt.update_tree(second_message_hash)
    print(str(client.check_post(second_message_hash, server.mt.get_merkle_root())))