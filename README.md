# TheSimDiary 
## ✈️ About 
**TheSimDiary** is a streamlined desktop companion for flight simulation enthusiasts. With an intuitive interface, it centralizes everything you need to enhance and track your virtual flying experience.

## 📷 User Interface 
<img width="1512" alt="Screenshot 2025-06-06 at 12 54 35 PM" src="https://github.com/user-attachments/assets/71b7bf53-4104-4222-8c6b-290704686041" />
<img width="1512" alt="Screenshot 2025-06-06 at 12 55 53 PM" src="https://github.com/user-attachments/assets/e95e076f-6dfc-4371-a947-f8d3c6742242" />

## 🌟 Features 
- Log individual flights with detailed information
- Track technical faults specific to mods and flight simulators
- View real-time METAR weather reports
- Access essential platforms and tools for realistic flight simulation
- Visualize your logged flight data with interactive summaries and charts
- Organized, user-friendly interface for smooth navigation and use

## 📚 Instructions 
Click and download the latest release of the application from the release tab on the right of the GitHub page when available. 
Run the file appropriate to your machine (.exe for Windows and .pkg for macOS) and the app is yours to discover.

## ⚠️ Notice on Application Signing and Security 

**TheSimDiary** is currently distributed **without a code-signing certificate**, which means that operating systems like **Windows** and **macOS** may warn you when launching the application for the first time.

This is **not because the application is unsafe**, but simply because it hasn't yet been signed with a verified developer license. Signing certificates can be costly for independent developers, but obtaining one is **on the roadmap** as the project grows.

I assure you of the following:

- ✅ **No personal or usage data is collected** — your logs and data stay completely local on your system.  
- ✅ The application is built in Python with open-source libraries, and the **source code is made available** for full transparency.  
- ✅ You can inspect the code and verify its behavior yourself.  

**To run the application:**

- On **Windows**, click **"More Info" → "Run Anyway"** when the Windows Defender warning appears.  
- On **macOS**, go to **System Preferences → Security & Privacy**, and allow the app manually after the first attempt.  

I appreciate your understanding and support as this project grows into something officially signed and verified.

## 🤓 Development Insights
- **Developed in Python** using **PyQt5** for a responsive and modern desktop UI  
- **CSS** used for custom styling of UI components  
- **Pandas** and **Matplotlib** for data processing, summaries, and visualizations  
- **NOAA Weather API** integrated to fetch real-time **METAR** data  
- **METAR library** used to parse and summarize weather reports  
- **Haversine module** to calculate distances between coordinates  
- **CSV-based storage** for:
  - Flight logs and fault reports  
  - **Airport data** (location, ICAO, etc.)  
  - **Aircraft data** (model, type, performance characteristics)

## 🐞 Known Issues & Feedback
### Known Issues:
- Delay in opening Weather Tab

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
