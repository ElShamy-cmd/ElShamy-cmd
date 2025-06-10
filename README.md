# Stable Diffusion Projects Monorepo

This monorepo contains multiple related projects for Stable Diffusion development and deployment.

## Project Structure

```
.
├── apps/                    # Application projects
│   ├── milk/               # Milk application
│   │   ├── src/           # Source code
│   │   ├── tests/         # Test files
│   │   └── README.md      # Project-specific documentation
│   ├── milk-homepage/     # Milk homepage application
│   │   ├── src/
│   │   ├── tests/
│   │   └── README.md
│   └── stable-diffusion/  # Stable Diffusion project
│       ├── src/
│       ├── tests/
│       └── README.md
├── packages/               # Shared packages and libraries
│   ├── common/            # Common utilities and shared code
│   └── config/            # Shared configuration
├── docs/                  # Documentation
├── scripts/              # Build and deployment scripts
└── .github/             # GitHub workflows and templates
```

## Development Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project-Specific Setup

Each project in the `apps/` directory has its own README with specific setup instructions.

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

[Your License Here] 