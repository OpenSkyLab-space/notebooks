import nbformat,sys
for f in sys.argv[1:]:
    nb=nbformat.read(f,4)
    for i,c in enumerate(nb.cells):
        if c.cell_type!='code': continue
        for o in c.outputs:
            if o.output_type=='stream': print(f'[{i}]',o.text[:1500])
            elif o.output_type=='error': print(f'[{i}] ERR',o.ename,o.evalue)
            elif 'text/plain' in o.get('data',{}) and 'image/png' not in o['data']: print(f'[{i}]',o['data']['text/plain'][:1500])
            elif 'image/png' in o.get('data',{}): print(f'[{i}] <image>')
