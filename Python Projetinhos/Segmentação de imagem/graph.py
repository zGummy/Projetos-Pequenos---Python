
'''
Defina a classe de vértice (nó) e defina cada pixel como um nó (vértice). O vértice tem três propriedades:
(1) pai, o vértice corresponde ao vértice pai da área segmentada, que pode ser considerado como o número ou índice da área segmentada.
Na inicialização subsequente, cada pixel da imagem é considerado uma área de segmentação, de modo que o vértice mãe de cada pixel é ele mesmo.
(2) rank, a prioridade do vértice pai (cada vértice é inicializado com 0), usado para determinar o único vértice pai quando duas regiões são mescladas.
(3) size (Cada vértice é inicializado com 1), o que indica o número de vértices na região dividida quando cada vértice é usado como vértice pai.
Quando ele é mesclado por outras regiões e não é mais um vértice pai, seu tamanho não muda mais.
'''
class Node:
    def __init__(self, parent, rank=0, size=1):
      #A mesma área, expressa como o mesmo pai, pode ser expressa como se as duas áreas fossem iguais / dois pixels são iguais, a color[parent] é a mesma, ou seja, a mesma cor        self.parent = parent

        self.parent = parent
        self.rank = rank
        self.size = size

    def __repr__(self):
        return '(parent=%s, rank=%s, size=%s)' % (self.parent, self.rank, self.size)

'''
(1) self.nodes inicializa a lista de todos os vértices da classe floresta e usa cada pixel da imagem como um vértice durante a inicialização.
Como uma área segmentada, o vértice mãe de cada pixel é ele mesmo. forest.num_sets representa o número atual de regiões divididas da imagem.
(2) size_of (), obtém o tamanho de um determinado vértice, geralmente usado para obter o tamanho de um determinado vértice mãe, ou seja, o número de vértices na área de partição onde o vértice mãe está localizado.
(3) find (), obtém o número do vértice pai (índice) da região onde o vértice está localizado
'''
class Forest:
    def __init__(self, num_nodes):
        self.nodes = [Node(i) for i in range(num_nodes)]
        self.num_sets = num_nodes
    #O tamanho da área onde o vértice está localizado (incluindo o número de pixels)
    def size_of(self, i):
        return self.nodes[i].size
    #Este vértice corresponde ao vértice mãe da região dividida
    def find(self, n):
        temp = n
        while temp != self.nodes[temp].parent:
            temp = self.nodes[temp].parent

        self.nodes[n].parent = temp
        return temp
    #Unir duas regiões
    def merge(self, a, b):
        if self.nodes[a].rank > self.nodes[b].rank:
            self.nodes[b].parent = a
            self.nodes[a].size = self.nodes[a].size + self.nodes[b].size
        else:
            self.nodes[a].parent = b
            self.nodes[b].size = self.nodes[b].size + self.nodes[a].size

            if self.nodes[a].rank == self.nodes[b].rank:
                self.nodes[b].rank = self.nodes[b].rank + 1

        self.num_sets = self.num_sets - 1

    def print_nodes(self):
        for node in self.nodes:
            print(node)
# Crie uma aresta, a direção de (x, y) para (x1, y1), o tamanho é o valor do gradiente
def create_edge(img, width, x, y, x1, y1, diff):
    #De acordo com nossa ordem de leitura, leia cada linha de cima para baixo e cada linha é numerada da esquerda para a direita.
    vertex_id = lambda x, y: y * width + x
    w = diff(img, x, y, x1, y1)
    return (vertex_id(x, y), vertex_id(x1, y1), w)

#Crie um gráfico. Para cada vértice, ← ↑ ↖↗ cria quatro arestas para obter o efeito de vizinhança 8. Desde então, a construção do gráfico foi concluída.
def build_graph(img, width, height, diff, neighborhood_8=False):
    graph_edges = []
    for y in range(height):
        for x in range(width):
            if x > 0:
                graph_edges.append(create_edge(img, width, x, y, x-1, y, diff))

            if y > 0:
                graph_edges.append(create_edge(img, width, x, y, x, y-1, diff))

            if neighborhood_8:
                if x > 0 and y > 0:
                    graph_edges.append(create_edge(img, width, x, y, x-1, y-1, diff))

                if x > 0 and y < height-1:
                    graph_edges.append(create_edge(img, width, x, y, x-1, y+1, diff))

    return graph_edges

'''
Após a segmentação inicial, as duas áreas adjacentes onde o número de pontos fixos são menores que min_size são mescladas.
'''
def remove_small_components(forest, graph, min_size):
    for edge in graph:
        a = forest.find(edge[0])
        b = forest.find(edge[1])

        if a != b and (forest.size_of(a) < min_size or forest.size_of(b) < min_size):
            forest.merge(a, b)

    return  forest


'''
(1) Inicialize primeiro a floresta
(2) Para todas as bordas, classifique-as de acordo com seus pesos, de pequeno a grande
(3) Inicializar a lista de diferenças internas da área
(4) Percorra todas as arestas de pequeno a grande, se os vértices estiverem em duas regiões, e o peso for menor que a diferença interna das regiões onde os dois vértices estão localizados （threshold[]）,
Em seguida, mescle as duas regiões, encontre o novo vértice-mãe da região mesclada e atualize a diferença interna da região correspondente ao vértice （threshold[]）:
threshold[i]=Int(Ci)+ k/|Ci|
Int (Ci) é a diferença interna da área onde o vértice i está localizado; ∣Ci∣ é o número de vértices na área;
k é um parâmetro ajustável. Se k for muito grande, a diferença interna da região durante a atualização é muito grande, resultando em muitas regiões a serem mescladas e, por fim, resultando em segmentação de imagem grosseira. Ao contrário, se k for muito pequeno , é fácil fazer com que a segmentação da imagem fique muito fina.
Como a travessia é de pequeno a grande, se mesclada, o peso dessa aresta deve ser o maior peso de todas as arestas na nova área.
Essa é a diferença interna da nova área, então Int(Ci)=weight(edge)
'''
def segment_graph(graph_edges, num_nodes, const, min_size, threshold_func):
    # Step 1: initialization
    forest = Forest(num_nodes)
    weight = lambda edge: edge[2]
    sorted_graph = sorted(graph_edges, key=weight)
    threshold = [ threshold_func(1, const) for _ in range(num_nodes) ]

    # Step 2: merging
    for edge in sorted_graph:
        parent_a = forest.find(edge[0])
        parent_b = forest.find(edge[1])

        #Quando a lacuna entre as classes é menor do que a lacuna dentro das classes, a condição é True, indicando que pode ser mesclada
        a_condition = weight(edge) <= threshold[parent_a]
        b_condition = weight(edge) <= threshold[parent_b]

        #Se os vértices estão em duas áreas, e o peso é menor do que a diferença interna das áreas onde os dois vértices estão localizados (threshold[]), mescle as duas áreas
        if parent_a != parent_b and a_condition and b_condition:
            forest.merge(parent_a, parent_b)
            a = forest.find(parent_a)
            threshold[a] = weight(edge) + threshold_func(forest.nodes[a].size, const)

    return remove_small_components(forest, sorted_graph, min_size)
