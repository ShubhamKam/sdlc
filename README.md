# R&D AI Improvements Calculator

A comprehensive tool for calculating and visualizing the impact of AI implementation in software development processes. This application helps organizations assess the potential benefits, costs, and ROI of integrating AI into their R&D workflows.

## Features

- **Interactive SDLC Graph Visualization**
  - Visual representation of the Software Development Life Cycle
  - Customizable AI augmentation percentages for each process
  - Dynamic graph modification capabilities

- **AI Impact Calculator**
  - Team & Project Metrics analysis
  - Financial Parameters evaluation
  - AI Impact Metrics assessment
  - Efficiency Metrics calculation

- **Comprehensive Results**
  - Basic Metrics (Team Cost, AI Cost, Savings)
  - Investment Metrics (ROI, NPV, IRR)
  - Time Metrics (Cycle Time, Payback Period)
  - Productivity Metrics (Velocity, Features)
  - Additional Financial Metrics

- **Notes & Collaboration**
  - Persistent notes system
  - Email-based comment submission
  - Comment history tracking

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rd-ai-improvements.git
cd rd-ai-improvements
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Requirements

- Python 3.7+
- Streamlit
- NetworkX
- Pandas
- D3.js (included in the application)

## Usage

1. **SDLC Graph Visualization**
   - Use the sidebar controls to modify the graph
   - Add/delete/rename nodes
   - Set AI augmentation percentages
   - Modify connections between nodes

2. **AI Impact Calculator**
   - Input team and project metrics
   - Configure financial parameters
   - Set AI impact metrics
   - Calculate and analyze results

3. **Results Analysis**
   - View comprehensive metrics
   - Download results as CSV
   - Add notes and comments
   - Track historical calculations

## Project Structure

```
rd-ai-improvements/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── README.md          # Project documentation
└── .gitignore         # Git ignore file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Streamlit for the web application framework
- NetworkX for graph operations
- D3.js for visualization
- Pandas for data manipulation

## Contact

For any questions or suggestions, please open an issue in the repository.

---

Made with ❤️ for better R&D processes 