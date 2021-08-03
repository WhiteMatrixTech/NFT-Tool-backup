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
	"tokenId" : 0,
	"id" : 0,
	"hat" : 0, 
	"head" : 0,
	"jacket" : 0,
	"trousers" : 0,
	"shoes" : 0,
	"type" : 0,
	"backGround" : 0
}
```
	
	id : Pawn ID
	hat : Component ID
	head : Component ID
	jacket : Component ID
	trousers : Component ID
	shoes : Component ID
	type : Component ID
	backGround : BackGround Texture ID

	[Note] when COMPONENT_ID == -1, this component will be ignored

### OUPUT_MODE == 2 (Composition) :

```json
{
	"target" : 0, 
	"tokenId" : 0,
	"pawns" : [
		{
			"id" : 0,
			"tokenId" : 0,
		},
		{
			"id" : 0,
			"tokenId" : 0,
		}
	]
}
```

	target : Scene ID / Place ID / Part ID / Whole ID
	pawns : Array of Pawns 

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
		
## Docker Usage
### Build
```
docker build . -t renderjob 
```

### Run
```bash
export ROOT=$(pwd)
docker run -v $ROOT/../data:/data -it renderjob bash "./scripts/test_run_pawn.sh"
```

OR 

```bash
export ROOT=$(pwd)
docker run -v $ROOT/data:/data -it --name renderjob renderjob

docker exec -it renderjob bash

# in container
blender -b -P main.py -- 1 "{\"tokenId\" : 0,\"id\" : 0,\"hat\" : -1,\"head\" : 1,\"jacket\" : 2,\"trousers\" : 3,\"shoes\" : 4,\"type\" : -1}"

```
