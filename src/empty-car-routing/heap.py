import heapq

class Heap:
    def __init__(self):
        self._heap = []
        self._index = 0

    def push(self, item, t):
        heapq.heappush(self._heap, (t, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._heap)[-1]  
        #,self._heap  #[-1]表示只输出name
        #heapq.heappop(heap) 弹出索引位置0中的值
    def pushpop(self, item, t):
        temp =  heapq.heappushpop(self._heap, (t, self._index, item))
        self._index += 1
        return temp



class Item:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return 'Item({!r})'.format(self.name)