import cv2
import apriltag

print("[INFO] loading image...")
filename="dist/img/German_2024-06-09-14h32m_0001"
filename="dist/img/Pizza_2024-05-27-12h15m_0027"
# filename="dist/img/Starter_2024-06-09-11h01m_0170"
image = cv2.imread(f"{filename}.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print("[INFO] detecting AprilTags...")
options = apriltag.DetectorOptions(families="tag16h5", quad_decimate=4, quad_blur=2)
detector = apriltag.Detector(options)
results = detector.detect(gray)
print("[INFO] {} total AprilTags detected".format(len(results)))
# loop over the AprilTag detection results
for r in results:
	tagFamily = r.tag_family.decode("utf-8")
	print("[INFO] tag family: {}, id: {}".format(tagFamily, r.tag_id))
	# extract the bounding box (x, y)-coordinates for the AprilTag
	# and convert each of the (x, y)-coordinate pairs to integers
	(ptA, ptB, ptC, ptD) = r.corners
	print("[INFO] ptA[0]: {}, ptA[1]: {}".format(ptA[0],ptA[1]))
	print("[INFO] ptB[0]: {}, ptB[1]: {}".format(ptB[0],ptB[1]))
	print("[INFO] ptC[0]: {}, ptC[1]: {}".format(ptC[0],ptC[1]))
	print("[INFO] ptD[0]: {}, ptD[1]: {}".format(ptD[0],ptD[1]))
	ptA = (int(ptA[0]), int(ptA[1]))
	ptB = (int(ptB[0]), int(ptB[1]))
	ptC = (int(ptC[0]), int(ptC[1]))
	ptD = (int(ptD[0]), int(ptD[1]))

	# draw the bounding box of the AprilTag detection
	cv2.line(image, ptA, ptB, (0, 255, 0), 2)
	cv2.line(image, ptB, ptC, (0, 255, 0), 2)
	cv2.line(image, ptC, ptD, (255, 0, 0), 2)       # blue
	cv2.line(image, ptD, ptA, (255, 255, 0), 2)     # cyan
	# draw the center (x, y)-coordinates of the AprilTag
	(cX, cY) = (int(r.center[0]), int(r.center[1]))
	cv2.circle(image, (cX, cY), 10, (0, 0, 255), -1)
	# draw the tag family on the image
	cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# calc points for measurement window
w1 = results[0].corners[1][0] - results[0].corners[0][0]
w2 = results[0].corners[2][0] - results[0].corners[3][0]
w3 = results[1].corners[1][0] - results[1].corners[0][0]
w4 = results[1].corners[2][0] - results[1].corners[3][0]
h1 = results[0].corners[3][1] - results[0].corners[0][1]
h2 = results[0].corners[2][1] - results[0].corners[1][1]
h3 = results[1].corners[3][1] - results[1].corners[0][1]
h4 = results[1].corners[2][1] - results[1].corners[1][1]
w = max(w1, w2, w3, w4) / 6
print("[INFO] width: {}, ({}, {}, {}, {})".format(w,w1,w2,w3,w4))
print("[INFO] height: {}, {}, {}, {}".format(h1,h2,h3,h4))
ptA = (int(results[0].corners[0][0] - w*8), int(results[1].corners[0][1]))
ptB = (int(results[0].corners[0][0] - w*2), int(results[1].corners[0][1]))
ptC = (int(results[0].corners[0][0] - w*2), int(results[0].corners[3][1]))
ptD = (int(results[0].corners[0][0] - w*8), int(results[0].corners[3][1]))

# draw the bounding box of the AprilTag detection
cv2.line(image, ptA, ptB, (0, 255, 0), 2)
cv2.line(image, ptB, ptC, (0, 255, 0), 2)
cv2.line(image, ptC, ptD, (255, 0, 0), 2)       # blue
cv2.line(image, ptD, ptA, (255, 255, 0), 2)     # cyan

# show the output image after AprilTag detection
cv2.imwrite(f"{filename}-tagged.jpg", image)