# NFT-Tool
Tools about NFT Project

===================================

main.py : the main script of this tool

config.py : the configuration file of the components/animations/...
	note that the config file list in "blender\2.92\scripts\modules"

input folder : put original resource file here

output folder : get your glb or png file here

===================================

usage example :
	blender -b -P main.py -- [OUTPUT_PATH] [OUTPUT_MODE] [POSE_ID] [COMPONENT_ID_LIST]

OUTPUT_PATH :
	relative to the .\output folder

OUTPUT_MODE :
	0 -- output png and glTF
	1 -- output png only
	2 -- output glTF only

COMPONENT_ID_LIST :
	[0,1,2, ...] -- the id list of components  we want to combine
		define in *config.py*

POSE_ID :
	0/1/2/... -- the id of animation pose we want to apply 

====================================

extra configuration :

camera : 
	position {X,Y,Z} rotation {X,Y,Z} -- the camera used to capture the picture
				define in *config.py*

render solution :
	x y 