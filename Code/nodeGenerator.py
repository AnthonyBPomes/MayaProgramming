import maya.cmds as cmd
import random as rand

# TODO: CONNECT FACES (EACH NODE HAVE SAME FACE POSITIONS e.g n1.f[154] = n2.f[154]

nodePosList = []

def gen():
    
    i = 0

    while i < 2:
        cmd.polySphere(n='node' + str(i))
        x = rand.uniform(-10,10)
        y = rand.uniform(-10,10)
        z = rand.uniform(-10,10)
        cmd.move(x,y,z)
        nodePosList.append([x,y,z])
        i = i + 1
    
    cmd.select(all=True)
    print(nodePosList)
    for nodePos in nodePosList:
        if CheckQuad(nodePos) == '++':
            print('++')
        elif CheckQuad(nodePos) == '+-':
            print('+-')
        elif CheckQuad(nodePos) == '-+':
            print('-+')
        else:
            print('--')
    # cmd.polyUnite(n='nodesCombined')

def CheckQuad(pos):

    if pos[0] - nodePosList[1][0] > 0 and pos[2] - nodePosList[1][2] > 0:
        return '++'
    if pos[0] - nodePosList[1][0] < 0 and pos[2] - nodePosList[1][2] < 0:
        return '--'
    if pos[0] - nodePosList[1][0] > 0 and pos[2] - nodePosList[1][2] < 0:
        return '+-'
    if pos[0] - nodePosList[1][0] < 0 and pos[2] - nodePosList[1][2] > 0:
        return '-+'