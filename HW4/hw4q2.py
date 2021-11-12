import sys

def read_overlaps(infile):
    BMR = {}
    BML = {}
    noBest = {}

    with open(infile, 'r') as fh:
        line = fh.readline()
        while line:
            readsAndLen = line.strip().split()
            firstID = readsAndLen[0]
            overlapLen = int(readsAndLen[1])
            secondID = readsAndLen[2]
            BMR[firstID] = [secondID, overlapLen]
            longestRepeat = 0
            if secondID in noBest:
                longestRepeat = noBest[secondID]
            if secondID not in noBest or overlapLen > longestRepeat:
                if secondID in BML:
                    currBest = BML[secondID]
                    currBestLen = int(currBest[1])
                    if overlapLen > currBestLen:
                        BML[secondID] = [firstID, overlapLen]
                    if overlapLen == currBestLen:
                        BML.pop(secondID)
                        if secondID in noBest and overlapLen > longestRepeat:
                            noBest[secondID] = overlapLen
                        if secondID not in noBest:
                            noBest[secondID] = overlapLen
                else:
                    BML[secondID] = [firstID, overlapLen]
            line = fh.readline()
        fh.close()
    return BMR, BML

def rightMatch(BMR, BML, left):
    if left in BMR:
        right = BMR[left][0]
        if right in BML:
            check = BML[right][0]
            if check == left:
                return "\n" + str(BML[right][1]) + " " + str(right), right
    return "", ""

def leftMatch(BMR, BML, right):
    if right in BML:
        left = BML[right][0]
        if left in BMR:
            check = BMR[left][0]
            if check == right:
                return str(left) + "\n" + str(BMR[left][1]) + " ", left
    return"",""


def make_unitigs(BMR, BML):
    unitigs = []
    keys = BMR.keys()
    unused = list(BMR.keys())
    for id in keys:
        if id in unused:
            unused.remove(id)
            unitig = id
            addition = False
            matchRight, rightID = rightMatch(BMR, BML, id)
            while matchRight:
                if rightID in unused:
                    unused.remove(rightID)
                unitig += matchRight
                matchRight, rightID = rightMatch(BMR, BML, rightID)
                addition = True
            matchLeft, leftID = leftMatch(BMR, BML, id)
            while matchLeft:
                if leftID in unused:
                    unused.remove(leftID)
                unitig = matchLeft + unitig
                matchLeft, leftID = leftMatch(BMR, BML, leftID)
                addition = True
            if addition is True:
                unitigs.append(unitig)
    return unitigs




if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]

    BMR, BML = read_overlaps(infile)
    unitigs = sorted(make_unitigs(BMR, BML))
    with open(outfile, 'w') as fh:
        fh.write("\n".join(unitigs))