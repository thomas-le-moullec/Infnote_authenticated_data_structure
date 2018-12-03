from src import merkle_tree


class Client:
    def __init__(self):
        self.proof_hashes = []

    def check_post(self, hash_post, merkle_root):
        print("Current Stored hash:"+str(self.proof_hashes)+" Merkle root to achieve:"+str(merkle_root)
              +"hash_post to check:"+str(hash_post))
        # Store the correct hashes in proof_hashes
        result = merkle_tree.validate_proof(self.proof_hashes, hash_post, merkle_root)
        index = 1
        self.proof_hashes.append({merkle_tree.get_sibling_pos(index): hash_post})
        return result
