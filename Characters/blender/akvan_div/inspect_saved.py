import bpy
import json
import hashlib
expected=['Akvan_Head_Headwear','Akvan_Eyes_Brows','Akvan_Torso_GarmentCore','Akvan_Arm_L','Akvan_Arm_R','Akvan_LowerGarment_Legs']
scene=bpy.data.scenes['Akvan_Inspection_v01']
root=bpy.data.collections['CHAR_AkvanDiv']
assert sorted(c.name for c in root.children)==['01_Reference','02_BaseMesh','03_Armature','04_StudioRig']
col=bpy.data.collections['02_BaseMesh']
assert sorted(o.name for o in col.objects)==sorted(expected)
assert len(bpy.data.collections['03_Armature'].objects)==0
report={'blender':bpy.app.version_string,'scene':scene.name,'meshes':[]}
for name in expected:
 obj=col.objects[name]
 assert obj.type=='MESH'
 assert tuple(obj.location)==(0.0,0.0,0.0) and tuple(obj.rotation_euler)==(0.0,0.0,0.0) and tuple(obj.scale)==(1.0,1.0,1.0)
 assert len(obj.users_collection)==1 and len(obj.data.materials)==6
 assert len(obj.data.vertices)>0
 report['meshes'].append({'name':name,'vertices':len(obj.data.vertices),'faces':len(obj.data.polygons),'min_z':min((obj.matrix_world@v.co).z for v in obj.data.vertices)})
assert min((col.objects[expected[-1]].matrix_world@v.co).z for v in col.objects[expected[-1]].data.vertices)==0.0
assert len([o for o in scene.objects if o.type=='MESH'])==6
assert len([o for o in scene.objects if o.type=='LIGHT'])==3
assert len([o for o in scene.objects if o.type=='CAMERA'])==2
assert not any(o.name.startswith('Akvan_Prop_Proxy') for o in scene.objects)
ref=bpy.data.objects['Akvan_ApprovedMaster']
assert ref.name in bpy.data.collections['01_Reference'].objects
assert all(ref.lock_location) and all(ref.lock_rotation) and all(ref.lock_scale) and ref.hide_select
assert ref.data.packed_file is not None
reference_hash=hashlib.sha256(bytes(ref.data.packed_file.data)).hexdigest()
assert reference_hash=='47362a764bc38cce4e09ab022741a093a296fb69918344eb33bf6fa1829e6813'
for material in col.objects[expected[0]].data.materials:
 shader=next(n for n in material.node_tree.nodes if n.type=='BSDF_PRINCIPLED')
 assert shader.inputs['Roughness'].default_value>0.8
assert scene.camera.name=='Akvan_FrontCamera'
report.update({'status':'PASS','reference_packed':True,'reference_sha256':reference_hash,'missing_image_dependencies':[i.name for i in bpy.data.images if i.source=='FILE' and not i.packed_file], 'cameras':2,'lights':3,'armatures':0,'fps':scene.render.fps,'frame_range':[scene.frame_start,scene.frame_end],'resolution':[scene.render.resolution_x,scene.render.resolution_y],'engine':scene.render.engine})
assert report['missing_image_dependencies']==[]
print('AKVAN_AUDIT='+json.dumps(report))
