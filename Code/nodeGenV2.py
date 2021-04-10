import maya.cmds as cmd
import maya.mel as mel
import random as rand

# FACES 168 TO 179 + 424 PER NODE

def gen():
    
    i = 0
    x = 0
    nodeList = []

    while i < 5:
        cmd.polySphere(n='node' + str(i))
        nodeList.append('node' + str(i))
        cmd.move(x)
        x = x - 3
        i = i + 1

    connectNodes(iter(nodeList))

def connectNodes(nodeList):
    print(nodeList)
    #print(next(nodeList))
    cmd.select('node0', 'node1')
    cmd.polyUnite(n='first')
    cmd.select('first.f[150]', 'first.f[574]')
    mel.eval('polyBridgeFaces')
    mel.eval('setAttr "polyBridgeEdge1.divisions" 5')
    mel.eval('setAttr "polyBridgeEdge1.targetDirection" 0')
    mel.eval('setAttr "polyBridgeEdge1.sourceDirection" 0')