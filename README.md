# NFT-Tool
Render Tools about NFT Project

===================================

usage example :
	blender -b -P main.py -- [OUTPUT_MODE] [INPUT_PARAM]

OUTPUT_MODE :
	0 -- Pawn
	1 -- Pawn with Pose
	2 -- Composition

OUTPUT_MODE == 0 (Pawn) || OUTPUT_MODE == 1 (Pawn with Pose) :
	INPUT_PARAM : 
		{
			"TOKEN_ID" : UNIQUE_ID,
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
			"Target" : SCENE_ID/PLACE_ID/PART_ID/WHOLE_ID,
			"TOKEN_ID" : UNIQUE_ID,
			"Pawns" : [
				{
					"ID" : PAWN_ID,
					"TOKEN_ID" : UNIQUE_ID,
				},
				... 
			]
		}

====================================

Output Path :

	Pawn :
		output/pawn/[PawnID]/ "Pawn_" + [UniqueID].png
		output/pawn/[PawnID]/ "Pawn_" + [UniqueID].glb

	Scene :
		output/scene/ "Scene_" + [UniqueID].png

	Place :
		output/place/ "Place_" + [UniqueID].png

	Part :
		output/part/ "Part_" + [UniqueID].png

	Whole :
		output/whole/ "Whole_" + [UniqueID].png
