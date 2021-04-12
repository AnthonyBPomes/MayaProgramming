import maya.cmds as cmd
import maya.mel as mel
import random as rand

# FACES 0 TO 340 + 424 PER NODE

def gen():
    
    i = 0
    x = 0
    nodeList = []

    while i < 11:
        cmd.polySphere(n='node' + str(i))
        nodeList.append('node' + str(i))
        #cmd.move(x)
        #x = x - 3
        x = rand.uniform(-10,10)
        y = rand.uniform(9-i*2,10-i*2)
        z = rand.uniform(-10,10)
        cmd.move(x,y,z)
        i = i + 1

    cmd.select(all=True)
    cmd.polyUnite(n='nodesCombined')
    connectNodes(nodeList)

def connectNodes(nodeList):
    j = 0
    bottomFace = 0
    topFace = 740
    while j < len(nodeList) - 1:
        print(nodeList[j])
        cmd.select('nodesCombined.f[{}]'.format(bottomFace), 'nodesCombined.f[{}]'.format(topFace))
        mel.eval('polyBridgeFaces')
        mel.eval('setAttr "polyBridgeEdge{}.divisions" 5'.format(j+1))
        mel.eval('setAttr "polyBridgeEdge{}.targetDirection" 0'.format(j+1))
        mel.eval('setAttr "polyBridgeEdge{}.sourceDirection" 0'.format(j+1))
        j = j + 1
        bottomFace = bottomFace + 400
        topFace = topFace + 400