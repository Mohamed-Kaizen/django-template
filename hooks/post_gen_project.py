#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import secrets
import shutil
import string
import subprocess
from typing import Dict, List


DOCS_SOURCES = "docs_sources"

ALL_TEMP_FOLDERS = [DOCS_SOURCES, "licenses"]
ALL_TEMP_Files = []

DOCS_FILES_BY_TOOL = {
    "mkdocs": [
        "index.md",
        "css",
        "js",
        "api",
        "overrides",
        "/mkdocs.yml"
    ],
}


def get_random_string(
    *,
    length: int = 50,
    allowed_chars: str = f"{string.ascii_letters}{string.digits}",
) -> str:
    """
    Return a securely generated random string.
    """
    return "".join(secrets.choice(allowed_chars) for i in range(length))


def create_git_repo() -> None:
    try:
        subprocess.call(["git", "init", "-q"])
        os.rename("git_ignore", ".gitignore")

    except Exception as error:
        print(error)


def create_env_file() -> None:
    env_file = f"""DEBUG=True
SECRET_KEY={get_random_string()}
ALLOWED_HOSTS={{cookiecutter.domain_name}}, localhost, 0.0.0.0, 127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
EMAIL_USER={{cookiecutter.email}}
EMAIL_PASSWORD=''
"""
    if "{{cookiecutter.use_sentry}}" == "y":
        env_file = env_file + "SENTRY_DSN=''\n"

    if "{{cookiecutter.use_redis}}" == "y":
        env_file = env_file + "REDIS_URL=''\n"

    if "{{cookiecutter.production_storage}}" == "Dropbox":
        env_file = env_file + "DROPBOX_OAUTH2_TOKEN=''\n"

    if "{{cookiecutter.production_storage}}" in ["MinIO", "Amazon S3"]:
        env_file = env_file + "AWS_ACCESS_KEY_ID=''\nAWS_SECRET_ACCESS_KEY=''\n"

    if "{{cookiecutter.production_storage}}" == "MinIO":
        env_file = env_file + "MinIO_URL=''"

    if "{{cookiecutter.app_type}}" != "plain django":
        env_file = env_file + "CORS_ALLOWED_ORIGINS=''\n"

    if "{{cookiecutter.app_type}}" == "django rest framework with firebase auth":
        env_file = env_file + "FIREBASE_PROJECT_ID=''\nFIREBASE_PRIVATE_KEY_ID=''\nFIREBASE_PRIVATE_KEY=''\nFIREBASE_CLIENT_EMAIL=''\nFIREBASE_CLIENT_ID=''\nFIREBASE_CLIENT_X509_CERT_URL=''"

    with open(".env", "w") as file:
        file.write(env_file)


def move_docs_files(
    *, docs_tool: str, docs_files: Dict[str, List[str]], docs_sources: str
) -> None:
    if docs_tool == "none":
        return None

    root = os.getcwd()
    docs = "docs"

    if not os.path.exists(docs):
        os.mkdir(docs)

    for item in docs_files[docs_tool]:
        dst, name = (root, item[1:]) if item.startswith("/") else (docs, item)
        src_path = os.path.join(docs_sources, docs_tool, name)
        dst_path = os.path.join(dst, name)

        if os.path.exists(dst_path):
            os.unlink(dst_path)

        os.rename(src_path, dst_path)


def remove_temp_files_folders(*, temp_folders: List[str], files) -> None:
    for folder in temp_folders:
        shutil.rmtree(folder)

    for file in files:
        os.remove(file)


def drf_check() -> None:
    """List of check to make sure if drf are been used."""
    if "{{cookiecutter.app_type}}" != "django rest framework with dj-rest-auth":
        ALL_TEMP_Files.append("users/adapter.py")

    if "{{cookiecutter.app_type}}" != "django rest framework with firebase auth":
        ALL_TEMP_Files.append("users/authentication.py")

    if "{{cookiecutter.app_type}}" not in [
        "django rest framework with dj-rest-auth",
        "django rest framework with firebase auth",
    ]:
        ALL_TEMP_Files.append("users/serializers.py")


if __name__ == "__main__":
    move_docs_files(
        docs_tool="{{cookiecutter.docs_tool}}",
        docs_files=DOCS_FILES_BY_TOOL,
        docs_sources=DOCS_SOURCES,
    )

    if "{{cookiecutter.text_editor}}" != "vscode" and "{{cookiecutter.text_editor}}" != "both":
        ALL_TEMP_FOLDERS.append(".vscode")

    if "{{cookiecutter.deployment}}" != "heroku":
        ALL_TEMP_Files.append("Procfile")

    drf_check()
    remove_temp_files_folders(temp_folders=ALL_TEMP_FOLDERS, files=ALL_TEMP_Files)
    create_env_file()
    create_git_repo()
