import csv
import maya.cmds as cmd
import maya.mel as mel
import pymel.core as pm
import maya.OpenMaya as OpenMaya
import random as rand
import colorsys
import math
import sys

data_blue = []
data_red = []
data_yellow = []
data_green = []
sets = [data_yellow,data_green,data_blue]
new_connections = []
new_connections_2 = []
j = 0
model_list = [{'phone': 'Social Media Users'},{'headphones': 'Online Music Listeners'},{'tv': 'Binge Watchers'},{'pets': 'Pet Owners'},{'active': 'Physically Active'},{'car': 'Regular Drivers'},{'culture': 'Cultural Participation'},{'coffeecup': 'Hot Drink Consumers'},{'degree': 'Graduates With Degrees'},{'beer': 'Craft Beer Drinkers'},{'house': 'Home Owners'},{'smoke': 'Smokers'}]

cmds.directionalLight()
cmds.directionalLight(rot=(90,0,0))
cmds.directionalLight(rot=(180,0,0))
cmds.directionalLight(rot=(270,0,0))

def textToSpacedHex(in_text):
    out = []
    for c in in_text:
        hx = c.encode('hex')
        out.append(hx)
    return ' '.join(out)

def gen(data_red,data_yellow,data_green,data_blue,):
    
    i = 0
    x = 0
    nodeList = []
    dist_coords = fibonacci_sphere(len(data_red))
    dist_modif = 4.5
    mel.eval('shadingNode -asUtility floatConstant')

    while i < len(data_red):
        cmd.polySphere(n=data_red[i],r=6)
        nodeList.append(data_red[i])
        #cmd.move(x)
        #x = x - 5
        x = dist_coords[i][0] * dist_modif
        y = dist_coords[i][1] * dist_modif
        z = dist_coords[i][2] * dist_modif
        calculate_node_colour([data_red,data_yellow,data_green,data_blue],i,data_red[i])
        #mel.eval('sets -e -forceElement standardSurface{}SG'.format(rand.randint(2,5)))
        cmd.select(data_red[i])
        cmd.move(x,y,z)
        i = i + 1

    cmd.select(all=True)
    cmd.polyUnite(n='nodesCombined')
    connectNodes(nodeList)
    
    i = 0
    
    while i < len(data_red):
        cmd.polyCube()
        #mel.eval('file -import -type "mayaBinary"  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "FF" -options "v=0;"  -pr  -importTimeRange "combine" "F:/Major Project 2/MayaFiles/MajorProject/scenes/headphones.mb"')
        cmd.select('pCube{}'.format(i+1))
        cmd.move(cmds.objectCenter(data_red[i])[0],cmds.objectCenter(data_red[i])[1],cmds.objectCenter(data_red[i])[2])
        cmd.scale(0.075,0.075,0.075)
        i += 1
    
    i = 0
        
    for model in model_list:
        for model_name in model:
            mel.eval('file -import -type "mayaBinary" -gr  -ignoreVersion -ra true -mergeNamespacesOnClash false -namespace "{}" -options "v=0;"  -pr  -importTimeRange "combine" "F:/Major Project 2/MayaFiles/MajorProject/scenes/{}.mb"'.format(model_name,model_name))
            if not i:
                cmd.select('group')
            else:
                cmd.select('group{}'.format(i))
            cmd.move(cmds.objectCenter(data_red[i])[0],cmds.objectCenter(data_red[i])[1],cmds.objectCenter(data_red[i])[2])
            cmd.scale(0.05,0.05,0.05)
    
            mel.eval('CreatePolygonType')
            mel.eval('setAttr "type{}.fontSize" 0.1'.format(i+1))
            mel.eval('setAttr "typeExtrude{}.extrudeDistance" 0.01'.format(i+1))
            mel.eval('setAttr "typeExtrude{}.extrudeDivisions" 1'.format(i+1))
            mel.eval('setAttr -type "string" "type{}.textInput" "{}"'.format(i+1,textToSpacedHex(model[model_name])))
    
            mel.eval("CenterPivot")
            mel.eval("move -rpr 0 0 0")
            mel.eval("FreezeTransformations")
    
            cmd.move(cmds.objectCenter(data_red[i])[0],cmds.objectCenter(data_red[i])[1]+0.2,cmds.objectCenter(data_red[i])[2])
    
            print(len(data_red))
            print(i)
            i += 1


surface_colour = 0
first_colour = 0
first_colour_rgb = ()
ramp_count = 1
    
def calculate_node_colour(colour_list,index,node_name):
    total_weight_list = []
    colourweight_pos = []
    global surface_colour, first_colour_rgb, ramp_count
    R = 0
    Y = 60
    G = 120
    B = 240
    
    def colour_type(cw):
        if cw[0] == 'R':
            return R
        elif cw[0] == 'Y':
            return Y
        elif cw[0] == 'G':
            return G
        elif cw[0] == 'B':
            return B
    
    def colour_algo(colourweight):
        global first_colour
        colourweight.sort(key=lambda x: x[1], reverse=True)
        print(colourweight)
        max_weight = colourweight[0][1] / float(len(data_red))
        max_weight_raw = colourweight[0][1]
        print(max_weight)
        C1 = colour_type(colourweight[0])
        first_colour = C1
        
        #for colour in colourweight:
            #if max_weight_raw - colour[1] == 0:
                #first_colour = (first_colour + colour_type(colour[0])) / 2
    
        for indx, colour in enumerate(colourweight):
            if indx < len(colourweight) - 1:
                C2 = colour_type(colourweight[indx+1])
                W2 = colourweight[indx+1][1]
                print(W2)
    
                G180 = abs(C1-C2) > 180
                AVG = (C1+C2) / 2
                print(AVG)
                if G180:
                    if AVG > 180:
                        AVG = AVG - 180
                    else:
                        AVG = AVG + 180
                print(AVG)
                INT = (AVG - C2) / len(data_red)
                print(INT)
                CN = C1 - (INT * W2)
                if CN > 360:
                    CN = CN - 360
                elif CN < 0:
                    CN = CN + 360
                print(CN)
                C1 = CN
        
        print("FIRST COL",first_colour)
        print(C1)
        if first_colour - C1 <= 30 and first_colour - C1 >= -30:
            return (0,0,0)
        return colorsys.hsv_to_rgb(C1/360.,max_weight,1)
        
    def colour_algo_second(colourweight):
        colourweight.sort(key=lambda x: x[1], reverse=True)
        print(colourweight)
        for colour in colourweight:
            colourweight_pos.append(colour[0])
        #colourweight_list = colourweight
        
        for indx, colour in enumerate(colourweight):
            if indx == 0:
                total_weight_list.append(colour[1])
            total_weight_list.append(colour[1])
        
        print(total_weight_list)
        print(sum(total_weight_list))
        
        #for indx, colour in enumerate(colourweight):
            #if indx == 0:
        
        return colourweight 
        
        
    print(colour_list[0].index(colour_list[1][index]))
    
    rgb_values_for_node = colour_algo_second([
        ('R', len(colour_list[0]) - colour_list[0].index(node_name)),
        ('Y', len(colour_list[1]) - colour_list[1].index(node_name)),
        ('G', len(colour_list[2]) - colour_list[2].index(node_name)),
        ('B', len(colour_list[3]) - colour_list[3].index(node_name))
    ])
    
    mel.eval('shadingNode -asShader standardSurface')
    mel.eval('sets -renderable true -noSurfaceShader true -empty -name standardSurface{}SG'.format(index+1))
    mel.eval('connectAttr -f standardSurface{}.outColor standardSurface{}SG.surfaceShader'.format(index+1,index+1))
    mel.eval('setAttr "standardSurface{}.specular" 0'.format(index+1))
    cmd.select(data_red[index])
    mel.eval('sets -e -forceElement standardSurface{}SG'.format(index+1))
    #mel.eval('setAttr "standardSurface{}.baseColor" -type double3 {} {} {}'.format(index+2,rgb_values_for_node[0],rgb_values_for_node[1],rgb_values_for_node[2]))
    
    mel.eval('shadingNode -asUtility blendColors')
    
    mel.eval('shadingNode -asTexture ramp')
    mel.eval('shadingNode -asUtility place2dTexture')
    mel.eval('setAttr "place2dTexture{}.repeatU" 2'.format(ramp_count))
    mel.eval('connectAttr place2dTexture{}.outUV ramp{}.uv'.format(ramp_count,ramp_count))
    mel.eval('connectAttr place2dTexture{}.outUvFilterSize ramp{}.uvFilterSize'.format(ramp_count,ramp_count))
    mel.eval('connectAttr -f ramp{}.outColor blendColors{}.color1'.format(ramp_count,index+1))
    mel.eval('connectAttr -f blendColors{}.output standardSurface{}.baseColor'.format(index+1,index+1))
    
    mel.eval('connectAttr -f floatConstant1.outFloat blendColors{}.blender'.format(ramp_count))
    
    position_for_ramp = 0
    
    for indx, value in enumerate(total_weight_list):
        print(position_for_ramp)
        print(value)
        if indx == 0:
            position_for_ramp = position_for_ramp + value
            continue
        position_total = position_for_ramp / float(sum(total_weight_list))
        print("POS",position_total)
        print("T",position_for_ramp / sum(total_weight_list))
        pos_col_weight = value / float(len(data_red))
        position_colour = colorsys.hsv_to_rgb(colour_type(rgb_values_for_node[indx-1])/360.,pos_col_weight,1)
        mel.eval('setAttr ramp{}.colorEntryList[{}].color {} {} {}'.format(ramp_count,indx-1,position_colour[0],position_colour[1],position_colour[2]))
        mel.eval('setAttr ramp{}.colorEntryList[{}].position {}'.format(ramp_count,indx-1,position_total))
        mel.eval('setAttr "ramp{}.interpolation" 4'.format(ramp_count))
        mel.eval('setAttr "ramp{}.noise" 0.5'.format(ramp_count))
        position_for_ramp = position_for_ramp + value
        
    cmds.expression(s="if (frame >= 500 && frame < 900) {\n\tblendColors%s.color2R = ramp%s.colorEntryList[%s].colorR;\n\tblendColors%s.color2G = ramp%s.colorEntryList[%s].colorG;\n\tblendColors%s.color2B = ramp%s.colorEntryList[%s].colorB;\n} else if (frame >= 4890 && frame < 5327) {\n\tblendColors%s.color2R = ramp%s.colorEntryList[%s].colorR;\n\tblendColors%s.color2G = ramp%s.colorEntryList[%s].colorG;\n\tblendColors%s.color2B = ramp%s.colorEntryList[%s].colorB;\n} else if (frame >= 9306 && frame < 9761) {\n\tblendColors%s.color2R = ramp%s.colorEntryList[%s].colorR;\n\tblendColors%s.color2G = ramp%s.colorEntryList[%s].colorG;\n\tblendColors%s.color2B = ramp%s.colorEntryList[%s].colorB;\n} else if (frame >= 13728 && frame < 14135) {\n\tblendColors%s.color2R = ramp%s.colorEntryList[%s].colorR;\n\tblendColors%s.color2G = ramp%s.colorEntryList[%s].colorG;\n\tblendColors%s.color2B = ramp%s.colorEntryList[%s].colorB;\n}" % (ramp_count,ramp_count,colourweight_pos.index('R'),ramp_count,ramp_count,colourweight_pos.index('R'),ramp_count,ramp_count,colourweight_pos.index('R'),ramp_count,ramp_count,colourweight_pos.index('Y'),ramp_count,ramp_count,colourweight_pos.index('Y'),ramp_count,ramp_count,colourweight_pos.index('Y'),ramp_count,ramp_count,colourweight_pos.index('G'),ramp_count,ramp_count,colourweight_pos.index('G'),ramp_count,ramp_count,colourweight_pos.index('G'),ramp_count,ramp_count,colourweight_pos.index('B'),ramp_count,ramp_count,colourweight_pos.index('B'),ramp_count,ramp_count,colourweight_pos.index('B')))
    
    '''first_colour_rgb = colorsys.hsv_to_rgb(first_colour/360.,1,1)
    print("F",first_colour)
    print("RBG",first_colour_rgb)
    
    mel.eval('setAttr "standardSurface{}.sheen" 1'.format(index+2))
    mel.eval('setAttr "standardSurface{}.sheenColor" -type double3 {} {} {}'.format(index+2,first_colour_rgb[0],first_colour_rgb[1],first_colour_rgb[2]))
    mel.eval('setAttr "standardSurface{}.sheenRoughness" 1'.format(index+2))
    mel.eval('setAttr "standardSurface{}.emission" 0.025'.format(index+2))
    mel.eval('setAttr "standardSurface{}.emissionColor" -type double3 {} {} {}'.format(index+2,first_colour_rgb[0],first_colour_rgb[1],first_colour_rgb[2]))'''
    
    surface_colour = index+1
    ramp_count += 1
    
    print(rgb_values_for_node)
    
