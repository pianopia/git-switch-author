#!/usr/bin/env python3
import argparse
import subprocess
import json
import os

# プロファイル設定ファイルのパス
profiles_file = "git_profiles.json"

def load_profiles():
    """プロファイル設定をファイルから読み込む"""
    if os.path.exists(profiles_file):
        with open(profiles_file, "r") as file:
            return json.load(file)
    else:
        return {}

def save_profiles(profiles):
    """プロファイル設定をファイルに保存する"""
    with open(profiles_file, "w") as file:
        json.dump(profiles, file, indent=4)

def switch_git_profile(profile_name, profiles):
    """指定されたプロフィールにGitの設定を変更する"""
    profile = profiles.get(profile_name)
    if profile is None:
        print(f"指定されたプロフィールが見つかりません: {profile_name}")
        return

    # Gitコマンドを実行してユーザー名とメールアドレスを設定
    subprocess.run(["git", "config", "--local", "user.email", profile["email"]], check=True)
    subprocess.run(["git", "config", "--local", "user.name", profile["name"]], check=True)
    print(f"プロファイル '{profile_name}' に切り替えました: {profile['name']} <{profile['email']}>")

def add_profile(profiles):
    """新しいプロファイルを対話式で追加"""
    name = input("プロファイル名: ")
    email = input("Email: ")
    user_name = input("ユーザー名: ")

    profiles[name] = {"email": email, "name": user_name}
    save_profiles(profiles)
    print(f"プロファイル '{name}' を追加しました。")


def main():
    profiles = load_profiles()
    parser = argparse.ArgumentParser(description="Gitプロファイル切り替えツール")
    parser.add_argument("-a", "--add", action="store_true", help="新しいプロファイルを追加")
    parser.add_argument("profile", nargs="?", help="切り替えるGitプロファイル名", default="")
    args = parser.parse_args()

    if args.add:
        add_profile(profiles)
    elif args.profile:
        switch_git_profile(args.profile, profiles)
    else:
        parser.print_help()

main()
