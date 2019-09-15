import json
import os
import sys

class Method:
    def __init__(self, params):
        self.name = params["out_goods"][0] #only one out_goods, use it as method_name
        self.time = float(params["time"])
        self.plant = params["plant"]
        self.in_goods = params["in_goods"]
        self.out_goods = params["out_goods"]
        self.in_num = params["in_num"]
        self.out_num = params["out_num"]
        
class Goods:
    def __init__(self, name, id):
        self.method = None
        self.name = name
        self.id = id
    
    def add(self, x):
        self.method = x


def main():
    a = input("input method name:")
    b = input("input target name:")
    cnt = 0
    goods_id = {}
    id_goods = []
    methods = []
    goods = []
    fp = open("./method/" + a + ".json")
    for line in fp.readlines():
        x = json.loads(line)
        for i, good in enumerate(x["in_goods"]):
            if good not in goods_id:
                goods_id[good] = cnt
                id_goods.append(good)
                goods.append(Goods(good, cnt))
                cnt += 1
            x["in_goods"][i] = goods_id[good]
        for i, good in enumerate(x["out_goods"]):
            if good not in goods_id:
                goods_id[good] = cnt
                id_goods.append(good)
                goods.append(Goods(good, cnt))
                cnt += 1
            goods[goods_id[good]].add(len(methods))
            x["out_goods"][i] = goods_id[good]
        #print(x)
        methods.append(Method(x))
    #print(goods_id)
    #print(id_goods)
    #for x in goods:
    #    print(x.name, x.id, x.method)
    
    global goods_num
    goods_num = []
    methods_num = []
    for i in range(len(goods_id)):
        goods_num.append(0)
    for i in range(len(methods)):
        methods_num.append(0)

    def dfs(good, num):
        #print(id_goods[good], num)
        global goods_num
        goods_num[good] -= num
        if goods[good].method == None:
            return
        if goods_num[good] >= 0:
            return

        t = num - goods_num[good]
        method = methods[goods[good].method]
        #print(method.name, good)
        for i in range(len(method.out_goods)):
            if method.out_goods[i] == good:
                d = num // method.out_num[i]
                if num % method.out_num[i] != 0:
                    d += 1
                #print(d)
                methods_num[goods[good].method] += d
                goods_num[good] += method.out_num[i] * d
                for j in range(len(method.in_goods)):
                    dfs(method.in_goods[j], method.in_num[j] * d)
                break


    fp = open("./target/" + b + ".txt")
    for line in fp.readlines():
        line = line.split()
        dfs(goods_id[line[0]], int(line[1]))
    print("goods:")
    for i in range(len(goods_id)):
        if goods[i].method == None:
            print(id_goods[i], goods_num[i])
    print("methods:")
    for i in range(len(methods)):
        if methods_num[i] != 0:
            print(id_goods[methods[i].name], methods_num[i])


if __name__ == "__main__":
    main()