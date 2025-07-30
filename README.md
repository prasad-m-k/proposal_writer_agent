
# python3 --version
Python 3.13.5
# pip3 --version
pip 25.1.1 from /opt/homebrew/lib/python3.13/site-packages/pip (python 3.13)

# cd /Users/deepamk/OneDrive/source/ai-agents/proposal_writer_agent/
# ls -l

### If necessary remove old environment
## rm -rf venv/
# python3 -m venv venv
# ls -l
# source venv/bin/activate
(venv) bash-3.2$ pip list
Package Version
------- -------
pip     25.1.1
(venv) bash-3.2$ pip install pandas
Successfully installed numpy-2.3.2 pandas-2.3.1 python-dateutil-2.9.0.post0 pytz-2025.2 six-1.17.0 tzdata-2025.2
(venv) bash-3.2$ pip install python-dotenv
Successfully installed python-dotenv-1.1.1
(venv) bash-3.2$ 
(venv) bash-3.2$ pip install google-generativeai
Successfully installed annotated-types-0.7.0 cachetools-5.5.2 certifi-2025.7.14 charset_normalizer-3.4.2 google-ai-generativelanguage-0.6.15 google-api-core-2.25.1 google-api-python-client-2.177.0 google-auth-2.40.3 google-auth-httplib2-0.2.0 google-generativeai-0.8.5 googleapis-common-protos-1.70.0 grpcio-1.74.0 grpcio-status-1.71.2 httplib2-0.22.0 idna-3.10 proto-plus-1.26.1 protobuf-5.29.5 pyasn1-0.6.1 pyasn1-modules-0.4.2 pydantic-2.11.7 pydantic-core-2.33.2 pyparsing-3.2.3 requests-2.32.4 rsa-4.9.1 tqdm-4.67.1 typing-extensions-4.14.1 typing-inspection-0.4.1 uritemplate-4.2.0 urllib3-2.5.0
(venv) bash-3.2$ pip install  Flask
Successfully installed Flask-3.1.1 blinker-1.9.0 click-8.2.1 itsdangerous-2.2.0 jinja2-3.1.6 markupsafe-3.0.2 werkzeug-3.1.3
(venv) bash-3.2$ pip install python-docx
Successfully installed python-docx-1.2.0
$ pandoc "TRUSD conv.docx"  -o proposal.txt
$ pip install markdown pdfkit