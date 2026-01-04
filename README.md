CramIt — Personal Planner (PyQt6)
=================================

A lightweight, local-first planner desktop app using PyQt6 with professional MVC architecture. Built for learning and extending with clean, modular code.

## Features

- ✅ **Activity Management**: Create, edit, delete activities with start/end times
- ✅ **Smart Tracking**: Automatic duration calculation, execution status toggle
- ✅ **Categories**: Work, school, hobbies, or custom types
- ✅ **Calendar View**: Integrated calendar widget for date visualization
- ✅ **Analytics**: Summary statistics and activity tracking
- 🔄 **Hub Views**: Week/Month/Year views with progress graphs (planned)
- 🔄 **Advanced Scheduling**: Optimizer for fitting activities into free slots (planned)
- 🔄 **Cloud Sync**: Optional Google Calendar integration (planned)

## Quick Start

### Installation

1. **Create and activate a virtual environment** (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

On Linux / macOS:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Run the application**:

```bash
python CramITApp.py
```

## Project Structure

```
CramIt/
├── CramITApp.py              # ⭐ Main entry point
├── models.py                 # Activity data model
├── storage.py                # JSON persistence
├── dialogs.py                # UI dialogs
├── controllers/              # Business logic (MVC Controller)
├── ui/                       # Main window (MVC View)
├── widgets/                  # Reusable UI components
├── doc/                      # Comprehensive documentation
└── test/                     # Test files and lessons
```

The application follows **MVC (Model-View-Controller)** architecture for clean separation of concerns and maintainability.

## Documentation

Comprehensive documentation in the `doc/` directory:

- **[doc/PROJECT_STRUCTURE.md](doc/PROJECT_STRUCTURE.md)**: Detailed project structure and setup guide
- **[doc/ARCHITECTURE.md](doc/ARCHITECTURE.md)**: Visual architecture diagrams and design patterns
- **[doc/CODE_GUIDE.md](doc/CODE_GUIDE.md)**: Developer quick reference and common tasks
- **[doc/FEATURES.md](doc/FEATURES.md)**: Feature specifications and data model
- **[doc/LEARNING.md](doc/LEARNING.md)**: Step-by-step learning roadmap

## Data Storage

All data is stored locally by default:
- **Windows**: `%USERPROFILE%\.cramit\activities.json`
- **Linux/Mac**: `~/.cramit/activities.json`

## Architecture Highlights

- **MVC Pattern**: Clean separation between UI, logic, and data
- **Observer Pattern**: Automatic UI updates when data changes
- **Modular Design**: Each component has a single responsibility
- **Professional Structure**: Industry-standard organization with proper packages
## Data Storage

All data is stored locally by default:
- **Windows**: `%USERPROFILE%\.cramit\activities.json`
- **Linux/Mac**: `~/.cramit/activities.json`

## Architecture Highlights

- **MVC Pattern**: Clean separation between UI, logic, and data
- **Observer Pattern**: Automatic UI updates when data changes
- **Modular Design**: Each component has a single responsibility
- **Professional Structure**: Industry-standard organization with proper packages

## Development

### Adding Features

1. **Model Changes**: Update `models.py` and `storage.py`
2. **Business Logic**: Extend or create controllers in `controllers/`
3. **UI Changes**: Update `ui/main_window.py` or add widgets to `widgets/`
4. **Dialogs**: Modify or extend `dialogs.py`

See [doc/CODE_GUIDE.md](doc/CODE_GUIDE.md) for detailed developer guidance.

### Code Quality

- Follow PEP 8 style guidelines
- Add docstrings to classes and public methods
- Keep MVC separation clean
- Test locally before committing

## Roadmap

Based on the learning path in [doc/LEARNING.md](doc/LEARNING.md):

- ✅ **Lessons 1-2**: Environment setup, basic UI, data model, MVC architecture
- 🔄 **Lesson 5**: Enhanced calendar views with activity display
- 🔄 **Lesson 6**: Analytics panel with charts
- 🔄 **Lesson 7**: Scheduler/optimizer algorithm
- 🔄 **Lesson 8**: Optional Google Calendar sync
- 🔄 **Lesson 9**: Packaging and distribution

## Contributing

This is a learning project! Contributions and suggestions are welcome.

When contributing:
1. Maintain the MVC architecture
2. Update documentation if structure changes
3. Test thoroughly before submitting
4. Add comments explaining complex logic

## License

Personal learning project. Feel free to use as reference or starting point for your own projects.

## Support

For questions or issues:
1. Check the documentation in `doc/`
2. Review the code organization in [doc/ARCHITECTURE.md](doc/ARCHITECTURE.md)
3. See [doc/LEARNING.md](doc/LEARNING.md) for the learning path

