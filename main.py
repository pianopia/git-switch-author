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
    return {}

def save_profiles(profiles):
    """プロファイル設定をファイルに保存する"""
    with open(profiles_file, "w") as file:
        json.dump(profiles, file, indent=4)

def switch_git_profile(profile_name, profiles):
    """指定されたプロファイルにGitの設定を変更する"""
    profile = profiles.get(profile_name)
    if profile is None:
        print(f"指定されたプロファイルが見つかりません: {profile_name}")
        return
    subprocess.run(["git", "config", "--local", "user.email", profile["email"]], check=True)
    subprocess.run(["git", "config", "--local", "user.name", profile["name"]], check=True)
    print(f"プロファイル '{profile_name}' に切り替えました: {profile['name']} <{profile['email']}>")

def add_profile(profiles):
    """新しいプロファイルを追加する"""
    name = input("プロファイル名: ")
    email = input("メールアドレス: ")
    user_name = input("ユーザー名: ")
    profiles[name] = {"email": email, "name": user_name}
    save_profiles(profiles)
    print(f"プロファイル '{name}' を追加しました。")

def list_profiles(profiles):
    """プロファイルの一覧を表示する"""
    if profiles:
        print("登録されたプロファイルの一覧:")
        for name, profile in profiles.items():
            print(f"- {name}: {profile['name']} <{profile['email']}>")
    else:
        print("登録されたプロファイルはありません。")

def main():
    parser = argparse.ArgumentParser(description="Gitプロファイル管理ツール")
    parser.add_argument("-s", "--switch", help="切り替えるGitプロファイル名")
    parser.add_argument("-a", "--add", action="store_true", help="新しいプロファイルを追加")
    parser.add_argument("-l", "--list", action="store_true", help="プロファイルの一覧を表示")
    args = parser.parse_args()

    profiles = load_profiles()

    if args.add:
        add_profile(profiles)
    elif args.switch:
        switch_git_profile(args.switch, profiles)
    elif args.list:
        list_profiles(profiles)
    else:
        parser.print_help()

main()

