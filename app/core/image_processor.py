import cv2
import numpy as np
import matplotlib.pyplot as plt


letters = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

def process_image(input):
    img = cv2.imread(input)
    h, w, rgb = img.shape
    ratio = h / w
    h = 2134
    img = cv2.resize(img, (int(h / ratio), h))

    """NAME"""

    basex = 410
    endx = (img.shape[0] // 2) - 60
    basey = 170
    segments = []

    for i in range(25):
        temp = img[basex:endx, basey + 32 * i : basey + 32 * (i + 1)]
        temp = cv2.resize(temp, (32, 598))
        segments.append(temp)

    name = ""
    for segment in segments:
        index = []
        list_ = []
        for i in range(26):
            mark = segment[23 * i : 23 * (i + 1), :]
            for j in range(3):
                mark = np.mean(mark, axis=2 - j)
            list_.append(mark)
            index.append(i)

        list_, index = zip(*sorted(zip(list_, index)))
        if list_[1] - list_[0] >= 50:
            name += letters[index[0]]
        else:
            name += " "

    """OMR questions"""

    basex = (img.shape[0] // 2) + 20
    basey = 160
    segments = []

    for j in range(5):
        for i in range(20):
            temp = img[
                basex + 46 * i : basex + 46 * (i + 1),
                basey + 250 * j : basey + 250 * (j + 1),
            ]
            segments.append(temp)

    # Preprocess the image
    segment_contours = []
    for segment in segments:
        gray = cv2.cvtColor(segment, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        segment_contours.append(contours)

    final_contour = []  # jo mark kara hai
    for i, contour in enumerate(segment_contours):
        index = []
        list_ = []
        ind = 0
        for j, box in enumerate(contour):
            area = cv2.contourArea(box)  # area nikal liya
            list_.append(area)
            index.append(j)

        list_, index = zip(
            *sorted(zip(list_, index), reverse=True)
        )  # sorts 2 list same time
        if list_[0] - list_[1] <= 150:
            ind = index[1]
        else:
            ind = index[0]

        final_contour.append(contour[ind])
        mask = np.zeros(segments[i].shape, np.uint8)
        cv2.drawContours(mask, [contour[ind]], -1, 255, -1)
        colour = (0, 0, 255)
        cv2.drawContours(segments[i], [contour[ind]], -1, colour, 1)

    #plt.figure()
    #plt.imshow(segments[i])

    responses = []
    for i, contour in enumerate(final_contour):
        avg = 0
        count = 0
        for coords in contour:
            avg += np.mean(coords, axis=1)
            count += 1
        avg /= count
        if 40 <= avg <= 60:
            #print("Question", i + 1, ": A")
            responses.append(f"Question {i + 1}: A")
        elif 60 < avg <= 80:
            #print("Question", i + 1, ": B")
            responses.append(f"Question {i + 1}: B")
        elif 80 < avg <= 100:
            #print("Question", i + 1, ": C")
            responses.append(f"Question {i + 1}: C")
        elif 100 < avg:
            #print("Question", i + 1, ": D")
            responses.append(f"Question {i + 1}: D")
    
    return name.strip(), responses
