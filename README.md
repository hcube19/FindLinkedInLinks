# FindLinkedInLinks

## Project Description
 Automates LinkedIn founder verification from a CSV using Selenium and OpenAI GPT-5. Searches, scrapes, and confirms founder-company links, saving verified profiles to CSV. Modular, configurable, and built for professional, maintainable workflows.

## Features
- Google search automation for LinkedIn profiles
- Human-like browsing with Selenium
- LLM-based profile verification (OpenAI GPT-5)
- Modular codebase for easy maintenance
- Configurable input/output and prompt files
- Professional logging and error handling


## Project Structure
```
FindLinkedInLinks/
├── .venv_linkedin/           # Python virtual environment (not tracked by git)
├── config/
│   └── config.py             # User-editable configuration (input/output paths, API key, etc.)
├── data/
│   └── Founders.csv          # Input data (list of founders)
├── prompts/
│   └── llm_prompt.txt        # LLM prompt template
├── results/                  # Output folder for verified profiles
├── src/
│   ├── main.py               # Entry point for running the workflow
│   ├── workflow.py           # Orchestrates the workflow
│   ├── scraper.py            # Web scraping and Selenium logic
│   ├── llm.py                # LLM prompt and verification logic
│   └── io_utils.py           # CSV and file I/O utilities
├── requirements.txt          # Python dependencies
├── .gitignore                # Git ignore file
└── README.md                 # Project documentation
```

## Setup Instructions

### 1. Clone the repository
```sh
git clone https://github.com/hcube19/FindLinkedInLinks.git
cd FindLinkedInLinks
```

### 2. Create and activate a virtual environment
```sh
python3 -m venv .venv_linkedin
source .venv_linkedin/bin/activate
```

### 3. Install dependencies
```sh
pip install -r requirements.txt
```

### 4. Install SSL certificates (macOS only)
Selenium and Chrome may require valid SSL certificates to work properly on macOS. Find and run the Install Certificates.command script that comes with your Python installation. For example:
```sh
open "/Applications/Python <version>/Install Certificates.command"
```
This step ensures that Python and Selenium can access HTTPS websites without SSL errors.


### 5. Configure the project
- Copy the example config file and edit it with your actual OpenAI API key:
	```sh
	cp config/config.example.py config/config.py
	# Then open config/config.py and set your OpenAI API key and any other settings
	```
- Place your input data in `data/Founders.csv` (see below for format).
- Edit `prompts/llm_prompt.txt` to customize the LLM prompt if needed.


## How to Run the Main Script

Activate your virtual environment if not already active:
```sh
source .venv_linkedin/bin/activate
```

**Run the program from the project root using the `-m` flag:**
```sh
python -m src.main
```
This ensures Python treats the `src` folder as a package and all imports work correctly. Do not run `python src/main.py` directly, as this may cause import errors.

## Example Input/Output

### Input: `data/Founders.csv`
| Founder Name | Startup      | Title         |
|--------------|--------------|---------------|
| Alice Smith  | TechStars    | CEO           |
| Bob Jones    | InnovateNow  | CTO           |

### Output: `results/Verified_Founders.csv`
| Name         | Company      | LinkedIn                                      |
|--------------|-------------|------------------------------------------------|
| Alice Smith  | TechStars   | https://www.linkedin.com/in/alicesmith123      |

## Notes
- The script will prompt you to manually solve CAPTCHAs or log in to Google/LinkedIn if required.
- All logs and errors are output to the console for transparency.
- The OpenAI API key is stored in `config/config.py` for convenience.

## Troubleshooting
- If you encounter SSL or certificate errors, make sure you have run the certificate installation command above.
- If Chrome or Selenium fails to launch, ensure Chrome is installed and up to date.
- For any issues with dependencies, re-run `pip install -r requirements.txt` in your virtual environment.

---

For further questions or improvements, feel free to open an issue or contribute!

## License & Use

This project is licensed under the **PolyForm Noncommercial License 1.0.0**.  
**Noncommercial only:** You may use, modify, and share the software for any **noncommercial** purpose.  
For **commercial** licensing, contact: [your-email@example.com].

See the full license text in [`LICENSE`](./LICENSE) and at:
https://polyformproject.org/licenses/noncommercial/1.0.0/

## Third-Party Terms

This project uses the following libraries via `pip` (not redistributed in this repo). Each is governed by its own license:

- **Selenium** — Apache-2.0  
- **OpenAI Python client (`openai`)** — Apache-2.0  
- **pandas** — BSD-3-Clause  
- **beautifulsoup4** — MIT  
- **python-dotenv** — BSD-3-Clause  
- **chromedriver-autoinstaller** — MIT

See [`THIRD_PARTY_LICENSES.md`](./THIRD_PARTY_LICENSES.md) for links/attribution and [`NOTICE`](./NOTICE) for Apache-2.0 notices.

## OpenAI API

This tool uses the OpenAI API. By using it, **you must supply your own API key** and **agree to OpenAI’s terms and policies**.  
- Terms of Use: https://openai.com/policies/row-terms-of-use/  
- Usage Policies: https://openai.com/policies/usage-policies/

Configure your OpenAI API key in `config/config.py` (see `config/config.example.py`).

## Compliance Notes (Important)

- **Google Search:** Automated queries and scraping of Google Search may violate Google’s Terms of Service. Use this tool responsibly. Consider using an official search API instead.  
- **LinkedIn:** Automated scraping/automation on LinkedIn is prohibited by LinkedIn’s rules. Access only publicly available pages and comply with their policies.  
- **Privacy:** Do not submit sensitive or personal data without a lawful basis. If you process personal data, comply with applicable privacy laws (e.g., GDPR). See `docs/LEGAL_COMPLIANCE.md` for details.
