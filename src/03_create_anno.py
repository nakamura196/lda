import cv2
import numpy as np
import glob
import json
import urllib.request
import tempfile
import requests
import requests
import shutil

def imread_web(url):
    # 画像をリクエストする
    res = requests.get(url)
    img = None
    # Tempfileを作成して即読み込む
    with tempfile.NamedTemporaryFile(dir='./') as fp:
        fp.write(res.content)
        fp.file.seek(0)
        img = cv2.imread(fp.name)
    return img


def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

# files = glob.glob("/Users/nakamura/Dropbox/U-PARL_Moeller/input/*.jpg")
files = glob.glob("/Users/nakamura/git/nagai/input/*.jpg")

manifest = "https://diyhistory.org/public/omekas13/iiif/1/manifest"

res = urllib.request.urlopen(manifest)
# json_loads() でPythonオブジェクトに変換
data = json.loads(res.read())

canvases = data["sequences"][0]["canvases"]

result = {
    "@context": "http://www.w3.org/ns/anno.jsonld",
    "@graph": [
        
    ]
}

graphs = result["@graph"]

for i in range(len(canvases)):
    canvas = canvases[i]
    image_url = canvas["images"][0]["resource"]["@id"]
    print(image_url)

    file = "input.jpg"

    # download_img(image_url, file)

    img = cv2.imread(file)

    # BGR -> グレースケール
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # エッジ抽出 (Canny)
    edges = cv2.Canny(gray, 1, 100, apertureSize=3)
    cv2.imwrite('edges.png', edges)
    # 膨張処理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    edges = cv2.dilate(edges, kernel)
    # 輪郭抽出
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 面積でフィルタリング
    rects = []

    count = 0

    for cnt, hrchy in zip(contours, hierarchy[0]):
        if cv2.contourArea(cnt) < 60000:
            continue  # 面積が小さいものは除く
        if hrchy[3] == -1:
            continue  # ルートノードは除く
        # 輪郭を囲む長方形を計算する。
        rect = cv2.minAreaRect(cnt)
        rect_points = cv2.boxPoints(rect).astype(int)

        min_x = 100000
        min_y = 100000
        max_x = 0
        max_y = 0

        for i in range(len(rect_points)):
            print(rect_points[i])
            x = rect_points[i][0]
            y = rect_points[i][1]

            if min_x > x:
                min_x = x
            
            if min_y > y:
                min_y = y
            if max_x < x:
                max_x = x
            if max_y < y:
                max_y = y

        w = max_x - min_x
        h = max_y - min_y

        imgBox = img[min_y: max_y, min_x: max_x]
        imgBox = cv2.cvtColor(imgBox, cv2.COLOR_BGR2GRAY)

        thresh = 100
        max_pixel = 255
        ret, imgBox = cv2.threshold(imgBox,
                                    thresh,
                                    max_pixel,
                                    cv2.THRESH_BINARY)

        cnt = 0
        for x in range(0, imgBox.shape[0]):
            for y in range(0, imgBox.shape[1]):
                if imgBox[x, y] == 0:
                    cnt += 1

        
        cv2.imwrite('tmp/imgBox_'+str(count)+"_"+str(cnt)+".png", imgBox)
        count += 1

        if cnt > 1000:

            graphs.append({
                "target": image_url+"#xywh="+str(min_x)+","+str(min_y)+","+str(w)+","+str(h),
                "bodyValue": ""
            })

            rects.append(rect_points)

    # x-y 順でソート
    rects = sorted(rects, key=lambda x: (x[0][1], x[0][0]))

    # 描画する。
    for i, rect in enumerate(rects):
        color = np.random.randint(0, 255, 3).tolist()
        cv2.drawContours(img, rects, i, color, 50)
        cv2.putText(img, str(i), tuple(rect[0]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 3)

        # print('rect:\n', rect)

    cv2.imwrite("out.png", img)

fw = open("test.json", 'w')
json.dump(result, fw, ensure_ascii=False, indent=4,
          sort_keys=True, separators=(',', ': '))
