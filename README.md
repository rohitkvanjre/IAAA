# IAAA – Intelligent Attendance Automation with AI 👨‍🏫🎯

> Built with ❤️ by [Rohit K](https://github.com/rohitkvanjre)

A full-stack AI-based face recognition attendance system that automates and streamlines classroom attendance using real-time video processing and a smart React dashboard. It eliminates manual efforts, supports time-based attendance checks, and generates downloadable attendance reports.




## 📂 Repository

🔗 [GitHub Repository](https://github.com/rohitkvanjre/IAAA)

---

## 📌 Features

- Real-time face recognition using InsightFace and dlib
- Automated attendance every 10 minutes per class hour
- Final attendance based on majority interval presence
- SQLite database with auto-finalization logic
- ReactJS-based dashboard for faculty login and attendance report download
- Embedding storage in local folders for faster lookups
- Export attendance in Excel or CSV format by class/date

---

## 🛠️ Tech Stack

### ✅ Python & Back-End (FastAPI + Face Recognition)
- `Python 3.9.x`
- `FastAPI`, `Uvicorn`
- `face_recognition`, `dlib`, `InsightFace`, `OpenCV`
- `SQLAlchemy`, `SQLite`
- `Pandas`, `Pillow`, `Numpy`

### ✅ Front-End (React)
- `React 18`, `React Router`
- `Tailwind CSS`, `MUI`, `Bootstrap`
- `Axios`, `XLSX`, `file-saver`

---

## 💻 System Requirements

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.9.x | Compatible with dlib & face_recognition |
| pip | Latest | Use `python -m ensurepip --upgrade` |
| CMake | 3.22+ | Required for dlib |
| Visual Studio Build Tools | Required | For dlib compilation on Windows |
| SQLite DB Browser | Optional | GUI to explore `.db` |
| Git | Latest | Version control |
| Node.js | v16.x / v18.x | For React |
| npm | v8.x / v9.x | React dependencies |
| Jupyter Notebook | Optional | Manual testing of recognition |

---

## 📦 Backend `requirements.txt`

```txt
fastapi==0.95.2
uvicorn==0.22.0
face_recognition==1.3.0
opencv-python==4.7.0.72
dlib==19.24.0
numpy==1.23.5
pandas==1.5.3
pillow==9.4.0
insightface==0.7.3
sqlalchemy==1.4.49
python-multipart==0.0.6
