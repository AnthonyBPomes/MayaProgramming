import maya.cmds as cmd
import maya.mel as mel
import random as rand

# FACES 0 TO 340 + 424 PER NODE

def gen(numberOfNodes):
    
    i = 0
    x = 0
    nodeList = []

    while i < numberOfNodes:
        cmd.polySphere(n='node' + str(i))
        nodeList.append('node' + str(i))
        #cmd.move(x)
        #x = x - 3
        x = rand.uniform(-10,10)
        y = rand.uniform(-10,10)
        z = rand.uniform(-10,10)
        #mel.eval('sets -e -forceElement standardSurface{}SG'.format(rand.randint(2,5)))
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
        if j == 0:
            bottomFace = bottomFace + 399
        else:
            bottomFace = bottomFace + 398
        topFace = topFace + 398
        j = j + 1