import os
from PIL import ImageGrab, Image
import pytesseract
import pyautogui
import pyperclip



def boundingBoxToTextArray(box: tuple[int,int,int,int]):
    textArr = []
    img = ImageGrab.grab(bbox=box)
    img = img.convert('L')
    img = img.point( lambda p: 255 if p < 128 else 0 )
    img = img.convert('1')
    text = pytesseract.image_to_string(img)
    textArr = list(filter(("").__ne__, text.split("\n")))
    return textArr

monsterPaths = os.listdir("monsterScreenshots")

monsterDict = {}
for path in monsterPaths:
    monsterDict[path[:-4]] = Image.open("monsterScreenshots\\"+path)
print(monsterPaths)

monsterBoundingBoxes = (
    (327, 631, 426, 750),
    (327, 750, 426, 856),
    (327, 856, 426, 966)
)
allMonsters = []
allNames = []
allLevels = []
for _ in range(10):
    for box in monsterBoundingBoxes:
        haystackImage = ImageGrab.grab(bbox=box)
        foundMonster = "???"
        for monster in monsterDict:
            try: 
                pyautogui.locate(monsterDict[monster],haystackImage, confidence=0.9)
            except pyautogui.ImageNotFoundException:
                pass
            else:
                foundMonster = monster
                break
        allMonsters.append(foundMonster)

    allNames += boundingBoxToTextArray((423,636,2073,970))
    allLevels += boundingBoxToTextArray((2082,636,2239,970))
    pyautogui.click(2442,661)

for i, levelString in enumerate(allLevels):
    levelString = levelString[3:]
    levelString = levelString.replace("l","1")
    levelString = levelString.replace("I","1")
    levelString = levelString.replace("t","1")
    levelString = levelString.replace("T","1")
    levelString = levelString.replace("o","0")
    levelString = levelString.replace("O","0")
    levelString = levelString.replace("?","7")
    allLevels[i] = levelString

pasteString = ""
print(len(allMonsters), len(allNames), len(allLevels))
print(allMonsters)
for i in range(len(allNames)):
    pasteString += f"{allMonsters[i]}\t{allNames[i]}\t{allLevels[i]}\n"

pyperclip.copy(pasteString)
