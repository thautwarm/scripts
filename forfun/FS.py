symmetric = ('friend', )

class Node:
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
        self.friends = []
        
    def connect(self, n):
        self.friends.append(n)
        n.friends.append(self)
    def __str__(self):
        return self.name if hasattr(self, 'name') else self
    
A = Node(lang=['C#','JS', 'C', 'Shell'], name='A')
B = Node(lang=['JS', 'Python', 'PHP'], name='B')
C=  Node(lang=['Java', 'Python','HTML'], name='C')
D = Node(lang=['Python', 'Forth', 'JS'], name='D')
E = Node(lang=['Java', 'Kotlin','HTML'], name='E')
F = Node(lang=['Shell', 'JS', 'C'], name='F')
G = Node(lang=['Java', 'C', 'Racket','Tex'], name='G')
H = Node(lang=['Dart', 'C++', 'Kotlin', 'C#', 'Haskell', 'Tex'], name='H')
I = Node(lang=['Haskell', 'HTML', 'C++','Tex'], name='I')
J = Node(lang=['C','Python','Scala'], name='J')

A.connect(H)
B.connect(C)
C.connect(E)
D.connect(A)
E.connect(F)
F.connect(G)
G.connect(E)
H.connect(B)
I.connect(F)
I.connect(J)
J.connect(C)



def DFS(max_depth=10):
    def query(node):
        net = dict()
        idx = 0
        def search(now:Node, depth=0):
            nonlocal idx
            if now in net or depth > max_depth:
                return 
            net[now] = idx
            idx += 1
            for friend in now.friends:
                search(friend, depth+1)
        search(node)
        return net
    return query


from collections import deque
def BFS(now:Node):
    net = dict() # handled
    cache = deque([now])
    idx = 0
    while cache:
        now = cache.popleft()
        net[now] = idx
        idx += 1
        for friend in now.friends:
            if friend not in net: # not handled
                cache.append(friend)
    return net
        
def DBFS(max_depth = 10):
    def query(now:Node):
        net = dict() # handled
        cache = deque([now])
        idx = 0
        depth = 0
        while cache:
            if depth > max_depth:
                break
            for now in cache.copy():
                now = cache.popleft()
                net[now] = idx
                idx += 1
                for friend in now.friends:
                    if friend not in net: # not handled
                        cache.append(friend)
            depth += 1
        return net
    return query

make_op1 = lambda n :  DFS(max_depth=n)
make_op2 = lambda n :  BFS
make_op3 = lambda n :  DBFS(max_depth=n)

for i, make_op in enumerate((make_op1, make_op2, make_op3)):
    print(i)
    for n in range(10):
        op = make_op(n)
        friends = op(A)
        y = [f'{node}' for node in friends]
        print(y)









