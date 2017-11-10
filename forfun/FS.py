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


from collections import deque, OrderedDict
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
                net[now] = idx
                idx += 1
                for friend in now.friends:
                    if friend not in net: # not handled
                        cache.append(friend)
            depth += 1
        return net
    return query
        

def GFS(max_depth_and_with = 2):
    def init(now:Node):
        net = OrderedDict() # handled
        cache = OrderedDict()
        def query(node, max_depth):
            def search(now:Node, depth=0):
                if now in net:
                    return 
                elif depth > max_depth:
                    if now not in cache:
                        cache[now] = None
                    return 
                net[now] = None
                for friend in now.friends[:depth+1]:
                    search(friend, depth+1)
            search(node)
        query(now, max_depth_and_with)
        return net
    return init

                


make_op1 = lambda n :  DFS(max_depth=n)
make_op2 = lambda n :  BFS
make_op3 = lambda n :  DBFS(max_depth=n)
make_op4 = lambda n :  GFS(max_depth_and_with=n)

for i, make_op in enumerate((make_op1, make_op2, make_op3, make_op4)):
    print(i)
    for n in range(10):
        op = make_op(n)
        friends = op(A)
        y = [f'{node}' for node in friends]
        print(y)



func = {0:lambda x,y : (x+1, y),
        1:lambda x,y : (x, y+1),
        2:lambda x,y : (x-1, y),
        3:lambda x,y : (x, y-1)}

class NN:
    def __init__(self, x0=0,y0=0):
        self.elems  = [(x0, y0)]
        self.status = 0
        self.evaluated = 0
    
    def __getitem__(self, i):
        if i < self.evaluated:
            return self.elems[i]
        else:
            while i >= self.evaluated:
                next(self)
            return self.elems[i]
    
        
    def __iter__(self):
        return self
    
    def __next__(self):
        tmp = self.status
        self.evaluated += 1
        self.status = (self.status+1)%4
        self.elems.append(func[tmp](*self.elems[-1]))
        return self.elems[-1]
        

# 无穷邻接?
class Infinite:
    
    def __init__(self, succ = lambda x:x+1, init = 0):
        self.succ = succ
        self.elems = [init]
        self.evaluated = 0
    def __getitem__(self, i):
        if i < self.evaluated:
            return self.elems[i]
        else:
            while i >= self.evaluated:
                next(self)
            return self.elems[i]
    
    def __str__(self):
        return f'{", ".join([str(self[i]) for i in range(10)] + ["..."])}'
            
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.evaluated += 1
        self.elems.append(self.succ(self.elems[-1]))
        return self.elems[-1]

class Sample:
    def __init__(self, deepth = 0, board = 0):
        self.x, self.y = deepth , board
        self._friends = None
        self._next = None
    
    @property
    def friends(self):
        if self._friends is None:
            self._friends = Infinite(lambda s: Sample(s.x, s.y+1), init=Sample(self.x, self.y+1))
        return self._friends

    @property
    def next(self):
        if self._next is None:
            self._next = Sample(self.x+1, self.y)
        return self._next






