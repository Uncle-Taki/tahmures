import math,json
from pathlib import Path
OUT=Path('/home/mehdi/Project/leela/tahmures/Characters/blender/akvan_div')
parts={n:[[],[],[]] for n in ['Akvan_Head_Headwear','Akvan_Eyes_Brows','Akvan_Torso_GarmentCore','Akvan_Arm_L','Akvan_Arm_R','Akvan_LowerGarment_Legs']}
# Artwork-derived frontal coordinates, expressed in proportional scene units.
def P(x,z,y): return ((x-543)/200,y,(1404-z)/200)
def poly(n,points,y,thick,mat):
 v,f,m=parts[n]; start=len(v); N=len(points)
 v.extend([P(x,z,y) for x,z in points]);v.extend([P(x,z,y+thick) for x,z in points])
 f.append([start+i for i in reversed(range(N))]);m.append(mat)
 f.append([start+N+i for i in range(N)]);m.append(mat)
 for i in range(N): f.append([start+i,start+(i+1)%N,start+N+(i+1)%N,start+N+i]);m.append(mat)
def tube(n,centers,radii,mat,segments=10):
 v,f,m=parts[n];start=len(v)
 for (x,z,y),r in zip(centers,radii):
  for i in range(segments):
   a=2*math.pi*i/segments; px,py,pz=P(x,z,y);v.append((px+r*math.cos(a),py+r*math.sin(a),pz))
 for j in range(len(centers)-1):
  for i in range(segments):f.append([start+j*segments+i,start+j*segments+(i+1)%segments,start+(j+1)*segments+(i+1)%segments,start+(j+1)*segments+i]);m.append(mat)
 f.extend([[start+i for i in reversed(range(segments))],[start+(len(centers)-1)*segments+i for i in range(segments)]]);m.extend([mat,mat])
def mirror(points):return [(1086-x,z) for x,z in points]
H='Akvan_Head_Headwear';E='Akvan_Eyes_Brows';T='Akvan_Torso_GarmentCore';G='Akvan_LowerGarment_Legs'
# tapered head, raised angular nose, long neck
poly(H,[(503,160),(543,131),(583,160),(586,206),(574,242),(552,266),(539,268),(514,242),(499,203)],-.27,.49,0)
poly(H,[(525,192),(540,184),(550,219),(544,229),(533,225)],-.34,.1,0)
poly(T,[(520,247),(566,247),(565,323),(579,345),(542,381),(505,344),(522,320)],-.02,.31,0)
for s in [False,True]:
 q=lambda pts:mirror(pts) if s else pts
 poly(H,q([(496,195),(443,175),(473,210),(498,221)]),-.06,.16,0)
 poly(H,q([(490,207),(500,219),(494,279),(486,258)]),-.23,.10,5)
 for pts,dep in [([(537,106),(513,104),(477,134),(459,176),(492,171),(526,140)],-.37), ([(489,180),(461,192),(453,218),(488,215)],.09), ([(491,210),(463,226),(444,250),(492,247)],.11), ([(493,244),(460,264),(431,303),(494,313)],.14), ([(499,283),(456,316),(422,355),(506,347)],.18)]:poly(H,q(pts),dep,.17,4)
 centers=[(490,137,.12),(477,115,.13),(453,100,.14),(438,77,.15),(426,33,.16)]
 if s:centers=[(1086-x,z,y) for x,z,y in centers]
 tube(H,centers,[.085,.092,.071,.04,.002],5)
 # almond eyes, lids and brows
 poly(E,q([(500,181),(512,179),(531,189),(518,192),(507,188)]),-.302,.012,3)
 poly(E,q([(501,179),(514,178),(531,186),(532,189),(514,183)]),-.319,.012,4)
 poly(E,q([(506,164),(520,166),(533,176),(532,180),(517,171),(503,170)]),-.32,.015,4)
 poly(E,q([(513,182),(520,185),(519,190),(514,189)]),-.325,.015,4)
poly(E,[(532,239),(542,235),(553,240),(544,243)],-.345,.02,4)
# torso shaped rather than cube: layered shoulder and tapered waist
poly(T,[(468,355),(507,333),(542,387),(578,333),(618,355),(594,476),(587,541),(546,561),(499,541),(483,470)],-.07,.45,1)
poly(T,[(533,384),(546,397),(555,547),(543,560),(532,545)],-.105,.035,2)
for s in [False,True]:
 q=lambda pts:mirror(pts) if s else pts
 poly(T,q([(505,321),(515,351),(542,389),(536,399),(501,347)]),-.125,.04,3)
 poly(T,q([(489,541),(541,562),(541,585),(483,567)]),-.15,.07,3)
 poly(T,q([(541,390),(526,430),(542,466),(558,430)]),-.17,.04,5)
 poly(T,q([(542,409),(535,430),(543,447),(550,430)]),-.22,.02,2)
