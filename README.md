# NFT-Tool
Render Tools about NFT Project

===================================

main.py : the main script of this tool

config.py : the configuration file of the components/animations/...
	note that the config file list in "blender\2.92\scripts\modules"

input folder : put original resource file here

output folder : get your glb or png file here

===================================

usage example :
	blender -b -P main.py -- [OUTPUT_PATH] [OUTPUT_MODE] [INPUT_PARAM]

OUTPUT_PATH :
	relative to the .\output folder

OUTPUT_MODE :
	0 -- Pawn
	1 -- Pawn with Pose
	2 -- Composition

OUTPUT_MODE == 0 (Pawn) || OUTPUT_MODE == 1 (Pawn with Pose) :
	INPUT_PARAM : 
		{
			"ID" : PAWN_ID,
			"Hat" : COMPONENT_ID, 
			"Head" : COMPONENT_ID,
			"Jacket" : COMPONENT_ID,
			"Trousers" : COMPONENT_ID,
			"Shoes" : COMPONENT_ID,
			"Type" : COMPONENT_ID
		}
	
	[Note] when COMPONENT_ID == -1, this component will be ignored

OUPUT_MODE == 2 (Composition) :
	INPUT_PARAM : 
		{
			"Target" : SCENE_ID/PLACE_ID/PART_ID/WHOLE_ID, --- Ref to environment resource
			"Pawns" : [
				{
					"Pawn" : PAWN_ID, --- Ref to position in scene
					"Hat" : COMPONENT_ID,
					"Head" : COMPONENT_ID,
					"Jacket" : COMPONENT_ID,
					"Trousers" : COMPONENT_ID,
					"Shoes" : COMPONENT_ID,
					"Type" : COMPONENT_ID
				},
				{
					...
				},
				... 
			]
		}

====================================

extra configuration :

camera : 
	position {X,Y,Z} rotation {X,Y,Z} -- the camera used to capture the picture
				define in *config.py*

render solution :
	x y 

====================================

