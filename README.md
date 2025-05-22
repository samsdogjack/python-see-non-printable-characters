# See Non-Printable Characters (Python Version)

This is a Python/Flask web application that displays non-printable Unicode characters in a string.  
It is a transpiled version of the original PHP tool by [BurninLeo](https://github.com/BurninLeo/see-non-printable-characters).

## Features

- Paste any string and visualize hidden or non-printable Unicode characters.
- Counts characters and bytes.
- No data is stored or logged.

## Running Locally

### Prerequisites

- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)
- (Recommended) Create and activate a virtual environment:
  ```sh
  python3 -m venv venv
  source venv/bin/activate
  ```

### Install dependencies

```sh
pip install -r requirements.txt
```

### Run the app

```sh
python app.py
```

The app will start on [http://127.0.0.1:5000](http://127.0.0.1:5000).  
Open this URL in your browser.

## License

- The original code is © 2021 BurninLeo and licensed under the MIT License (see `LICENSE`).
- Python transpilation and modifications © 2025 samsdogjack, licensed under the MIT License (see `LICENSE.transpiled_code`).

## Credits

- Original PHP version: [BurninLeo/see-non-printable-characters](https://github.com/BurninLeo/see-non-printable-characters)