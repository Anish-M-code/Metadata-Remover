
import enum
import importlib
from typing import Dict, Optional, Union

# A set of extension that aren't supported, despite matching a supported mimetype
UNSUPPORTED_EXTENSIONS = {
    '.asc',
    '.bat',
    '.brf',
    '.c',
    '.h',
    '.ksh',
    '.pl',
    '.pot',
    '.rdf',
    '.srt',
    '.wsdl',
    '.xpdl',
    '.xsd',
    '.xsl',
    }

DEPENDENCIES = {
    'Mutagen': {
        'module': 'mutagen',
        'required': True,
    },
}


def check_dependencies() -> Dict[str, Dict[str, bool]]:
    ret = dict()  # type: Dict[str, dict]

    for key, value in DEPENDENCIES.items():
        ret[key] = {
            'found': True,
            'required': value['required'],
        }
        try:
            importlib.import_module(value['module'])  # type: ignore
        except ImportError:  # pragma: no cover
            ret[key]['found'] = False


    return ret


@enum.unique
class UnknownMemberPolicy(enum.Enum):
    ABORT = 'abort'
    OMIT = 'omit'
    KEEP = 'keep'
