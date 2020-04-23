from hashlib import sha256


class MerkleNode:
    """
    Nếu là nút lá thì lưu mã hash, giá trị phần dữ liệu và nút cha.
    Nếu là nút cha thì lưu thêm 2 nút con
    """
    def __init__(self, hash, chunk=None):
        self.chunk = chunk
        self.hash = hash
        self.parent = None
        self.left_child = None
        self.right_child = None


class MerkleTree:
    """
    Lưu nút lá và tính root hash
    """
    def __init__(self, data_chunks):
        self.leaves = []

        for chunk in data_chunks:
            node = MerkleNode(self.compute_hash(chunk), chunk=chunk)
            self.leaves.append(node)

        self.root = self.build_merkle_tree(self.leaves)

    def build_merkle_tree(self, leaves):
        """
        Tạo Merkle trees từ các nút lá. 
        Nếu số lượng nút lá lẻ, nút cuối sẽ được nhân đôi để ghép cặp chính nó.
        """
        num_leaves = len(leaves)
        if num_leaves == 1:
            return leaves[0]

        parents = []

        i = 0
        while i < num_leaves:
            left_child = leaves[i]
            right_child = leaves[i + 1] if i + 1 < num_leaves else left_child

            parents.append(self.create_parent(left_child, right_child))

            i += 2

        return self.build_merkle_tree(parents)

    def create_parent(self, left_child, right_child):
        """
        Tạo nút cha từ 2 nút con.
        """
        parent = MerkleNode(
            self.compute_hash(left_child.hash + right_child.hash), left_child.chunk + right_child.chunk)
        left_child.parent, right_child.parent = parent, parent
        parent.left_child, parent.right_child = left_child, right_child
        
        print ("---------")
        print("Left child {}: {}, Right child {}: {}, Parent {}: {}".format(
            left_child.chunk, left_child.hash, right_child.chunk, right_child.hash, parent.chunk, parent.hash))
        return parent

    @staticmethod
    def compute_hash(data):
        data = data.encode('utf-8')
        return sha256(data).hexdigest()

    def getMerklePath(self, chunk):
        """
        Kiểm tra xem nút có tồn tại và tìm Merkle path cho nó.
        """

        hash = self.compute_hash(chunk)

        for leaf in self.leaves:
            if leaf.hash == hash:
                print("leaf exist")
                return self.generateMerklePath(leaf)
        
        return False

    def generateMerklePath(self, node, path = []):
        """
        Sinh ra Merkle Path từ dưới lên trên.
        """

        if node == self.root:
            path.append(node.hash)
            return path

        isLeft = (node.parent.left_child == node)
        if isLeft:

            path.append((node.parent.right_child.hash, not isLeft))
            return self.generateMerklePath(node.parent, path)
        else:
            path.append((node.parent.left_child.hash, not isLeft))
            return self.generateMerklePath(node.parent, path)

    def verifyMerklePath(self, chunk, path):
        """
        Xác minh xem nút có tồn tại không bằng Merkle Path.
        """

        sumHash = self.compute_hash(chunk)
        
        for hashNode in path[:-1]:
            hash = hashNode[0]
            isLeft = hashNode[1]
            if isLeft:
                sumHash = self.compute_hash(hash + sumHash)
            else:
                sumHash = self.compute_hash(sumHash + hash)

        return sumHash == path[-1]



if __name__ == "__main__":
    lst = list("01234567")
    merkle = MerkleTree(lst)

#     # path = merkle.getMerklePath("2")

#     # verify = merkle.verifyMerklePath("2", path)
#     # print(verify)