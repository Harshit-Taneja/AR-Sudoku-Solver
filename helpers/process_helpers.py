import operator
import cv2
import numpy as np


def find_extreme_corners(polygon, limit_fn, compare_fn):
    section, _ = limit_fn(enumerate([compare_fn(pt[0][0], pt[0][1]) for pt in polygon]),
                          key=operator.itemgetter(1))

    return polygon[section][0][0], polygon[section][0][1]


def draw_extreme_corners(pts, original):
    cv2.circle(original, pts, 7, (0, 255, 0), cv2.FILLED)


def clean_helper(img):
    if np.isclose(img, 0).sum() / (img.shape[0] * img.shape[1]) >= 0.95:
        return np.zeros_like(img), False

    height, width = img.shape
    mid = width // 2
    if np.isclose(img[:, int(mid - width * 0.4):int(mid + width * 0.4)], 0).sum() / (2 * width * 0.4 * height) >= 0.90:
        return np.zeros_like(img), False

    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    x, y, w, h = cv2.boundingRect(contours[0])

    start_x = (width - w) // 2
    start_y = (height - h) // 2
    new_img = np.zeros_like(img)
    new_img[start_y:start_y + h, start_x:start_x + w] = img[y:y + h, x:x + w]

    return new_img, True


def grid_line_helper(img, shape_location, length=10):
    clone = img.copy()
    row_or_col = clone.shape[shape_location]
    size = row_or_col // length
    if shape_location == 0:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, size))
    else:
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, 1))
    clone = cv2.erode(clone, kernel)
    clone = cv2.dilate(clone, kernel)

    return clone


def draw_lines(img, lines):
    clone = img.copy()
    lines = np.squeeze(lines)

    for rho, theta in lines:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * a)
        cv2.line(clone, (x1, y1), (x2, y2), (255, 255, 255), 4)
    return clone
