"""Local challenge records only: never silently download or regenerate test data."""
import json
import hashlib
from pathlib import Path
import numpy as np


def load(data_dir, tier, split):
    path = Path(data_dir) / f'tier{tier}_{split}.npz'
    with np.load(path, allow_pickle=False) as archive:
        data = {key: archive[key] for key in archive.files}
    data['meta'] = json.loads(str(data['meta']))
    if split == 'test' and 'labels' in data:
        raise ValueError('Published test records must remain unlabelled.')
    return data


def content_hash(data):
    """Hash array contents and canonical metadata, independent of ZIP timestamps."""
    digest=hashlib.sha256()
    for key in sorted(data):
        digest.update(key.encode())
        if key=='meta':
            digest.update(json.dumps(data[key],sort_keys=True,separators=(',',':')).encode())
        else:
            array=np.ascontiguousarray(data[key])
            digest.update(array.dtype.str.encode())
            digest.update(str(array.shape).encode())
            digest.update(array.tobytes())
    return digest.hexdigest()