def connectNodes(nodeList):
    global j
    bottomFace = 0
    topFace = 740
    while j < len(nodeList) - 1:
        print(nodeList[j])
        cmd.select('nodesCombined.f[{}]'.format(bottomFace), 'nodesCombined.f[{}]'.format(topFace))
        mel.eval('polyBridgeFaces')
        mel.eval('setAttr "polyBridgeEdge{}.curveType" 1'.format(j+1))
        mel.eval('setAttr "polyBridgeEdge{}.divisions" 20'.format(j+1))
        mel.eval('setAttr "polyBridgeEdge{}.targetDirection" 0'.format(j+1))
        mel.eval('setAttr "polyBridgeEdge{}.sourceDirection" 0'.format(j+1))
        mel.eval('setAttr "polyBridgeEdge{}.taper" 2'.format(j+1))
        #mel.eval('setAttr "polyBridgeEdge{}.twist" 2'.format(j+1))
        cmd.polySplitEdge()
        if j == 0:
            bottomFace = bottomFace + 399
        else:
            bottomFace = bottomFace + 398
        topFace = topFace + 398
        j = j + 1

def algo(data_red, sets):
    for colour_set in sets:
        print("Next")
        for indx, data_point in enumerate(colour_set):
            if indx != len(colour_set) - 1:
                if list_range(data_red,data_point,colour_set,indx):
                    print("Works")
                    #continue
                elif connection_history(new_connections_2,data_point,colour_set,indx):
                    print("Already Connected")
                    #continue
                else:
                    new_connections.append([data_point,colour_set[indx+1]])
                    new_connections_2.append([data_point,colour_set[indx+1]])
                    print(new_connections)
    print(new_connections)

node_connection_x = 0
break_num = 0

def create_connection(nodes_to_connect,data_red):
    global j, node_connection_x, break_num
    while node_connection_x < len(nodes_to_connect):
    #for the_nodes_to_connect in nodes_to_connect:
        the_nodes_to_connect = nodes_to_connect[node_connection_x]
        FirstFaceDone = False
        for idx in enumerate(the_nodes_to_connect):
            if not data_red.index(the_nodes_to_connect[idx[0]]):
                MinFace = 0
                MaxFace = 358
            else:
                node_to_num = int(data_red.index(the_nodes_to_connect[idx[0]]))
                #print(399 + ((node_to_num-1) * 398))
                MinFace = 399 + ((node_to_num-1) * 398)
                MaxFace = 358 + ((data_red.index(the_nodes_to_connect[idx[0]]) * 398))
            if not FirstFaceDone:
                FirstFace = rand.randint(MinFace,MaxFace)
                FirstFaceDone = True
            else:
                SecondFace = rand.randint(MinFace,MaxFace)
                FirstFaceDone = False
            print("MIN AND MAX FACE:",MinFace,MaxFace)
        print("FIR AND SEC FACE:",FirstFace,SecondFace)
        cmd.select('nodesCombined.f[{}]'.format(FirstFace), 'nodesCombined.f[{}]'.format(SecondFace))
        try:
            mel.eval('polyBridgeFaces')
        except:
            print('H')
        print("COUNTER:",j)
        try:
            mel.eval('setAttr "polyBridgeEdge{}.curveType" 1'.format(j+1))
        except:
            mel.eval('undo')
            break_num += 1
            if break_num > 100:
                break
            continue
        mel.eval('setAttr "polyBridgeEdge{}.divisions" 20'.format(j+1))
        mel.eval('setAttr "polyBridgeEdge{}.targetDirection" 0'.format(j+1))
        mel.eval('setAttr "polyBridgeEdge{}.sourceDirection" 0'.format(j+1))
        mel.eval('setAttr "polyBridgeEdge{}.taper" 2'.format(j+1))
        #mel.eval('setAttr "polyBridgeEdge{}.twist" 2'.format(j+1))
        cmd.polySplitEdge()
        j = j + 1
        node_connection_x += 1

def connection_history(new_connections_temp,data_point,colour_set,indx):
    #new_connections_temp = list(new_connections)
    #print(id(new_connections_temp),id(new_connections))
    for connections in new_connections_temp:
        print("INPUT:",connections)
        connections.sort()
        print("INPUTSORT1:",connections)
        print([data_point,colour_set[indx+1]])
        if connections == [data_point,colour_set[indx+1]]:
            return True
        connections.sort(reverse=True)
        print("INPUTSORT2:",connections)
        if connections == [data_point,colour_set[indx+1]]:
            return True
    return False

