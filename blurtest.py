import cv2
import time
import easyocr
import matplotlib.pyplot as plt

def to_gray(img):
    if len(img.shape) == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def laplacian_variance(img):
    gray = to_gray(img)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def ocr_success(img, target_words):
    results = reader.readtext(img)
    detected_text = " ".join([res[1] for res in results]).lower()
    detected_words = detected_text.split()
    print("OCR output:", detected_words)
    for target_word in target_words:
        if target_word.lower() not in detected_words:
            answer = False
            return answer
    answer = True
    return answer

reader = easyocr.Reader(['en'], gpu=True)
cap = cv2.VideoCapture(0)
checking_sharpness = False
started_check = False
start_time=time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    #give the user have six seconds to center the image
    if not checking_sharpness and time.time() - start_time >= 6:
        print("Starting sharpness check...")
        checking_sharpness = True

    #once program enters check sharpness phase use laplacian variance to take a clear image and have option to exit program
    if checking_sharpness == True:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        variance = laplacian.var()
        
        cv2.putText(
            frame,
            f"Sharpness: {variance:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )
        if variance > 135:
            cv2.imwrite("working_image.jpg",frame)
            print("image captured") 
            print(frame.shape) 
            break

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

image = cv2.imread("working_image.jpg")
cv2.imshow("Target Object", image)
kernel_sizes = [1,3,5]
lap_vals = []
success_vals = []   
target_words = ["blue", "lizard", "50", "sensitive"]

for k in kernel_sizes:
    blurred = cv2.GaussianBlur(image, (k, k), 0)
    lap = laplacian_variance(blurred)
    success = ocr_success(blurred, target_words)
    lap_vals.append(lap)
    if success == True:
        success_vals.append(True)
    else:
        success_vals.append(False)

    print(f"Blur k={k:2d} | LapVar={lap:.2f} | OCR Success={success}")

plt.figure()
plt.plot(kernel_sizes, lap_vals, marker='o')
plt.xlabel("Gaussian Blur Kernel Size")
plt.ylabel("Laplacian Variance")
plt.title("Effect of Blur on Image Sharpness")
plt.grid(True)
plt.show()

