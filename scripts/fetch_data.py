"""Restore the published v1.0.0 records, without login, simulation, or test labels.

Run after `uv sync --extra download`. This script is optional: data are bundled.
"""
import json
from pathlib import Path
import numpy as np
from catflip.data import content_hash


def main():
    import pyarrow.compute as pc
    from aqora.pyarrow import dataset
    root=Path(__file__).resolve().parent.parent/'data'
    manifest=json.loads((root/'manifest.json').read_text())
    for tier in ('A','B'):
        table=dataset(f'Alice_Bob/catch-the-flip-tier-{tier.lower()}',
                      'v1.0.0',aqora_auth=False).to_table()
        for split in ('train','val','test'):
            t=table.filter(pc.field('split')==split).sort_by([('segment_id','ascending')])
            d={'nbar':t['nbar'].to_numpy(),
               'meta':{**json.loads(t.schema.metadata[b'catchtheflip']),'n':len(t)}}
            if split!='test':
                d['labels']=t['label'].to_numpy().astype(np.int8)
            if tier=='A':
                col=t['clicktimes'].combine_chunks(); counts=col.value_lengths().to_numpy()
                clicks=np.full((len(col),int(counts.max())+1),np.nan)
                clicks[np.arange(clicks.shape[1])[None,:]<counts[:,None]]=col.flatten().to_numpy()
                d['clicktimes']=clicks
            else:
                for key in ('I','Q'):
                    d[key]=t[key].combine_chunks().flatten().to_numpy().reshape(len(t),-1).astype(np.float16)
            name=f'tier{tier}_{split}.npz'
            if content_hash(d)!=manifest['files'][name]['content_sha256']:
                raise ValueError(f'{name}: published data no longer match bundled version; not overwriting.')
            temporary=root/(name+'.download.npz')
            np.savez_compressed(temporary,**dict(d,meta=json.dumps(d['meta'])))
            temporary.replace(root/name)
            print('Restored',name,len(t),'segments',flush=True)


if __name__=='__main__': main()
