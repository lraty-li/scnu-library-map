
# 以图书馆地图上南下北，全图左下角为原点。
from enum import Enum
import json

features = {
    "type": "FeatureCollection",
    "features": [
    ]
}

# 设定每个书架长2m，宽0.5m ，过道宽1m （实际上书架为自由拼凑有长有短，
shelfLength = 2
shelfWidth = 0.5
aisleWidth = 1


class Towards(Enum):
    NorthSouth = True
    WestEast = False

# towards : 书架朝向， True 南北 ， False 西东


def getCoodinate(towards, x, y):
    coordinates = []
    if towards == Towards.NorthSouth:
        # left top, lb,  rb, rt  Polygons and MultiPolygons should follow the right-hand rule
        coordinates = [
            [(x - shelfWidth)/2, (y + shelfLength)/2],
            [(x - shelfWidth)/2, (y - shelfLength)/2],
            [(x + shelfWidth)/2, (y - shelfLength)/2],
            [(x + shelfWidth)/2, (y + shelfLength)/2],
            # the first and last positions in a LinearRing of coordinates must be the same
            [(x - shelfWidth)/2, (y + shelfLength)/2],
        ]
    else:
        coordinates = [
            [(x - shelfLength)/2, (y + shelfWidth)/2],
            [(x - shelfLength)/2, (y - shelfWidth)/2],
            [(x + shelfLength)/2, (y - shelfWidth)/2],
            [(x + shelfLength)/2, (y + shelfWidth)/2],
            [(x - shelfLength)/2, (y + shelfWidth)/2],
        ]
    return [coordinates]


def getFeature(name, towards, x, y):
    return {
        "type": "Feature",
        "properties": {
            "name": "{0}".format(name),
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": getCoodinate(towards, x, y)
        }
    }


# 202 理科借阅
# 24个书架

# 每两个字符串左右代表一个书架的西东两面
row1ShelfNumbering = ["x703.1", " x21", " u", " tu983", " tu201.4", " ts972.122", " ts664.01-39", " tq150.1", " tn941.3", " tn919", " tn911.22", " tn643", " tn01", " tm13", " th-62", " tb472-39", " tb11", " s682.2", " s216.4", " r746.940.5", " r541.5", " r323.1",
                      " r212", " r151.3-62", " q959.1", " q945.4", " q78", " q2-49", " q-49", " p7-092", " p338", " p159-49", " o64-61", " o6-3", " o413.1", " o351.2", " o226", " o21", " o174.1", " o157", " o141.4", " o13", " o13", " o1-53", " o1", " n49", " n091-49", " n", ]
row1ShelfCount = len(row1ShelfNumbering)

offsetX = 10
offsetY = 10


def getShelfOffsetX(index):
    return offsetX + index * (shelfWidth + aisleWidth)


for index in range(row1ShelfCount):
    features['features'].append(
        getFeature(
            row1ShelfNumbering[index], Towards.NorthSouth, getShelfOffsetX(index), offsetY)
    )

with open('./temp.json', 'w') as f:
    f.write(json.dumps(features))


# ?个书架
row2 = []
