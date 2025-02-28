# ChatGPT-Text-Comprehensor

A ChatGPT clone that is specilized in text comprehension. Written with Flask and HTML.

## Requirements
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [OpenAI Python API Library](https://pypi.org/project/openai/)
- [OpenAI API keys](https://platform.openai.com/api-keys)

## General Installation
```
git clone https://github.com/Peter-YeungPW/ChatGPT-Text-Comprehensor.git
```

## Library Installation
```
pip install flask dotenv openai
```

## Setting Credentials

Create .env file with the following content:

```
API_KEY=<your-api-key>
```

If you want to use Azure OpenAI API, also specify the following in the .env file.

```
AZURE_ENDPOINT=<azure-endpoint-url>
API_VERSION=<azure-endpoint-api-version>
```

## Author
[@Peter-YeungPW](https://github.com/Peter-YeungPW)

## License
[MIT License](LICENSE)
