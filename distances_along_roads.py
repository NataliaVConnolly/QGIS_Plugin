### this is for the roads layer set to the WGS 84 system
### make sure to go to view->panels->layers
# also check out https://github.com/chourmo/QGIS-Transit-tools/tree/master/scripts
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.networkanalysis import *

vl = qgis.utils.iface.mapCanvas().currentLayer()

director = QgsLineVectorLayerDirector(vl, -1, '', '', '', 3)
properter = QgsDistanceArcProperter()
director.addProperter(properter)
crs = qgis.utils.iface.mapCanvas().mapRenderer().destinationCrs()
builder = QgsGraphBuilder(crs)


file=open('/data/Distances.txt','w')
myarr1={}
myarr2={}
count1=0
file1=open('/Data/Addresses1_Geocoded.txt','r')
for line in file1:
  arr1 = line.split('\t')
  if (count1 > 0):
    if (arr1[1] >= 0.8):
      myarr1[arr1[0]] = [arr1[2],arr1[3]]
  count1 = count1+1

file1.close()


file2=open('/data/Addresses2_Geocoded.txt','r')
count2 = 0
for line in file2:
  arr2 = line.split('\t')
  if (count2 > 0):
    if (arr2[1] >= 0.8):
      myarr2[arr2[0]] = [arr2[2],arr2[3]]
  count2 = count1+1

file2.close()

for k in myarr1:
  if k in myarr2:
    x1 = myarr1[k][0]
    y1 = myarr1[k][1]
    x2 = myarr2[k][0]
    y2 = myarr2[k][1]
    
    #print "x1=",x1,"y1=",y1
    pStart = QgsPoint(float(y1),float(x1))
    pStop = QgsPoint(float(y2),float(x2))

    tiedPoints = director.makeGraph(builder, [pStart, pStop])
    graph = builder.graph()
    tStart = tiedPoints[0]
    tStop = tiedPoints[1]
    idStart = graph.findVertex(tStart)
    tree = QgsGraphAnalyzer.shortestTree(graph, idStart, 0)
    idStart = graph.findVertex(tiedPoints[0])
    idStop = graph.findVertex(tiedPoints[1])
    (tree, cost) = QgsGraphAnalyzer.dijkstra(graph, idStart, 0)
    totalLength = 0.    
    rb = QgsRubberBand(qgis.utils.iface.mapCanvas())
    rb.setColor(Qt.red)    
    if tree[idStop] == -1:
      print "Path not found"
    else:
      p = []
      curPos = idStop
      while curPos != idStart:
        p.append(graph.vertex(graph.arc(tree[curPos]).inVertex()).point())
        curPos = graph.arc(tree[curPos]).outVertex();
        ### my additions start here
        #line = QgsGeometry.fromPolyline([graph.vertex(graph.arc(tree[curPos]).inVertex()).point(), graph.vertex(graph.arc(tree[curPos]).outVertex()).point()]) 
        #print >>f1,"length of line is ",line.length()        
        #p.append(tStart)          
    for pnt in p:
      rb.addPoint(pnt)
          
    len = (rb.asGeometry()).length();
    file.write(k+'\t'+len)



file.close()


#######



