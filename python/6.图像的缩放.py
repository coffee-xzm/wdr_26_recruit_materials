import cv2 

img = cv2.imread("D://111.png")
# 方式2：按比例缩放（fx=水平比例，fy=垂直比例）

scale = 0.5  
# 缩小为原图的50%
resized2 = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

# 显示结果
cv2.imshow("Original", img)
cv2.imshow("Resized (50%)", resized2)
cv2.waitKey(0)
cv2.destroyAllWindows()
