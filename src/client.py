from src.mt_tools import MtTools


class Client:
    def __init__(self):
        self.proof_hashes = []

    def _store_proof_hashes(self, hash_post):
        index = 1
        self.proof_hashes.append({MtTools.get_sibling_pos(index): hash_post})

    def check_post(self, hash_post, merkle_root):
        print("Current Stored hash:"+str(self.proof_hashes)+" Merkle root to achieve:"+str(merkle_root)
              + "hash_post to check:"+str(hash_post))
        # Store the correct hashes in proof_hashes
        result = MtTools.validate_proof(self.proof_hashes, hash_post, merkle_root)
        self._store_proof_hashes(hash_post)
        return result
