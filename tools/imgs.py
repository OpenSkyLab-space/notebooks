import nbformat,sys,base64,os
f,out=sys.argv[1],sys.argv[2];os.makedirs(out,exist_ok=True)
nb=nbformat.read(f,4)
for i,c in enumerate(nb.cells):
    for j,o in enumerate(c.get('outputs',[])):
        if 'image/png' in o.get('data',{}):
            open(f'{out}/{os.path.basename(f)[:-6]}_{i}_{j}.png','wb').write(base64.b64decode(o['data']['image/png']))
