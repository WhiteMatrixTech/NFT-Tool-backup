from pathlib import Path


def batch_renaming(suffix):
    for path in Path('./data').rglob('*.' + suffix.upper()):
        print('renaming ' + path.name[:-4])
        path.rename(str(path.parent.absolute()) + '/' + str(path.name[:-4]) + '.' + suffix.lower())


batch_renaming('FBX')
batch_renaming('MAX')
batch_renaming('JPG')
batch_renaming('PNG')