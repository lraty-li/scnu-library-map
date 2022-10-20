
# 以图书馆地图上南下北，leaflet 以左上角为原点
from enum import Enum
import json

# console.log(map.unproject([-w, -h], map.getMaxZoom()-1))

mapImgWidth = 1789
mapImgHeight = 1971

latLangX = 223.625
latLangY = -246.375

features = {
    "type": "FeatureCollection",
    "features": [
    ]
}

# 设定每个书架长2，宽0.5 ，过道宽1 （实际上书架为自由拼凑有长有短，
shelfLength = 8
shelfWidth = 2
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
            [x - shelfWidth/2, y + shelfLength/2],
            [x - shelfWidth/2, y - shelfLength/2],
            [x + shelfWidth/2, y - shelfLength/2],
            [x + shelfWidth/2, y + shelfLength/2],
            # the first and last positions in a LinearRing of coordinates must be the same
            [x - shelfWidth/2, y + shelfLength/2],
        ]
    else:
        coordinates = [
            [x - shelfLength/2, y + shelfWidth/2],
            [x - shelfLength/2, y - shelfWidth/2],
            [x + shelfLength/2, y - shelfWidth/2],
            [x + shelfLength/2, y + shelfWidth/2],
            [x - shelfLength/2, y + shelfWidth/2],
        ]
    return [coordinates]


def getFeature(northWestName, southEastName, towards, x, y):
    return {
        "type": "Feature",
        "properties": {
            "northWestName": "{}".format(northWestName),
            "southEastName": "{}".format(southEastName),
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": getCoodinate(towards, x, y)
        }
    }


def getShelfOffsetX(offsetX, index):
    return offsetX + index * (shelfWidth + aisleWidth)

def zipNumbering(lList):
  index = 0
  zipped = []
  length = len(lList)
  if not length % 2 == 0:
    raise '书架编号长度非偶数'
  while(index < length-1):
    zipped.append([lList[index],lList[index+1]])
    index += 2
  return zipped 

def get_202_science_chinese():
    offsetX_202_science_chinese = latLangX * 0.115
    offsetY_202_science_chinese = latLangY * 0.75

    # 202 理科借阅
    # 24个书架

    # 每两个字符串左右代表一个书架的西东两面
    # todo 修正，东西面放入property
    row1ShelfNumbering = ["x703.1", " x21", " u", " tu983", " tu201.4", " ts972.122", " ts664.01-39", " tq150.1", " tn941.3", " tn919", " tn911.22", " tn643", " tn01", " tm13", " th-62", " tb472-39", " tb11", " s682.2", " s216.4", " r746.940.5", " r541.5", " r323.1",
                          " r212", " r151.3-62", " q959.1", " q945.4", " q78", " q2-49", " q-49", " p7-092", " p338", " p159-49", " o64-61", " o6-3", " o413.1", " o351.2", " o226", " o21", " o174.1", " o157", " o141.4", " o13", " o13", " o1-53", " o1", " n49", " n091-49", " n", ]
    zipped = zipNumbering(row1ShelfNumbering)

    for index in range(len(zipped)):
        features['features'].append(
            getFeature(
                zipped[index][0],
                zipped[index][1],
                Towards.NorthSouth,
                getShelfOffsetX(offsetX_202_science_chinese, index),
                offsetY_202_science_chinese
            )
        )
    # todo
    row2 = []


get_202_science_chinese()

with open('./data.js', 'w') as f:
    f.write("var features = {}".format(json.dumps(features)))
