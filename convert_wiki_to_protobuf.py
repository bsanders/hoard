import hoard_pb2
from collections import namedtuple

def read_hoard_database():
    a = open('infile.txt').read()
    WikiItem = namedtuple('WikiItem', ['id', 'name', 'description', 'abilities', 'source', 'owner'])
    parsed_items = [WikiItem(*list(map(str.strip,line[2:-2].split('||')))) for line in a.splitlines() if line]
    hrd = hoard_pb2.Hoard(
                campaign=hoard_pb2.Name(name="Dalelands")
                )

    for i in parsed_items:
        hi = hrd.items.add(
                inventory_number=int(i.id),
                name=i.name,
                description=i.description,
                source=i.source,
                owner=i.owner,
                )

        for ability in i.abilities.split(';'):
            ha = hi.abilities.add()
            ab = ability.strip()
            if ab.startswith(('http://', 'https://')):
                ha.url = ab
                ha.function = ab.rstrip('/').split('/')[-1]
            else:
                ha.function = ab
            ha.identified = False
    return hrd
