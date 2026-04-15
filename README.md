# AIR CANVAS : A VIRTUAL DRAWING APP

A real-time virtual drawing application built using **OpenCV** and **Python** that allows users to draw on screen using a colored object captured via webcam — no physical surface needed.

---

##  Project Overview

This project uses computer vision techniques to track a colored object (marker) and enables users to draw on a virtual canvas in real time. The system detects the object based on **HSV color segmentation**, tracks its movement, and renders drawing strokes live on screen.

---

##  Features

- 🎥 Real-time webcam-based drawing
- 🎯 Color detection using HSV color space
- 🖌️ Multiple drawing colors:
  - Blue
  - Green
  - Red
  - Yellow
- 🧹 Clear canvas functionality
- 📌 Smooth drawing using `deque` data structure
- ⚡ Noise reduction using morphological operations

---

##  How It Works

1. Webcam captures live video frames
2. Frames are converted from **BGR → HSV** color space
3. A mask is created to detect the selected color
4. Noise is removed using:
   - Erosion
   - Dilation
   - Morphological Opening
5. Contours are detected from the mask
6. The **largest contour** is tracked as the drawing pointer
7. The center of the object is stored and used to draw continuous lines

---

##  Tech Stack

| Component | Details |
|-----------|---------|
| Language | Python |
| Core Library | OpenCV (`cv2`) |
| Numerical Computing | NumPy |
| Data Structure | Collections (`deque`) |

---

##  Project Structure

```
Virtual-Drawing-OpenCV/
│
├── air_canvas.py     # Main source code
└── README.md         # Project documentation
```

---

##  Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/virtual-drawing-opencv.git
cd virtual-drawing-opencv
```

### 2️⃣ Install Dependencies

```bash
pip install opencv-python numpy
```

### 3️⃣ Run the Project

```bash
python air_canvas.py
```

---

##  Controls

| Action | Description |
|--------|-------------|
| Move colored object | Draw on screen |
| Top-left button | Clear canvas |
| Color boxes | Change drawing color |
| Press `q` | Exit application |

---

##  HSV Trackbars

The application provides interactive trackbars to adjust:

- **Hue** — Select the color range to detect
- **Saturation** — Control color intensity
- **Value** — Adjust brightness threshold

This helps fine-tune color detection for different lighting conditions.

---

## 🖼️ Output Windows

| Window | Description |
|--------|-------------|
| **Live Drawing** | Displays real-time drawing feed |
| **Paint Window** | Canvas showing all drawn strokes |
| **Mask** | Binary image of the detected color region |

---

## 📌 Key Concepts Used

- 🖼️ Image Processing
- 🎨 Color Detection (HSV Color Space)
- 🔍 Contour Detection
- 🔧 Morphological Transformations
- 📹 Real-time Video Processing

---

## ⚡ Future Improvements

- ✋ Hand gesture drawing (without a colored object)
- 💾 Save drawing as an image file
- 🎨 Add more colors and adjustable brush sizes
- 🤖 Integrate AI-based object detection

---

## 👩‍💻 Author

**Kavya Sharma**
B.Tech CSE (AIML) | Aspiring AI/ML Engineer 🚀

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repository and improve the project by:

- Adding new features
- Improving performance
- Enhancing the UI

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgement

This project is inspired by real-world applications of **Computer Vision** and **OpenCV** in interactive and gesture-based systems.
