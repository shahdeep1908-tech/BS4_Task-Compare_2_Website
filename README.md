# Blog Utils

## Prerequisites

### Technology

* Python 3.8.10
* Google Chrome 108.0.5359.124 or later

## Table of contents

- Creating virtual environment
- Installing requirements
- Configuration (Setting env file)
- Execute the project

## 1. Create Virtual Environment

```console
    sudo apt install python3-virtualenv
```

```console
    virtualenv blog_utils_env
```

```console
    source blog_utils_env/bin/activate
```

## 2. Install the requirements.txt file

* Go to the project directory.

```console
    cd blog-utils/
```

* Check if the requirements.txt file exists.

```console
    ls
```

* Install the project requirements packages and modules.

```console
    pip install -r requirements.txt
```

## 3. Setting up .env file

* Open the Source Project Directory.
* Find the .env file in the project blog-utils.
* Open the file in your text editor.
* Replace YOUR_SYSTEM_JIDIPI_EMAIL_ID with your email-id and YOUR_SYSTEM_JIDIPI_PASSWORD with your password and let all
  remain as it is.
* Save the file

## 4. Project Execution

```console
     python main.py
```

## Usage

1. When the programme starts, the localhost (127.0.0.1:8000) link will redirect you to the Home page, where the two URLs
   are compared (Blog URL & JIDIPI URL).
2. In addition, there is a Data Division By Parts feature; clicking on it will take you to another page where you can
   enter your blog URL and it will divide the data into parts, from which you can copy the text. 
