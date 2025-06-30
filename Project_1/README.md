# ONGC Monthly Production Dashboard

A comprehensive desktop application for analyzing and visualizing ONGC (Oil and Natural Gas Corporation) monthly production data. This application provides an intuitive GUI interface for data analysis, visualization, and reporting of oil, gas, water, and condensate production volumes.

![ONGC Dashboard](ongc.png)

## Features

- **Interactive GUI**: Built with Tkinter for easy-to-use desktop interface
- **Data Visualization**: Matplotlib-powered charts and graphs for production analysis
- **CSV Data Processing**: Efficient handling of large production datasets
- **Multi-Product Analysis**: Support for oil, gas, water, and condensate volume tracking
- **Well-wise Analysis**: Individual well performance monitoring
- **Field-wise Reporting**: Production data aggregated by field
- **Export Capabilities**: Generate reports and export visualizations

## Requirements

- Python 3.7 or higher
- Required packages (see `requirements.txt`):
  - pandas >= 1.5.0
  - matplotlib >= 3.6.0
  - Pillow >= 9.0.0
  - numpy >= 1.20.0
  - openpyxl >= 3.0.0

## Installation

### Option 1: Automated Setup (Recommended)

#### For Windows:
```bash
# Run the setup batch file
setup.bat
```

#### For Python users:
```bash
# Run the setup script
python setup.py
```

### Option 2: Manual Installation

1. **Navigate to this project folder:**
   ```bash
   cd path/to/your/repo/ongc-production-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

#### Quick Start (Windows):
```bash
# Use the run script
run_dashboard.bat
```

#### Manual Start:
```bash
# Run directly with Python
python Monthly_Production.py
```

### Data Format

The application expects CSV data with the following columns:
- `WELL_NAME`: Name of the production well
- `REL_NAME`: Release name
- `UBHI`: Well identifier
- `STRING_NAME`: String configuration
- `FIELD`: Production field name
- `PRODUCTION_DATE`: Date of production (DD-MMM-YY format)
- `LAYER_NAME`: Geological layer
- `OIL_VOLUME`: Oil production volume
- `GAS_VOLUME`: Gas production volume
- `WATER_VOLUME`: Water production volume
- `CONDENSATE_VOLUME`: Condensate production volume
- `OIL_MASS`: Oil mass
- `GAS_MASS`: Gas mass
- `WATER_MASS`: Water mass
- `CONDENSATE_MASS`: Condensate mass
- `FLOWING_HOURS`: Number of flowing hours

### Sample Data

The repository includes sample production data in `Monthly_Production_Volume_Students.csv` for testing and demonstration purposes.

## Project Structure

```
ongc-production-dashboard/         # This project folder
├── Monthly_Production.py          # Main application file
├── Monthly_Production_Volume_Students.csv  # Sample data file
├── requirements.txt               # Python dependencies
├── setup.py                      # Setup script
├── setup.bat                     # Windows setup script
├── run_dashboard.bat             # Windows run script
├── logo.png                      # Application logo
├── ongc.png                      # ONGC logo/screenshot
├── README.md                     # This file
└── .gitignore                    # Git ignore rules (project-specific)
```

> **Note**: This project is designed to work as a standalone folder within a larger repository. All dependencies and configurations are self-contained within this directory.

## Features in Detail

### Data Analysis
- Load and process large CSV datasets
- Filter data by date, field, and well
- Calculate production statistics and trends

### Visualization
- Interactive charts and graphs
- Time-series analysis
- Comparative production analysis
- Export charts as images

### User Interface
- Splash screen with logo
- Intuitive menu system
- Data filtering and search capabilities
- Real-time chart updates

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all required packages are installed using `pip install -r requirements.txt`
2. **Data Loading Issues**: Verify that your CSV file follows the expected format
3. **Display Issues**: Make sure you have tkinter installed (usually comes with Python)

### Performance Tips

- For large datasets, consider filtering data by date range
- Close unused chart windows to free up memory
- Use the latest version of pandas for optimal performance

## License

This project is developed for ONGC production data analysis. Please refer to your organization's policies regarding data usage and distribution.

## Support

For technical support or questions about the application:
- Check the troubleshooting section above
- Review the sample data format
- Ensure all dependencies are properly installed

## Acknowledgments

- ONGC for production data standards
- Python community for excellent libraries
- Contributors to pandas, matplotlib, and tkinter projects
