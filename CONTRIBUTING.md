# Contributing to Clone Hero Video Forge

Thank you for your interest in contributing!  
Clone Hero Video Forge is an open-source project that welcomes improvements, bug reports, feature requests, and pull requests from the community.

This document explains how to contribute effectively and safely.

---

# 🧩 Ways You Can Contribute

### ✅ Report Bugs
If you find a bug, please open a **GitHub Issue** and include:
- Your OS version  
- Steps to reproduce  
- What you expected to happen  
- What actually happened  
- Debug Log output (if relevant)  
- Screenshots (optional but very helpful)

### 💡 Request Features
If you have an idea for improvement, open a Feature Request issue.  
Please describe:
- The problem the feature solves  
- How you imagine the UI should behave  
- Any examples or references  

### 🛠 Submit Pull Requests
We welcome code contributions of all sizes.

Before submitting:
1. **Check existing issues** to avoid duplicates  
2. **Create a new branch** for your work  
3. Test your changes thoroughly  
4. Run the app and ensure no regressions  
5. Include a description of what was changed and why  

---

# 🧪 Development Setup

### Clone the repo:
```
git clone https://github.com/Robot011011/CHVideoForge.git
cd CHVideoForge
```

### Create & activate a virtual environment:
```
python -m venv .venv
```

Windows:
```
.\.venv\Scriptsctivate
```

### Install dependencies:
```
pip install -r requirements.txt
```

Run the app:
```
python ch_video_gui.py
```

---

# 🧼 Code Style Guidelines

Please follow these conventions:

### ✔ Python style
- Use **PEP8** guidelines  
- Use clear variable names  
- Add comments when behavior isn’t obvious  
- Keep functions modular and readable  

### ✔ Git practices
- One logical change per commit  
- Write meaningful commit messages  
- Avoid committing large binaries  

### ✔ GUI considerations
- GUI must remain responsive (use threads for heavy tasks)  
- All long operations must update the progress bar  
- Avoid adding features that clutter the layout  

---

# 📁 Project Structure

```
Clone Hero Video Forge/
│
├── ch_video_gui.py            # Main GUI app
├── ch_video_tool.py           # Processing engine
├── README.md                  # Main documentation
├── USING_CLONE_HERO_VIDEO_FORGE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── requirements.txt
```

If you add new modules, please update this section accordingly.

---

# 🧷 Pull Request Checklist

Before opening a PR, confirm:

- [ ] The app runs without errors  
- [ ] ffmpeg processes complete normally  
- [ ] yt-dlp integration still works  
- [ ] UI remains responsive  
- [ ] No leftover temporary files  
- [ ] Windows EXE still builds (if applicable)  
- [ ] README or manual updated (if needed)  

---

# 🤝 Code of Conduct

Be respectful, constructive, and collaborative.  
We welcome contributors from all backgrounds and skill levels.

---

# 📬 Getting Help

If you need help with the codebase or want to discuss a feature before building it, feel free to:
- Open a GitHub issue  
- Start a discussion on the repository  
- Submit a draft PR for review  

---

Thank you for contributing to Clone Hero Video Forge!  
Together we make Clone Hero modding easier for everyone.

