"""
Provides the commands `create()` for making a string form of the XML files and
`write()` for writing them to files.
"""

from . import hex

__all__ = ['create_xml', 'write_xml', 'create_hex', 'write_hex']

_XML_PREAMBLE = '<?xml version="1.0" encoding="utf-8"?><Experiment>'
_XML_EPILOGUE = '<Pulse Laser397B1="off" Laser397B2="off" Laser729="off" Laser854="off" Laser729RF1="off" Laser729RF2="off" Laser854POWER="off" Laser854FREQ="off" LaserAux1="off" LaserAux2="off" Type="Stop" Ticks="0" TargetLength="0" Name="Stop" /></Experiment>'

def create_xml(elements, base_args={}):
    """
    Make a string of XML representing the pulse sequence `elements`.

    Arguments --
    elements: seq.Element or iterable of seq.Element --
        The elements in the sequence.  This may often just be a single `Loop`
        element.
    base_args: dict --
        The base argument dictionary to use, which must fill in any loose
        variables which are not defined by loops.
    """
    try:
        body = "".join([e.xml(base_args) for e in elements])
    except TypeError:
        body = elements.xml(base_args)
    return "".join([_XML_PREAMBLE, body, _XML_EPILOGUE])

def write_xml(file, elements, base_args={}):
    """
    Write out an XML file which can be loaded by the Spectroscopy Controller
    pulse sequence designer.

    Arguments --
    file: str --
        The file name to write out to.
    elements: seq.Element or iterable of seq.Element --
        The elements in the sequence.  This may often just be a single `Loop`
        element.
    base_args: dict --
        The base argument dictionary to use, which must fill in any loose
        variables which are not defined by loops.
    """
    str = create_xml(elements, base_args)
    with open(file, "w") as f:
        print(str, file=f)

def create_hex(elements, base_args={}):
    try:
        body = b"".join([e.hex(base_args) for e in elements])
    except TypeError:
        body = elements.hex(base_args)
    return body + hex.STOP

def write_hex(file, elements, base_args={}):
    with open(file, "wb") as f:
        f.write(create_hex(elements, base_args))