def list_range(data_b,data_p,colour_set,indx):
    if not data_b.index(data_p):
        return colour_set[indx+1] == data_red[data_red.index(data_p) + 1]
    elif data_b.index(data_p) == len(data_b) - 1:
        return colour_set[indx+1] == data_red[data_red.index(data_p) - 1]
    else:
        return colour_set[indx+1] == data_red[data_red.index(data_p) + 1] or colour_set[indx+1] == data_red[data_red.index(data_p) - 1]

line_count = 0

def fibonacci_sphere(samples):

    points = []
    phi = math.pi * (3. - math.sqrt(5.))  # golden angle in radians

    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2  # y goes from 1 to -1
        radius = math.sqrt(1 - y * y)  # radius at y

        theta = phi * i  # golden angle increment

        x = math.cos(theta) * radius
        z = math.sin(theta) * radius
        
        random_disperse = rand.uniform(20,40)

        points.append((x*random_disperse,y*random_disperse,z*random_disperse))
    
    rand.shuffle(points)
    return points
    
all_data_sequence = []

def read_csv_data(lc):
    with open('F:\\Major Project 2\\dataset_main.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not lc:
                lc =+ 1
                continue
            data_red.extend(row[0])
            data_yellow.extend(row[1])
            data_green.extend(row[2])
            data_blue.extend(row[3])

    all_data_sequence.extend(data_red)        
    all_data_sequence.extend(data_yellow)
    all_data_sequence.extend(data_green)
    all_data_sequence.extend(data_blue)

k = 1

bridge_list = []

def renaming():
    global k
    for indx, node in enumerate(data_red):
        cmd.rename('polySurface{}'.format(k),node)
        k += 1
    for indx, node in enumerate(data_red):
        if indx != len(data_red) - 1:
            cmd.rename('polySurface{}'.format(k),node + "to" + data_red[indx+1])
            bridge_list.append(node + "to" + data_red[indx+1])
            k += 1
    for bridges in new_connections:
        cmd.rename('polySurface{}'.format(k),bridges[0] + "to" + bridges[1])
        bridge_list.append(bridges[0] + "to" + bridges[1])
        k += 1
        
    print(bridge_list)

def fading_bridges():
    ramp_bridge = len(data_red) + 1
    global surface_colour, ramp_count
    for bridge in bridge_list:
        cmd.select(bridge)
        cmd.polyMapSew()
        mel.eval('texNormalProjection 0 1 "" ')
        cmd.select('{}.e[0:7]'.format(bridge))
        mel.eval('texStraightenShell')
        cmd.select(bridge)
        mel.eval('texLinearAlignUVs')
        cmd.polyNormalizeUV(pa=False)
        
        print("SURFACE", surface_colour)
        
        mel.eval('shadingNode -asShader standardSurface')
        mel.eval('sets -renderable true -noSurfaceShader true -empty -name standardSurface{}SG'.format(surface_colour+1))
        mel.eval('connectAttr -f standardSurface{}.outColor standardSurface{}SG.surfaceShader'.format(surface_colour+1,surface_colour+1))
        cmd.select(bridge)
        mel.eval('setAttr "standardSurface{}.specular" 0'.format(surface_colour+1))
        mel.eval('sets -e -forceElement standardSurface{}SG'.format(surface_colour+1))
        
        mel.eval('shadingNode -asTexture ramp')
        mel.eval('shadingNode -asUtility place2dTexture')
        mel.eval('connectAttr place2dTexture{}.outUV ramp{}.uv'.format(ramp_count,ramp_count))
        mel.eval('connectAttr place2dTexture{}.outUvFilterSize ramp{}.uvFilterSize'.format(ramp_count,ramp_count))
        mel.eval('connectAttr -f ramp{}.outColor standardSurface{}.baseColor'.format(ramp_count,surface_colour+1))
        
        RED1 = cmd.getAttr('standardSurface{}.baseColor'.format(data_red.index(bridge[0])+2))[0][0]
        GREEN1 = cmd.getAttr('standardSurface{}.baseColor'.format(data_red.index(bridge[0])+2))[0][1]
        BLUE1 = cmd.getAttr('standardSurface{}.baseColor'.format(data_red.index(bridge[0])+2))[0][2]
        
        NODE_MIX_1 = data_red.index(bridge[0])+1

        RED2 = cmd.getAttr('standardSurface{}.baseColor'.format(data_red.index(bridge[3])+2))[0][0]
        GREEN2 = cmd.getAttr('standardSurface{}.baseColor'.format(data_red.index(bridge[3])+2))[0][1]
        BLUE2 = cmd.getAttr('standardSurface{}.baseColor'.format(data_red.index(bridge[3])+2))[0][2]
        
        NODE_MIX_2 = data_red.index(bridge[3])+1
        
        #print(RED,GREEN,BLUE)
        
        cmd.select('{}.e[0:3]'.format(bridge))
        mel.eval('MoveTool')
        if data_red.index(bridge[0]) > data_red.index(bridge[3]):
            print('IF:','{}'.format(bridge),cmd.getAttr('{}Shape.uvPivot'.format(bridge)))
            if cmd.getAttr('{}Shape.uvPivot'.format(bridge))[0][1] < 0.5:
                #mel.eval('setAttr ramp{}.colorEntryList[0].color {} {} {}'.format(ramp_count,RED2,GREEN2,BLUE2))
                #mel.eval('setAttr ramp{}.colorEntryList[1].color {} {} {}'.format(ramp_count,RED1,GREEN1,BLUE1))
                mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[0].color'.format(NODE_MIX_2,ramp_count))
                mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[1].color'.format(NODE_MIX_1,ramp_count))
                mel.eval('setAttr ramp{}.colorEntryList[0].position 0.25'.format(ramp_bridge))
                mel.eval('setAttr ramp{}.colorEntryList[1].position 0.75'.format(ramp_bridge))
            else:
                #mel.eval('setAttr ramp{}.colorEntryList[0].color {} {} {}'.format(ramp_count,RED1,GREEN1,BLUE1))
                #mel.eval('setAttr ramp{}.colorEntryList[1].color {} {} {}'.format(ramp_count,RED2,GREEN2,BLUE2))
                mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[0].color'.format(NODE_MIX_1,ramp_count))
                mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[1].color'.format(NODE_MIX_2,ramp_count))
                mel.eval('setAttr ramp{}.colorEntryList[0].position 0.25'.format(ramp_bridge))
                mel.eval('setAttr ramp{}.colorEntryList[1].position 0.75'.format(ramp_bridge))
        elif not cmd.getAttr('{}Shape.uvPivot'.format(bridge))[0][1] < 0.5:
            print('ELIF1:','{}'.format(bridge),cmd.getAttr('{}Shape.uvPivot'.format(bridge)))
            cmd.select('{}.f[0:83]'.format(bridge))
            mel.eval('polyRotateUVs 180 0')
            #mel.eval('setAttr ramp{}.colorEntryList[0].color {} {} {}'.format(ramp_count,RED1,GREEN1,BLUE1))
            #mel.eval('setAttr ramp{}.colorEntryList[1].color {} {} {}'.format(ramp_count,RED2,GREEN2,BLUE2))
            mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[0].color'.format(NODE_MIX_1,ramp_count))
            mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[1].color'.format(NODE_MIX_2,ramp_count))
            mel.eval('setAttr ramp{}.colorEntryList[0].position 0.25'.format(ramp_bridge))
            mel.eval('setAttr ramp{}.colorEntryList[1].position 0.75'.format(ramp_bridge))
        elif cmd.getAttr('{}Shape.uvPivot'.format(bridge))[0][1] < 0.5 and data_red.index(bridge[0]) > data_red.index(bridge[3]):
            print('ELIF2','{}'.format(bridge),cmd.getAttr('{}Shape.uvPivot'.format(bridge)))
            #cmd.select('{}.f[0:83]'.format(bridge))
            #mel.eval('polyRotateUVs 180 0')
            #mel.eval('setAttr ramp{}.colorEntryList[0].color {} {} {}'.format(ramp_count,RED2,GREEN2,BLUE2))
            #mel.eval('setAttr ramp{}.colorEntryList[1].color {} {} {}'.format(ramp_count,RED1,GREEN1,BLUE1))
            mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[0].color'.format(NODE_MIX_2,ramp_count))
            mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[1].color'.format(NODE_MIX_1,ramp_count))
            mel.eval('setAttr ramp{}.colorEntryList[0].position 0.75'.format(ramp_bridge))
            mel.eval('setAttr ramp{}.colorEntryList[1].position 0.25'.format(ramp_bridge))
        else:
            print('ELSE','{}'.format(bridge),cmd.getAttr('{}Shape.uvPivot'.format(bridge)))
            #mel.eval('setAttr ramp{}.colorEntryList[0].color {} {} {}'.format(ramp_count,RED1,GREEN1,BLUE1))
            #mel.eval('setAttr ramp{}.colorEntryList[1].color {} {} {}'.format(ramp_count,RED2,GREEN2,BLUE2))
            mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[0].color'.format(NODE_MIX_1,ramp_count))
            mel.eval('connectAttr -f standardSurface{}.baseColor ramp{}.colorEntryList[1].color'.format(NODE_MIX_2,ramp_count))
            mel.eval('setAttr ramp{}.colorEntryList[0].position 0.25'.format(ramp_bridge))
            mel.eval('setAttr ramp{}.colorEntryList[1].position 0.75'.format(ramp_bridge))
       
        surface_colour += 1
        ramp_count += 1
        ramp_bridge += 1

bridge_points = {}

def camera_flythrough_generate():
    XCor = []
    YCor = []
    ZCor = []
    MidPoints = []
    EndMidPoint = []
    FaceList = []
    
    def MidPointCalculate(XCor,YCor,ZCor):
        xavg = 0
        yavg = 0
        zavg = 0
        for xc in XCor:
            xavg += xc
        xavg = xavg / 4
        del XCor[:]
        for yc in YCor:
            yavg += yc
        yavg = yavg / 4
        del YCor[:]
        for zc in ZCor:
            zavg += zc
        zavg = zavg / 4
        del ZCor[:]
        #cmds.spaceLocator(p=(xavg,yavg,zavg))
        return [xavg,yavg,zavg]
    

    for bridge in bridge_list:
        Face = 0    
        for i in range(20):
            if not i:
                for i2 in range(4): 
                    face = pm.MeshFace("{}.f[{}]".format(bridge,Face))
                    Face += 1
                    pt = face.__apimfn__().center(OpenMaya.MSpace.kWorld)
                    XCor.append(pm.datatypes.Point(pt)[0])
                    YCor.append(pm.datatypes.Point(pt)[1])
                    ZCor.append(pm.datatypes.Point(pt)[2])
                EndMidPoint.append((MidPointCalculate(XCor,YCor,ZCor)))
                #EndMidPoint.append('END')
            for i2 in range(4):   
                face = pm.MeshFace("{}.f[{}]".format(bridge,Face))
                Face += 1
                pt = face.__apimfn__().center(OpenMaya.MSpace.kWorld)
                XCor.append(pm.datatypes.Point(pt)[0])
                YCor.append(pm.datatypes.Point(pt)[1])
                ZCor.append(pm.datatypes.Point(pt)[2])
                #print(centerPointCoordinates)
            #FaceList.append(centerPointCoordinates)
            #print(XCor)
            #print(YCor)
            #print(ZCor)
            MidPoints.append(MidPointCalculate(XCor,YCor,ZCor))
            #MidPoints.append('POINT')
            if i == 19:
                MidPoints.extend(EndMidPoint)
                temp = list(MidPoints)
                bridge_points['{}'.format(bridge)] = temp
                del EndMidPoint[:]
                del MidPoints[:]
            #print(MidPoints)
    #print(bridge_points['AtoB'])
    #print(bridge_points['GtoB'])    
    WholeCurvePointsRed = []
    WholeCurvePointsYellow = []
    WholeCurvePointsGreen = []
    WholeCurvePointsBlue = []
    for indx in enumerate(data_red):
        if indx[0] < len(data_red) - 1:
            getNodePosFirst = cmds.objectCenter(data_red[indx[0]])
            getNodePosSecond = cmds.objectCenter(data_red[indx[0]+1])
            totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_red[indx[0]],data_red[indx[0]+1])][0])]
            totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_red[indx[0]],data_red[indx[0]+1])][20])]
           # print(total)
            #print(bridge_points['{}to{}'.format(data_red[indx[0]],data_red[indx[0]+1])][0])
            NextStartingPosFirst = [number / 2 for number in totalFirst]
            NextStartingPosSecond = [number / 2 for number in totalSecond]
            WholeCurvePointsRed.append(getNodePosFirst)
            WholeCurvePointsRed.append(NextStartingPosFirst)
            WholeCurvePointsRed.extend(bridge_points['{}to{}'.format(data_red[indx[0]],data_red[indx[0]+1])])
            WholeCurvePointsRed.append(NextStartingPosSecond)
            WholeCurvePointsRed.append(getNodePosSecond)
    for indx in enumerate(data_yellow):
        if indx[0] < len(data_yellow) - 1:
            #if data_blue.index(data_yellow[indx[0]]) > data_blue.index(data_yellow[indx[0]+1]):
            #    getNodePosFirst = cmds.objectCenter(data_yellow[indx[0]+1])
            #    getNodePosSecond = cmds.objectCenter(data_yellow[indx[0]])
            getNodePosFirst = cmds.objectCenter(data_yellow[indx[0]])
            getNodePosSecond = cmds.objectCenter(data_yellow[indx[0]+1])
            WholeCurvePointsYellow.append(getNodePosFirst)
            print(data_yellow[indx[0]])
            print(data_yellow[indx[0]+1])
            try:
                if data_red.index(data_yellow[indx[0]]) > data_red.index(data_yellow[indx[0]+1]):
                    print("a")
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_yellow[indx[0]],data_yellow[indx[0]+1])][20])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_yellow[indx[0]],data_yellow[indx[0]+1])][0])]
                    NextStartingPosFirst = [number / 2 for number in totalFirst]
                    NextStartingPosSecond = [number / 2 for number in totalSecond]
                    WholeCurvePointsYellow.append(NextStartingPosFirst)
                    temp = list(bridge_points['{}to{}'.format(data_yellow[indx[0]],data_yellow[indx[0]+1])])
                    temp.reverse()
                    WholeCurvePointsYellow.extend(temp)
                else:
                    print("b")
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_yellow[indx[0]],data_yellow[indx[0]+1])][0])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_yellow[indx[0]],data_yellow[indx[0]+1])][20])]
                    NextStartingPosFirst = [number / 2 for number in totalFirst]
                    NextStartingPosSecond = [number / 2 for number in totalSecond]
                    WholeCurvePointsYellow.append(NextStartingPosFirst)
                    WholeCurvePointsYellow.extend(bridge_points['{}to{}'.format(data_yellow[indx[0]],data_yellow[indx[0]+1])])
            except:
                print("c")
                if data_red.index(data_yellow[indx[0]+1]) > data_red.index(data_yellow[indx[0]]):
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_yellow[indx[0]+1],data_yellow[indx[0]])][0])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_yellow[indx[0]+1],data_yellow[indx[0]])][20])]
                else:
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_yellow[indx[0]+1],data_yellow[indx[0]])][20])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_yellow[indx[0]+1],data_yellow[indx[0]])][0])]
                NextStartingPosFirst = [number / 2 for number in totalFirst]
                NextStartingPosSecond = [number / 2 for number in totalSecond]
                WholeCurvePointsYellow.append(NextStartingPosFirst)
                temp = list(bridge_points['{}to{}'.format(data_yellow[indx[0]+1],data_yellow[indx[0]])])
                if data_red.index(data_yellow[indx[0]]) > data_red.index(data_yellow[indx[0]+1]):
                    print("d")
                    temp.reverse()
                WholeCurvePointsYellow.extend(temp)
            WholeCurvePointsYellow.append(NextStartingPosSecond)
            WholeCurvePointsYellow.append(getNodePosSecond)
    for indx in enumerate(data_green):
        if indx[0] < len(data_green) - 1:
            #if data_red.index(data_green[indx[0]]) > data_red.index(data_green[indx[0]+1]):
            #    getNodePosFirst = cmds.objectCenter(data_green[indx[0]+1])
            #    getNodePosSecond = cmds.objectCenter(data_green[indx[0]])
            getNodePosFirst = cmds.objectCenter(data_green[indx[0]])
            getNodePosSecond = cmds.objectCenter(data_green[indx[0]+1])
            WholeCurvePointsGreen.append(getNodePosFirst)
            print(data_green[indx[0]])
            print(data_green[indx[0]+1])
            try:
                if data_red.index(data_green[indx[0]]) > data_red.index(data_green[indx[0]+1]):
                    print("a")
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_green[indx[0]],data_green[indx[0]+1])][20])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_green[indx[0]],data_green[indx[0]+1])][0])]
                    NextStartingPosFirst = [number / 2 for number in totalFirst]
                    NextStartingPosSecond = [number / 2 for number in totalSecond]
                    WholeCurvePointsGreen.append(NextStartingPosFirst)
                    temp = list(bridge_points['{}to{}'.format(data_green[indx[0]],data_green[indx[0]+1])])
                    temp.reverse()
                    WholeCurvePointsGreen.extend(temp)
                else:
                    print("b")
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_green[indx[0]],data_green[indx[0]+1])][0])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_green[indx[0]],data_green[indx[0]+1])][20])]
                    NextStartingPosFirst = [number / 2 for number in totalFirst]
                    NextStartingPosSecond = [number / 2 for number in totalSecond]
                    WholeCurvePointsGreen.append(NextStartingPosFirst)
                    WholeCurvePointsGreen.extend(bridge_points['{}to{}'.format(data_green[indx[0]],data_green[indx[0]+1])])
            except:
                print("c")
                if data_red.index(data_green[indx[0]+1]) > data_red.index(data_green[indx[0]]):
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_green[indx[0]+1],data_green[indx[0]])][0])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_green[indx[0]+1],data_green[indx[0]])][20])]
                else:                    
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_green[indx[0]+1],data_green[indx[0]])][20])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_green[indx[0]+1],data_green[indx[0]])][0])]
                NextStartingPosFirst = [number / 2 for number in totalFirst]
                NextStartingPosSecond = [number / 2 for number in totalSecond]
                WholeCurvePointsGreen.append(NextStartingPosFirst)
                temp = list(bridge_points['{}to{}'.format(data_green[indx[0]+1],data_green[indx[0]])])
                if data_red.index(data_green[indx[0]]) > data_red.index(data_green[indx[0]+1]):
                    print("d")
                    temp.reverse()
                WholeCurvePointsGreen.extend(temp)
            WholeCurvePointsGreen.append(NextStartingPosSecond) 
            WholeCurvePointsGreen.append(getNodePosSecond)
    for indx in enumerate(data_blue):
        if indx[0] < len(data_blue) - 1:
            #if data_red.index(data_red[indx[0]]) > data_red.index(data_red[indx[0]+1]):
            #    getNodePosFirst = cmds.objectCenter(data_red[indx[0]+1])
            #    getNodePosSecond = cmds.objectCenter(data_red[indx[0]])
            getNodePosFirst = cmds.objectCenter(data_blue[indx[0]])
            getNodePosSecond = cmds.objectCenter(data_blue[indx[0]+1])
            WholeCurvePointsBlue.append(getNodePosFirst)
            print(data_blue[indx[0]])
            print(data_blue[indx[0]+1])
            try:
                if data_red.index(data_blue[indx[0]]) > data_red.index(data_blue[indx[0]+1]):
                    print("a")
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_blue[indx[0]],data_blue[indx[0]+1])][20])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_blue[indx[0]],data_blue[indx[0]+1])][0])]
                    NextStartingPosFirst = [number / 2 for number in totalFirst]
                    NextStartingPosSecond = [number / 2 for number in totalSecond]
                    WholeCurvePointsBlue.append(NextStartingPosFirst)
                    temp = list(bridge_points['{}to{}'.format(data_blue[indx[0]],data_blue[indx[0]+1])])
                    temp.reverse()
                    WholeCurvePointsBlue.extend(temp)
                else:
                    print("b")
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_blue[indx[0]],data_blue[indx[0]+1])][0])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_blue[indx[0]],data_blue[indx[0]+1])][20])]
                    NextStartingPosFirst = [number / 2 for number in totalFirst]
                    NextStartingPosSecond = [number / 2 for number in totalSecond]
                    WholeCurvePointsBlue.append(NextStartingPosFirst)
                    WholeCurvePointsBlue.extend(bridge_points['{}to{}'.format(data_blue[indx[0]],data_blue[indx[0]+1])])
            except:
                print("c")
                if data_red.index(data_blue[indx[0]+1]) > data_red.index(data_blue[indx[0]]):
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_blue[indx[0]+1],data_blue[indx[0]])][0])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_blue[indx[0]+1],data_blue[indx[0]])][20])]
                else:
                    totalFirst = [x + y for x, y in zip(getNodePosFirst, bridge_points['{}to{}'.format(data_blue[indx[0]+1],data_blue[indx[0]])][20])]
                    totalSecond = [x + y for x, y in zip(getNodePosSecond, bridge_points['{}to{}'.format(data_blue[indx[0]+1],data_blue[indx[0]])][0])]
                NextStartingPosFirst = [number / 2 for number in totalFirst]
                NextStartingPosSecond = [number / 2 for number in totalSecond]
                WholeCurvePointsBlue.append(NextStartingPosFirst)
                temp = list(bridge_points['{}to{}'.format(data_blue[indx[0]+1],data_blue[indx[0]])])
                if data_red.index(data_blue[indx[0]]) > data_red.index(data_blue[indx[0]+1]):
                    print("d")
                    temp.reverse()
                WholeCurvePointsBlue.extend(temp)
            WholeCurvePointsBlue.append(NextStartingPosSecond)
            WholeCurvePointsBlue.append(getNodePosSecond)
        
    print(len(WholeCurvePointsRed))
    print(len(WholeCurvePointsYellow))
    print(len(WholeCurvePointsGreen))
    print(len(WholeCurvePointsBlue))
    cmds.camera()
    mel.eval('cameraMakeNode 2 ""')
    keyframe_time_camera = 0
    keframe_time_aim = 0
    keyframe_colors = 0
    node_sequence = 0
    distance_cam = 700
    angle = 90
    is_first = True
    start_num = 23
    start_num_decrease = 0
    start_num_CONST = start_num
    node_center = cmds.objectCenter('nodesCombined')
    
    #for i in len(data_red):
    
    
    cmds.setKeyframe('camera1_aim',v=node_center[0],at='translateX',t=keframe_time_aim)
    cmds.setKeyframe('camera1_aim',v=node_center[1],at='translateY',t=keframe_time_aim)
    cmds.setKeyframe('camera1_aim',v=node_center[2],at='translateZ',t=keframe_time_aim)
    
    for revolutions in range(2):
        for number_of_points in range(15):
            pos_cam_x = (math.sin(math.radians((24*number_of_points))) + (node_center[0] / distance_cam)) * distance_cam
            pos_cam_z = (math.cos(math.radians((24*number_of_points))) + (node_center[2] / distance_cam)) * distance_cam
            if number_of_points == 0 and revolutions == 0:
                cmds.setKeyframe('camera1',v=pos_cam_x*50,at='translateX',t=keyframe_time_camera)
                cmds.setKeyframe('camera1',v=node_center[1]-20000,at='translateY',t=keyframe_time_camera)
                cmds.setKeyframe('camera1',v=pos_cam_z*50,at='translateZ',t=keyframe_time_camera)
                keyframe_time_camera += 30
                keframe_time_aim += 30
            cmds.setKeyframe('camera1',v=pos_cam_x,at='translateX',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=node_center[1],at='translateY',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=pos_cam_z,at='translateZ',t=keyframe_time_camera)
            if number_of_points == 0 and revolutions == 0:
                keyframe_time_camera += 80
                keframe_time_aim += 80
            else:
                keyframe_time_camera += 30
                keframe_time_aim += 30
      
            if revolutions == 1 and number_of_points == 0:
                cmds.setKeyframe('floatConstant1', v=1, at='inFloat', t=keyframe_time_camera)
                cmds.setKeyframe('floatConstant1', v=0, at='inFloat', t=keyframe_time_camera+10)
                cmds.setKeyframe('floatConstant1', v=0, at='inFloat', t=keyframe_time_camera+390)
                cmds.setKeyframe('floatConstant1', v=1, at='inFloat', t=keyframe_time_camera+400)
                    
    cmds.setKeyframe('camera1_aim',v=node_center[0],at='translateX',t=keframe_time_aim-30)
    cmds.setKeyframe('camera1_aim',v=node_center[1],at='translateY',t=keframe_time_aim-30)
    cmds.setKeyframe('camera1_aim',v=node_center[2],at='translateZ',t=keframe_time_aim-30)

    index_point = 0
    #data_point_index = 1

    for index, the_node in enumerate(data_red):
                if index < len(data_red) - 1:
                    for point in range(25):
                        if point == 0:
                            pos_of_node = cmds.objectCenter(the_node)
                            for number_of_points in range(6):
                                pos_node_x = math.sin(math.radians(angle + (36*number_of_points))) + pos_of_node[0]
                                pos_node_z = math.cos(math.radians(angle + (36*number_of_points))) + pos_of_node[2]
                                print(index_point)
                                #if index_point == 225:
                                #    index_point = 224
                                cmds.setKeyframe('camera1',v=pos_node_x,at='translateX',t=keyframe_time_camera)
                                cmds.setKeyframe('camera1',v=WholeCurvePointsRed[index_point][1],at='translateY',t=keyframe_time_camera)
                                cmds.setKeyframe('camera1',v=pos_node_z,at='translateZ',t=keyframe_time_camera)
                                
                                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsRed[index_point][0],at='translateX',t=keframe_time_aim)
                                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsRed[index_point][1],at='translateY',t=keframe_time_aim)
                                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsRed[index_point][2],at='translateZ',t=keframe_time_aim)
                                
                                keyframe_time_camera += 20
                                keframe_time_aim += 20
                            print("BEGIN",index_point)
                            index_point += 1
                            continue
                        elif point == 24:
                            #print(data_point_index)
                            print("END OF", index_point)
                            if len(WholeCurvePointsRed) - 1 == index_point:
                                print("END!")
                                pos_of_node = cmds.objectCenter(data_red[index+1])
                                for number_of_points in range(6):
                                    pos_node_x = math.sin(math.radians(angle + (36*number_of_points))) + pos_of_node[0]
                                    pos_node_z = math.cos(math.radians(angle + (36*number_of_points))) + pos_of_node[2]
                                    
                                    #print(WholeCurvePoints[index_point][1])
                                    
                                    cmds.setKeyframe('camera1',v=pos_node_x,at='translateX',t=keyframe_time_camera)
                                    cmds.setKeyframe('camera1',v=WholeCurvePointsRed[index_point][1],at='translateY',t=keyframe_time_camera)
                                    cmds.setKeyframe('camera1',v=pos_node_z,at='translateZ',t=keyframe_time_camera)
                                    
                                    #print(WholeCurvePoints[index_point][1])
                                    
                                    cmds.setKeyframe('camera1_aim',v=WholeCurvePointsRed[index_point][0],at='translateX',t=keframe_time_aim)
                                    cmds.setKeyframe('camera1_aim',v=WholeCurvePointsRed[index_point][1],at='translateY',t=keframe_time_aim)
                                    cmds.setKeyframe('camera1_aim',v=WholeCurvePointsRed[index_point][2],at='translateZ',t=keframe_time_aim)
                                    
                                    #print(WholeCurvePoints[index_point][1])
                                    
                                    keyframe_time_camera += 20
                                    keframe_time_aim += 20
                                break
                            index_point += 1
                            continue
                        #if index_point == 225 or index_point == 224:
                        #    index_point = 223
                        print(index_point)
                        print(the_node)
                        cmds.setKeyframe('camera1',v=WholeCurvePointsRed[index_point][0],at='translateX',t=keyframe_time_camera)
                        cmds.setKeyframe('camera1',v=WholeCurvePointsRed[index_point][1],at='translateY',t=keyframe_time_camera)
                        cmds.setKeyframe('camera1',v=WholeCurvePointsRed[index_point][2],at='translateZ',t=keyframe_time_camera)
                        
                        cmds.setKeyframe('camera1_aim',v=WholeCurvePointsRed[index_point+1][0],at='translateX',t=keframe_time_aim)
                        cmds.setKeyframe('camera1_aim',v=WholeCurvePointsRed[index_point+1][1],at='translateY',t=keframe_time_aim)
                        cmds.setKeyframe('camera1_aim',v=WholeCurvePointsRed[index_point+1][2],at='translateZ',t=keframe_time_aim)
                        keyframe_time_camera += 8
                        keframe_time_aim += 8
                        print("NORMAL",index_point)
                        index_point += 1   

            #data_point_index += 1
    cmds.setKeyframe('camera1_aim',v=node_center[0],at='translateX',t=keframe_time_aim)
    cmds.setKeyframe('camera1_aim',v=node_center[1],at='translateY',t=keframe_time_aim)
    cmds.setKeyframe('camera1_aim',v=node_center[2],at='translateZ',t=keframe_time_aim)
    
    for revolutions in range(2):
        for number_of_points in range(15):
            pos_cam_x = (math.sin(math.radians((24*number_of_points))) + (node_center[0] / distance_cam)) * distance_cam
            pos_cam_z = (math.cos(math.radians((24*number_of_points))) + (node_center[2] / distance_cam)) * distance_cam
            cmds.setKeyframe('camera1',v=pos_cam_x,at='translateX',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=node_center[1],at='translateY',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=pos_cam_z,at='translateZ',t=keyframe_time_camera)
            if number_of_points == 0 and revolutions == 0:
                keyframe_time_camera += 80
                keframe_time_aim += 80
            else:
                keyframe_time_camera += 30
                keframe_time_aim += 30

            if revolutions == 1 and number_of_points == 0:
                cmds.setKeyframe('floatConstant1', v=1, at='inFloat', t=keyframe_time_camera)
                cmds.setKeyframe('floatConstant1', v=0, at='inFloat', t=keyframe_time_camera+10)
                cmds.setKeyframe('floatConstant1', v=0, at='inFloat', t=keyframe_time_camera+390)
                cmds.setKeyframe('floatConstant1', v=1, at='inFloat', t=keyframe_time_camera+400)
            
    cmds.setKeyframe('camera1_aim',v=node_center[0],at='translateX',t=keframe_time_aim-30)
    cmds.setKeyframe('camera1_aim',v=node_center[1],at='translateY',t=keframe_time_aim-30)
    cmds.setKeyframe('camera1_aim',v=node_center[2],at='translateZ',t=keframe_time_aim-30)

    index_point = 0

    for index, the_node in enumerate(data_yellow):
            if index < len(data_yellow) - 1:
                for point in range(25):
                    if point == 0:
                        pos_of_node = cmds.objectCenter(the_node)
                        for number_of_points in range(6):
                            pos_node_x = math.sin(math.radians(angle + (36*number_of_points))) + pos_of_node[0]
                            pos_node_z = math.cos(math.radians(angle + (36*number_of_points))) + pos_of_node[2]
                            print(index_point)
                            #if index_point == 225:
                            #    index_point = 224
                            cmds.setKeyframe('camera1',v=pos_node_x,at='translateX',t=keyframe_time_camera)
                            cmds.setKeyframe('camera1',v=WholeCurvePointsYellow[index_point][1],at='translateY',t=keyframe_time_camera)
                            cmds.setKeyframe('camera1',v=pos_node_z,at='translateZ',t=keyframe_time_camera)
                            
                            cmds.setKeyframe('camera1_aim',v=WholeCurvePointsYellow[index_point][0],at='translateX',t=keframe_time_aim)
                            cmds.setKeyframe('camera1_aim',v=WholeCurvePointsYellow[index_point][1],at='translateY',t=keframe_time_aim)
                            cmds.setKeyframe('camera1_aim',v=WholeCurvePointsYellow[index_point][2],at='translateZ',t=keframe_time_aim)
                            
                            keyframe_time_camera += 20
                            keframe_time_aim += 20
                        print("BEGIN",index_point)
                        index_point += 1
                        continue
                    elif point == 24:
                        #print(data_point_index)
                        print("END OF", index_point)
                        if len(WholeCurvePointsYellow) - 1 == index_point:
                            print("END!")
                            pos_of_node = cmds.objectCenter(data_yellow[index+1])
                            for number_of_points in range(6):
                                pos_node_x = math.sin(math.radians(angle + (36*number_of_points))) + pos_of_node[0]
                                pos_node_z = math.cos(math.radians(angle + (36*number_of_points))) + pos_of_node[2]
                                
                                #print(WholeCurvePoints[index_point][1])
                                
                                cmds.setKeyframe('camera1',v=pos_node_x,at='translateX',t=keyframe_time_camera)
                                cmds.setKeyframe('camera1',v=WholeCurvePointsYellow[index_point][1],at='translateY',t=keyframe_time_camera)
                                cmds.setKeyframe('camera1',v=pos_node_z,at='translateZ',t=keyframe_time_camera)
                                
                                #print(WholeCurvePoints[index_point][1])
                                
                                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsYellow[index_point][0],at='translateX',t=keframe_time_aim)
                                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsYellow[index_point][1],at='translateY',t=keframe_time_aim)
                                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsYellow[index_point][2],at='translateZ',t=keframe_time_aim)
                                
                                #print(WholeCurvePoints[index_point][1])
                                
                                keyframe_time_camera += 20
                                keframe_time_aim += 20
                            break
                        index_point += 1
                        continue
                    #if index_point == 225 or index_point == 224:
                    #    index_point = 223
                    print(index_point)
                    print(the_node)
                    cmds.setKeyframe('camera1',v=WholeCurvePointsYellow[index_point][0],at='translateX',t=keyframe_time_camera)
                    cmds.setKeyframe('camera1',v=WholeCurvePointsYellow[index_point][1],at='translateY',t=keyframe_time_camera)
                    cmds.setKeyframe('camera1',v=WholeCurvePointsYellow[index_point][2],at='translateZ',t=keyframe_time_camera)
                    
                    cmds.setKeyframe('camera1_aim',v=WholeCurvePointsYellow[index_point+1][0],at='translateX',t=keframe_time_aim)
                    cmds.setKeyframe('camera1_aim',v=WholeCurvePointsYellow[index_point+1][1],at='translateY',t=keframe_time_aim)
                    cmds.setKeyframe('camera1_aim',v=WholeCurvePointsYellow[index_point+1][2],at='translateZ',t=keframe_time_aim)
                    keyframe_time_camera += 8
                    keframe_time_aim += 8
                    print("NORMAL",index_point)
                    index_point += 1
                
    cmds.setKeyframe('camera1_aim',v=node_center[0],at='translateX',t=keframe_time_aim)
    cmds.setKeyframe('camera1_aim',v=node_center[1],at='translateY',t=keframe_time_aim)
    cmds.setKeyframe('camera1_aim',v=node_center[2],at='translateZ',t=keframe_time_aim)
    
    for revolutions in range(2):
        for number_of_points in range(15):
            pos_cam_x = (math.sin(math.radians((24*number_of_points))) + (node_center[0] / distance_cam)) * distance_cam
            pos_cam_z = (math.cos(math.radians((24*number_of_points))) + (node_center[2] / distance_cam)) * distance_cam
            cmds.setKeyframe('camera1',v=pos_cam_x,at='translateX',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=node_center[1],at='translateY',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=pos_cam_z,at='translateZ',t=keyframe_time_camera)
            if number_of_points == 0 and revolutions == 0:
                keyframe_time_camera += 80
                keframe_time_aim += 80
            else:
                keyframe_time_camera += 30
                keframe_time_aim += 30
                
            if revolutions == 1 and number_of_points == 0:
                cmds.setKeyframe('floatConstant1', v=1, at='inFloat', t=keyframe_time_camera)
                cmds.setKeyframe('floatConstant1', v=0, at='inFloat', t=keyframe_time_camera+10)
                cmds.setKeyframe('floatConstant1', v=0, at='inFloat', t=keyframe_time_camera+390)
                cmds.setKeyframe('floatConstant1', v=1, at='inFloat', t=keyframe_time_camera+400)
            
    cmds.setKeyframe('camera1_aim',v=node_center[0],at='translateX',t=keframe_time_aim-30)
    cmds.setKeyframe('camera1_aim',v=node_center[1],at='translateY',t=keframe_time_aim-30)
    cmds.setKeyframe('camera1_aim',v=node_center[2],at='translateZ',t=keframe_time_aim-30)

    index_point = 0

    for index, the_node in enumerate(data_green):
        if index < len(data_green) - 1:
            for point in range(25):
                if point == 0:
                    pos_of_node = cmds.objectCenter(the_node)
                    for number_of_points in range(6):
                        pos_node_x = math.sin(math.radians(angle + (36*number_of_points))) + pos_of_node[0]
                        pos_node_z = math.cos(math.radians(angle + (36*number_of_points))) + pos_of_node[2]
                        print(index_point)
                        #if index_point == 225:
                        #    index_point = 224
                        cmds.setKeyframe('camera1',v=pos_node_x,at='translateX',t=keyframe_time_camera)
                        cmds.setKeyframe('camera1',v=WholeCurvePointsGreen[index_point][1],at='translateY',t=keyframe_time_camera)
                        cmds.setKeyframe('camera1',v=pos_node_z,at='translateZ',t=keyframe_time_camera)
                        
                        cmds.setKeyframe('camera1_aim',v=WholeCurvePointsGreen[index_point][0],at='translateX',t=keframe_time_aim)
                        cmds.setKeyframe('camera1_aim',v=WholeCurvePointsGreen[index_point][1],at='translateY',t=keframe_time_aim)
                        cmds.setKeyframe('camera1_aim',v=WholeCurvePointsGreen[index_point][2],at='translateZ',t=keframe_time_aim)
                        
                        keyframe_time_camera += 20
                        keframe_time_aim += 20
                    print("BEGIN",index_point)
                    index_point += 1
                    continue
                elif point == 24:
                    #print(data_point_index)
                    print("END OF", index_point)
                    if len(WholeCurvePointsGreen) - 1 == index_point:
                        print("END!")
                        pos_of_node = cmds.objectCenter(data_green[index+1])
                        for number_of_points in range(6):
                            pos_node_x = math.sin(math.radians(angle + (36*number_of_points))) + pos_of_node[0]
                            pos_node_z = math.cos(math.radians(angle + (36*number_of_points))) + pos_of_node[2]
                            
                            #print(WholeCurvePoints[index_point][1])
                            
                            cmds.setKeyframe('camera1',v=pos_node_x,at='translateX',t=keyframe_time_camera)
                            cmds.setKeyframe('camera1',v=WholeCurvePointsGreen[index_point][1],at='translateY',t=keyframe_time_camera)
                            cmds.setKeyframe('camera1',v=pos_node_z,at='translateZ',t=keyframe_time_camera)
                            
                            #print(WholeCurvePoints[index_point][1])
                            
                            cmds.setKeyframe('camera1_aim',v=WholeCurvePointsGreen[index_point][0],at='translateX',t=keframe_time_aim)
                            cmds.setKeyframe('camera1_aim',v=WholeCurvePointsGreen[index_point][1],at='translateY',t=keframe_time_aim)
                            cmds.setKeyframe('camera1_aim',v=WholeCurvePointsGreen[index_point][2],at='translateZ',t=keframe_time_aim)
                            
                            #print(WholeCurvePoints[index_point][1])
                            
                            keyframe_time_camera += 20
                            keframe_time_aim += 20
                        break
                    index_point += 1
                    continue
                #if index_point == 225 or index_point == 224:
                #    index_point = 223
                print(index_point)
                print(the_node)
                cmds.setKeyframe('camera1',v=WholeCurvePointsGreen[index_point][0],at='translateX',t=keyframe_time_camera)
                cmds.setKeyframe('camera1',v=WholeCurvePointsGreen[index_point][1],at='translateY',t=keyframe_time_camera)
                cmds.setKeyframe('camera1',v=WholeCurvePointsGreen[index_point][2],at='translateZ',t=keyframe_time_camera)
                
                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsGreen[index_point+1][0],at='translateX',t=keframe_time_aim)
                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsGreen[index_point+1][1],at='translateY',t=keframe_time_aim)
                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsGreen[index_point+1][2],at='translateZ',t=keframe_time_aim)
                keyframe_time_camera += 8
                keframe_time_aim += 8
                print("NORMAL",index_point)
                index_point += 1

    cmds.setKeyframe('camera1_aim',v=node_center[0],at='translateX',t=keframe_time_aim)
    cmds.setKeyframe('camera1_aim',v=node_center[1],at='translateY',t=keframe_time_aim)
    cmds.setKeyframe('camera1_aim',v=node_center[2],at='translateZ',t=keframe_time_aim)
    
    for revolutions in range(2):
        for number_of_points in range(15):
            pos_cam_x = (math.sin(math.radians((24*number_of_points))) + (node_center[0] / distance_cam)) * distance_cam
            pos_cam_z = (math.cos(math.radians((24*number_of_points))) + (node_center[2] / distance_cam)) * distance_cam
            cmds.setKeyframe('camera1',v=pos_cam_x,at='translateX',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=node_center[1],at='translateY',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=pos_cam_z,at='translateZ',t=keyframe_time_camera)
            if number_of_points == 0 and revolutions == 0:
                keyframe_time_camera += 80
                keframe_time_aim += 80
            else:
                keyframe_time_camera += 30
                keframe_time_aim += 30
                
            if revolutions == 1 and number_of_points == 0:
                cmds.setKeyframe('floatConstant1', v=1, at='inFloat', t=keyframe_time_camera)
                cmds.setKeyframe('floatConstant1', v=0, at='inFloat', t=keyframe_time_camera+10)
                cmds.setKeyframe('floatConstant1', v=0, at='inFloat', t=keyframe_time_camera+390)
                cmds.setKeyframe('floatConstant1', v=1, at='inFloat', t=keyframe_time_camera+400)
            
    cmds.setKeyframe('camera1_aim',v=node_center[0],at='translateX',t=keframe_time_aim-30)
    cmds.setKeyframe('camera1_aim',v=node_center[1],at='translateY',t=keframe_time_aim-30)
    cmds.setKeyframe('camera1_aim',v=node_center[2],at='translateZ',t=keframe_time_aim-30)

    index_point = 0

    for index, the_node in enumerate(data_blue):
        if index < len(data_blue) - 1:
            for point in range(25):
                if point == 0:
                    pos_of_node = cmds.objectCenter(the_node)
                    for number_of_points in range(6):
                        pos_node_x = math.sin(math.radians(angle + (36*number_of_points))) + pos_of_node[0]
                        pos_node_z = math.cos(math.radians(angle + (36*number_of_points))) + pos_of_node[2]
                        print(index_point)
                        #if index_point == 225:
                        #    index_point = 224
                        cmds.setKeyframe('camera1',v=pos_node_x,at='translateX',t=keyframe_time_camera)
                        cmds.setKeyframe('camera1',v=WholeCurvePointsBlue[index_point][1],at='translateY',t=keyframe_time_camera)
                        cmds.setKeyframe('camera1',v=pos_node_z,at='translateZ',t=keyframe_time_camera)
                        
                        cmds.setKeyframe('camera1_aim',v=WholeCurvePointsBlue[index_point][0],at='translateX',t=keframe_time_aim)
                        cmds.setKeyframe('camera1_aim',v=WholeCurvePointsBlue[index_point][1],at='translateY',t=keframe_time_aim)
                        cmds.setKeyframe('camera1_aim',v=WholeCurvePointsBlue[index_point][2],at='translateZ',t=keframe_time_aim)
                        
                        keyframe_time_camera += 20
                        keframe_time_aim += 20
                    print("BEGIN",index_point)
                    index_point += 1
                    continue
                elif point == 24:
                    #print(data_point_index)
                    print("END OF", index_point)
                    if len(WholeCurvePointsBlue) - 1 == index_point:
                        print("END!")
                        pos_of_node = cmds.objectCenter(data_blue[index+1])
                        for number_of_points in range(6):
                            pos_node_x = math.sin(math.radians(angle + (36*number_of_points))) + pos_of_node[0]
                            pos_node_z = math.cos(math.radians(angle + (36*number_of_points))) + pos_of_node[2]
                            
                            #print(WholeCurvePoints[index_point][1])
                            
                            cmds.setKeyframe('camera1',v=pos_node_x,at='translateX',t=keyframe_time_camera)
                            cmds.setKeyframe('camera1',v=WholeCurvePointsBlue[index_point][1],at='translateY',t=keyframe_time_camera)
                            cmds.setKeyframe('camera1',v=pos_node_z,at='translateZ',t=keyframe_time_camera)
                            
                            #print(WholeCurvePoints[index_point][1])
                            
                            cmds.setKeyframe('camera1_aim',v=WholeCurvePointsBlue[index_point][0],at='translateX',t=keframe_time_aim)
                            cmds.setKeyframe('camera1_aim',v=WholeCurvePointsBlue[index_point][1],at='translateY',t=keframe_time_aim)
                            cmds.setKeyframe('camera1_aim',v=WholeCurvePointsBlue[index_point][2],at='translateZ',t=keframe_time_aim)
                            
                            #print(WholeCurvePoints[index_point][1])
                            
                            keyframe_time_camera += 20
                            keframe_time_aim += 20
                        break
                    index_point += 1
                    continue
                #if index_point == 225 or index_point == 224:
                #    index_point = 223
                print(index_point)
                print(the_node)
                cmds.setKeyframe('camera1',v=WholeCurvePointsBlue[index_point][0],at='translateX',t=keyframe_time_camera)
                cmds.setKeyframe('camera1',v=WholeCurvePointsBlue[index_point][1],at='translateY',t=keyframe_time_camera)
                cmds.setKeyframe('camera1',v=WholeCurvePointsBlue[index_point][2],at='translateZ',t=keyframe_time_camera)
                
                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsBlue[index_point+1][0],at='translateX',t=keframe_time_aim)
                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsBlue[index_point+1][1],at='translateY',t=keframe_time_aim)
                cmds.setKeyframe('camera1_aim',v=WholeCurvePointsBlue[index_point+1][2],at='translateZ',t=keframe_time_aim)
                keyframe_time_camera += 8
                keframe_time_aim += 8
                print("NORMAL",index_point)
                index_point += 1
    
    '''for point_indx, point in enumerate(WholeCurvePoints):
        if point_indx < len(WholeCurvePoints) - 1:
            if point_indx % start_num == 0:
                pos_of_node = cmds.objectCenter(all_data_sequence[node_sequence])
                for number_of_points in range(6):
                    pos_node_x = math.sin(math.radians(angle + (36*number_of_points))) + pos_of_node[0]
                    pos_node_z = math.cos(math.radians(angle + (36*number_of_points))) + pos_of_node[2]
                    
                    cmds.setKeyframe('camera1',v=pos_node_x,at='translateX',t=keyframe_time_camera)
                    cmds.setKeyframe('camera1',v=point[1],at='translateY',t=keyframe_time_camera)
                    cmds.setKeyframe('camera1',v=pos_node_z,at='translateZ',t=keyframe_time_camera)
                    
                    cmds.setKeyframe('camera1_aim',v=point[0],at='translateX',t=keframe_time_aim)
                    cmds.setKeyframe('camera1_aim',v=point[1],at='translateY',t=keframe_time_aim)
                    cmds.setKeyframe('camera1_aim',v=point[2],at='translateZ',t=keframe_time_aim)
                    
                    keyframe_time_camera += 20
                    keframe_time_aim += 20
                node_sequence += 1
                print(((9*start_num_CONST) + 9 - 1))
                print("P",point_indx)
                if point_indx % ((len(data_red)*start_num_CONST) + len(data_red) - 1) == 0 and point_indx != 0:
                    start_num_decrease += 1
                    print('YYY')
                    cmds.setKeyframe('camera1_aim',v=node_center[0],at='translateX',t=keframe_time_aim)
                    cmds.setKeyframe('camera1_aim',v=node_center[1],at='translateY',t=keframe_time_aim)
                    cmds.setKeyframe('camera1_aim',v=node_center[2],at='translateZ',t=keframe_time_aim)
                    for revolutions in range(2):
                        for number_of_points in range(15):
                            pos_cam_x = (math.sin(math.radians((24*number_of_points))) + (node_center[0] / 400)) * 400
                            pos_cam_z = (math.cos(math.radians((24*number_of_points))) + (node_center[2] / 400)) * 400
                            cmds.setKeyframe('camera1',v=pos_cam_x,at='translateX',t=keyframe_time_camera)
                            cmds.setKeyframe('camera1',v=node_center[1],at='translateY',t=keyframe_time_camera)
                            cmds.setKeyframe('camera1',v=pos_cam_z,at='translateZ',t=keyframe_time_camera)
                            if number_of_points == 0 and revolutions == 0:
                                keyframe_time_camera += 80
                                keframe_time_aim += 80
                            else:
                                keyframe_time_camera += 30
                                keframe_time_aim += 30
                    cmds.setKeyframe('camera1_aim',v=WholeCurvePoints[point_indx+1][0],at='translateX',t=keframe_time_aim)
                    cmds.setKeyframe('camera1_aim',v=WholeCurvePoints[point_indx+1][1],at='translateY',t=keframe_time_aim)
                    cmds.setKeyframe('camera1_aim',v=WholeCurvePoints[point_indx+1][2],at='translateZ',t=keframe_time_aim)
                    keyframe_time_camera += 30
                    keframe_time_aim += 30
                start_num = start_num + 25 - start_num_decrease

            cmds.setKeyframe('camera1',v=point[0],at='translateX',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=point[1],at='translateY',t=keyframe_time_camera)
            cmds.setKeyframe('camera1',v=point[2],at='translateZ',t=keyframe_time_camera)
            
            cmds.setKeyframe('camera1_aim',v=WholeCurvePoints[point_indx+1][0],at='translateX',t=keframe_time_aim)
            cmds.setKeyframe('camera1_aim',v=WholeCurvePoints[point_indx+1][1],at='translateY',t=keframe_time_aim)
            cmds.setKeyframe('camera1_aim',v=WholeCurvePoints[point_indx+1][2],at='translateZ',t=keframe_time_aim)
            keyframe_time_camera += 20
            keframe_time_aim += 20'''
        
    #cmds.curve(p=WholeCurvePoints, d=2)
    cmd.select('camera1_group')
    mel.eval('keyTangent -itt spline -ott spline -animation objects graphEditor1FromOutliner')

read_csv_data(line_count)    
gen(data_red,data_yellow,data_green,data_blue)
algo(data_red,sets)
create_connection(new_connections,data_red)
#except:
    #mel.eval('file -f -new')
cmd.polySeparate('nodesCombined') 
mel.eval('DeleteAllHistory')
renaming()
fading_bridges()
camera_flythrough_generate()
for i in range(len(data_red)):
    cmds.expression(s="typeMesh{}.rotateX = camera1.rotateX;\ntypeMesh{}.rotateY = camera1.rotateY;\ntypeMesh{}.rotateZ = camera1.rotateZ".format(i+1,i+1,i+1))