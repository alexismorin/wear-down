import maya.cmds as cmds
import maya.mel as mel
import random
import math

# VARIABLES

# How big the chunks taken off the mesh are by default
minChunkScale = 0.2
maxChunkScale = 0.5

# Chunks are deformed based on the length of the edge of which they are in, this is a multiplier for that
chunkDeformScale = 0.5

# Probability of chunking per edge meter. 1.5 means that for a 2 meter edge, you get three chunks.
chunkRatioPerUnit = 0.75


# Code Begins ---------------------------------------------------------------------------


# All of this is a single undo
cmds.undoInfo(openChunk= True)

sel = cmds.ls(sl=True, o=True)[0]
edges = cmds.ls(sel + ".e[:]", flatten=1)
chunks = []

# we blacken the model
cmds.polyColorPerVertex(sel, rgb=(0.0, 0.0, 0.0),cdo=True )


# We bevel the mesh for that sandblasted look
#cmds.polyBevel( sel, oaf=True, offset=0.3 )

for edge in edges:
    # we get all edges in the model and convert them into a list of vertices
    cmds.select(edge)
    points = cmds.polyListComponentConversion( tv=True)
    flatpoints = cmds.ls(points, fl=True)

    # we compute the distance between each edge's two points
    pointA = cmds.pointPosition(flatpoints[0])
    pointB = cmds.pointPosition(flatpoints[1])
    dx = pointA[0] - pointB[0]
    dy = pointA[1] - pointB[1]
    dz = pointA[2] - pointB[2]
    distance = math.sqrt( dx*dx + dy*dy + dz*dz )

    # based on edge length and a given ratio, we place chunks across each edge
    chunkAmount = distance * chunkRatioPerUnit
    for i in range(int(chunkAmount)):
        
        chunkPercent = random.random()
        x = ((pointB[0]-pointA[0])*chunkPercent)+pointA[0]
        y = ((pointB[1]-pointA[1])*chunkPercent)+pointA[1]
        z = ((pointB[2]-pointA[2])*chunkPercent)+pointA[2]
        spawnposition = (x,y,z)
        
        chunk = cmds.polySphere(sx=random.randrange(3,6), sy=random.randrange(3,6), r=random.uniform(minChunkScale, maxChunkScale))
        cmds.polyColorPerVertex(chunk, rgb=(1.0, 1.0, 1.0) )
        cmds.xform( t=spawnposition )
        
        xScale = random.uniform(minChunkScale*chunkDeformScale, maxChunkScale*chunkDeformScale*distance)
        yScale = random.uniform(minChunkScale*chunkDeformScale, maxChunkScale*chunkDeformScale*distance)
        zScale = random.uniform(minChunkScale*chunkDeformScale, maxChunkScale*chunkDeformScale*distance)
        
        cmds.scale( xScale, yScale, zScale, chunk)
        cmds.rotate( random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360), chunk )
        cmds.polySoftEdge( a=180 )
        chunks +=  cmds.ls(chunk,sl=True)


combinedChunk = chunks[0]
uniteLength = len(chunks)-1
for i in range(uniteLength):
    booleanChunk = cmds.polyBoolOp(combinedChunk,chunks[i+1], op=1,ch=False, n="united" )
    combinedChunk = cmds.ls(booleanChunk,sl=True)

       
finalmodel = cmds.polyBoolOp( sel,combinedChunk , op=2,ch=True, n='brokenModel' )

cmds.polyRemesh(maxEdgeLength=0.15,collapseThreshold=10.0)

cmds.polySoftEdge( a=180 )
cmds.polyMergeVertex( d=0.030 )
cmds.polyAverageVertex(i=1);

mel.eval('polyCleanupArgList 4 { "0","1","1","0","0","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","1","1","0" };')

cmds.select(finalmodel)
cmds.polyReduce(p=50)

cmds.polyMergeVertex( d=0.020 )
cmds.polySoftEdge( a=180 )



cmds.undoInfo(closeChunk= True)


