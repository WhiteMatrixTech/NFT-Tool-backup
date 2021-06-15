# NFT-Tool
Render Tools about NFT Project

===================================

## USAGE :
	blender -b -P main.py -- [OUTPUT_MODE] [INPUT_PARAM]

## OUTPUT_MODE :
	
	0 -- Pawn

	1 -- Pawn with Pose
	
	2 -- Composition

## INPUT_PARAM :

### OUTPUT_MODE == 0 (Pawn) || OUTPUT_MODE == 1 (Pawn with Pose):

```json
{
	"TOKEN_ID" : 0,
	"ID" : 0,
	"Hat" : 0, 
	"Head" : 0,
	"Jacket" : 0,
	"Trousers" : 0,
	"Shoes" : 0,
	"Type" : 0
}
```
	
	ID : Pawn ID
	Hat : Component ID
	Head : Component ID
	Jacket : Component ID
	Trousers : Component ID
	Shoes : Component ID
	Type : Component ID

	[Note] when COMPONENT_ID == -1, this component will be ignored

### OUPUT_MODE == 2 (Composition) :

```json
{
	"Target" : 0, 
	"TOKEN_ID" : 0,
	"Pawns" : [
		{
			"ID" : 0,
			"TOKEN_ID" : 0,
		},
		{
			"ID" : 0,
			"TOKEN_ID" : 0,
		}
	]
}
```

	Target : Scene ID / Place ID / Part ID / Whole ID
	Pawns : Array of Pawns 

## OUTPUT :

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
