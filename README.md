# TheSimDiary 
## ✈️ About 
TheSimDiary is a simple, focused desktop app built for flight sim enthusiasts. It helps you log flights, track progress, and keep everything in one place, so you can spend more time flying and less time organizing.

## 📷 User Interface 
![image](https://github.com/user-attachments/assets/f9941693-2a6d-4f75-9b63-12e44dfe8c5e)
<img width="1512" alt="Screenshot 2025-06-13 at 6 03 28 PM" src="https://github.com/user-attachments/assets/ca7dfebe-f0cd-4420-aab1-8dd0493cd754" />

## 🌟 Features 
- Log individual flights with detailed information
- Track technical faults specific to mods and flight simulators
- View real-time METAR weather reports
- Access essential platforms and tools for realistic flight simulation
- Visualize your logged flight data with interactive summaries and charts
- Organized, user-friendly interface for smooth navigation and use

## 📚 Instructions 
Click and download the latest release of the application from the release tab on the right of the GitHub page when available. 
Run the file appropriate to your machine (.exe for Windows and .dmg for macOS) and the app is yours to discover.

## ⚠️ Notice on Application Signing and Security 

**TheSimDiary** is currently distributed **without a code-signing certificate**, which means that operating systems like **Windows** and **macOS** may warn you when launching the application for the first time.

This is **not because the application is unsafe**, but simply because it hasn't yet been signed with a verified developer license. Signing certificates can be costly for independent developers, but obtaining one is **on the roadmap** as the project grows.

I assure you of the following:

- ✅ **No personal or usage data is collected** — your logs and data stay completely local on your system.  
- ✅ The application is built in Python with open-source libraries, and the **source code is made available** for full transparency.  
- ✅ You can inspect the code and verify its behavior yourself. The binaries are only provided for user convenience.

**To run the application:**

- On **Windows**, click **"More Info" → "Run Anyway"** when the Windows Defender warning appears.  
- On **macOS**, go to **System Preferences → Security & Privacy**, and allow the app manually after the first attempt.  

I appreciate your understanding and support as this project grows into something officially signed and verified.

## 🤓 Development Insights and Credits
- **Developed in Python** using **PyQt5** for a responsive and modern desktop UI  
- **CSS** used for custom styling of UI components  
- **Pandas** and **Matplotlib** for data processing, summaries, and visualizations  
- **NOAA Weather API** integrated to fetch real-time **METAR** data  
- **METAR library** used to parse and summarize weather reports  
- **Haversine module** to calculate distances between coordinates  
- **CSV-based storage** for:
  - Flight logs and fault reports  
  - **Airport data** (location, ICAO, etc.) from [here](https://github.com/datasets/airport-codes)
  - **Aircraft data** (model, type, performance characteristics) from [here](https://github.com/rikgale/ICAOList)

## 🐞 Known Issues & Feedback

### Feedback
As TheSimDiary is still in active development, you may encounter **unexpected behavior or minor bugs** during usage. Your experience and feedback are extremely valuable in helping improve the app.

If you run into any issues, please don’t hesitate to:

- Report the problem using the [**Issues**](https://github.com/Faizaan-Nasir/TheSimDiary/issues) tab on our GitHub page
- Include any relevant details such as:
  - What you were doing when the issue occurred
  - Any error messages (if visible)
  - Screenshots or log excerpts if possible

I am actively monitoring reports and will aim to address them as quickly as possible.

Thank you for being part of the development journey!

## 🤝 Contributing

TheSimDiary is an open and growing project, and contributions from developers like you are very welcome!

Whether you want to:

- Fix bugs  
- Add new features  
- Improve documentation  
- Suggest ideas or enhancements  

Here’s how you can help:

1. **Fork** the repository  
2. **Create a new branch** for your changes  
3. **Commit** your improvements with clear messages  
4. **Open a Pull Request** for review  

Your involvement helps make TheSimDiary better for everyone—thank you for considering contributing!

## 🚀 Upcoming Features

- Sharing summarized flight data through images on Social Media platforms.