poly(T,[(542,546),(525,580),(542,614),(560,580)],-.24,.04,5)
poly(T,[(542,562),(534,580),(542,598),(551,580)],-.29,.02,2)
# layered flared skirt and pointed separated shoes
poly(G,[(493,568),(592,568),(670,830),(858,1243),(704,1274),(612,1269),(543,1298),(473,1269),(382,1274),(227,1243),(416,830)],.03,.48,2)
for s in [False,True]:
 q=lambda pts:mirror(pts) if s else pts
 poly(G,q([(494,568),(539,588),(494,797),(446,1057),(388,1255),(221,1237),(340,995),(413,786)]),-.15,.22,1)
 poly(G,q([(494,570),(530,588),(470,739),(381,824),(423,710)]),-.22,.10,1)
 poly(G,q([(458,740),(488,723),(432,980),(375,1053),(269,1094),(364,899)]),-.25,.08,1)
 poly(G,q([(232,1176),(389,1214),(383,1272),(217,1251)]),-.275,.06,3)
 for x,z in [(263,1217),(311,1230),(360,1243)]:
  poly(G,q([(x,z-15),(x+17,z),(x,z+15),(x-17,z)]),-.31,.02,2)
  poly(G,q([(x,z-9),(x+10,z),(x,z+9),(x-10,z)]),-.34,.01,1)
 tube(G,[(397,1261,.12),(393,1329,.10),(380,1364,-.02)],[.07,.065,.07],1,8) if not s else tube(G,[(689,1261,.12),(693,1329,.1),(706,1364,-.02)],[.07,.065,.07],1,8)
 poly(G,q([(381,1321),(413,1326),(406,1361),(363,1398),(318,1404),(344,1370)]),-.23,.40,1)
 poly(G,q([(379,1339),(409,1325),(398,1348),(365,1365)]),-.255,.025,5)
poly(G,[(519,587),(562,587),(592,1080),(544,1155),(491,1080)],-.29,.06,3)
poly(G,[(526,595),(555,595),(578,1076),(544,1137),(505,1076)],-.36,.045,1)
poly(G,[(539,607),(547,607),(560,1073),(544,1104),(528,1073)],-.42,.02,2)
poly(G,[(543,1041),(564,1078),(543,1111),(523,1078)],-.46,.025,5)
poly(G,[(543,1056),(554,1078),(543,1095),(533,1078)],-.50,.015,2)
# arms with layered sleeves, cuffs and distinct articulated finger silhouettes
for s,n in [(False,'Akvan_Arm_R'),(True,'Akvan_Arm_L')]:
 q=lambda pts:mirror(pts) if s else pts
 tube(n,[(472 if not s else 614,373,.13),(412 if not s else 674,543,.10),(333 if not s else 753,741,.04)],[.12,.10,.075],1)
 poly(n,q([(468,359),(432,379),(365,505),(452,536)]),-.02,.24,2)
 poly(n,q([(466,359),(438,400),(433,476),(365,504)]),-.15,.12,3)
 poly(n,q([(464,355),(423,372),(363,471),(401,453),(441,417)]),-.25,.12,1)
 poly(n,q([(406,563),(377,584),(296,700),(377,790),(406,651)]),-.11,.24,1)
 poly(n,q([(401,592),(405,672),(378,784),(349,754)]),-.16,.05,2)
 poly(n,q([(329,639),(296,700),(377,790),(382,760)]),-.26,.07,3)
 for x,z in [(323,689),(338,716)]:poly(n,q([(x,z-14),(x+8,z-4),(x+3,z+14),(x-9,z+4)]),-.35,.02,2)
 poly(n,q([(314,733),(330,752),(336,800),(329,824),(342,849),(329,844),(318,816),(316,801),(310,813),(318,840),(333,865),(320,854),(307,833),(296,811),(301,784)]),-.16,.17,0)
 # circular fasteners, gold
 centers=[(470 if not s else 616,354,-.30),(470 if not s else 616,371,-.30)]
 v,f,m=parts[n];start=len(v)
 x=470 if not s else 616
 for depth in [-.34,-.29]:
  for i in range(16):
   a=2*math.pi*i/16;v.append(P(x+11*math.cos(a),362+11*math.sin(a),depth))
 f.append([start+i for i in range(16)]);m.append(5)
 f.append([start+16+i for i in reversed(range(16))]);m.append(5)
 for i in range(16):f.append([start+i,start+(i+1)%16,start+16+(i+1)%16,start+16+i]);m.append(5)
for name,(verts,faces,mats) in parts.items():
 # build via bmesh, updating the existing mesh in place on rerun
 code="import bpy\nimport bmesh\n"
 code+=f"vertices = {verts!r}\nfaces = {faces!r}\nindices = {mats!r}\n"
 code+="""col = bpy.data.collections.get('02_BaseMesh')
"""
 code+=f"mesh = bpy.data.meshes.get('{name}_Mesh') or bpy.data.meshes.new('{name}_Mesh')\nobj = bpy.data.objects.get('{name}') or bpy.data.objects.new('{name}', mesh)\n"
 code+="""if obj.name not in col.objects:
    col.objects.link(obj)
bm = bmesh.new()
vs = []
for co in vertices:
    vs.append(bm.verts.new(co))
for face, material_index in zip(faces, indices):
    f = bm.faces.new([vs[i] for i in face])
    f.material_index = material_index
bm.normal_update()
bm.to_mesh(mesh)
bm.free()
obj.location = (0.0, 0.0, 0.0)
obj.rotation_euler = (0.0, 0.0, 0.0)
obj.scale = (1.0, 1.0, 1.0)
mesh.materials.clear()
for material_name in ['Akvan_Ochre','Akvan_Forest','Akvan_Rust','Akvan_Cream','Akvan_Charcoal','Akvan_PaleGold']:
    mesh.materials.append(bpy.data.materials.get(material_name))
for polygon, index in zip(mesh.polygons, indices):
    polygon.material_index = index
print(obj.name, len(mesh.vertices), len(mesh.polygons))
"""
 (OUT/(name+'.json')).write_text(json.dumps({'code':code}))
(OUT/'geometry-source.json').write_text(json.dumps(parts))
