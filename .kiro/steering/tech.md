# Technology Stack

## Language & Runtime
- **Python 3.x** - Core language
- **OpenCV** (`cv2`) - Computer vision library (imported but not actively used)
- **NumPy** - Numerical computing support

## Dependencies
```python
import cv2
import numpy as np
from typing import List, Tuple
import copy
```

## Architecture Patterns
- **Object-Oriented Design**: Separate classes for puzzle representation and solving
- **Strategy Pattern**: Multiple solver implementations (basic backtracking vs constraint propagation)
- **Immutable Operations**: Deep copying for backtracking states

## Common Commands

### Running the Application
```bash
python main.py
```

### Development Setup
```bash
# Install dependencies
pip install opencv-python numpy

# Run with Python 3
python3 main.py
```

## Code Style Guidelines
- Use type hints for function parameters and return values
- Follow PEP 8 naming conventions (snake_case for functions/variables)
- Document complex algorithms with inline comments
- Use descriptive variable names (e.g., `is_greater`, `candidates`)