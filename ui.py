# Tiffany Ng
# tcng2@uci.edu
# 52892812

from os import path
from pathlib import Path
import shlex
from Profile import Profile, Post, DsuFileError, DsuProfileError
import ds_client

current_profile = None
current_file = None
admin_mode = False
DSP_port = 3001


def main():
    print("Welcome to your Journal entry!")
    home_user_input = input(
        "Would you like create like to create a new profile, "
        "open an existing profile, or Admin? (C/O/Admin): ")
    if home_user_input == "Admin" or home_user_input == "admin":
        global admin_mode
        admin_mode = True
        while True:
            command_input = input()
            try:
                command_split = shlex.split(command_input)
                if not command_split:
                    continue
                if command_split[0] == "Q":
                    print("Program has ended.")
                    break
                elif command_split[0] == "C":
                    create(command_split)
                elif command_split[0] == "D":
                    delete(command_split)
                elif command_split[0] == "R":
                    read(command_split)
                elif command_split[0] == "O":
                    open_file(command_split)
                elif command_split[0] == "E":
                    edit(command_split)
                elif command_split[0] == "P":
                    print_file(command_split)
                else:
                    print("ERROR")
            except ValueError:
                print("ERROR")
                continue
    elif home_user_input == "C":
        path = input("Enter directory path: ")
        name = input("Enter file name: ")
        create(["C", path, "-n", name])
        if current_profile is not None and current_file is not None:
            journal()
    elif home_user_input == "O":
        path = input("Enter file path: ")
        open_file(["O", path])
        if current_profile is not None and current_file is not None:
            journal()
    else:
        print("ERROR")


def journal():
    while True:
        print("1. Edit username")
        print("2. Edit password")
        print("3. Edit Bio")
        print("4. Add post")
        print("5. Delete post")
        print("6. Print all posts")
        print("7. Print a specific post")
        print("8. Quit")

        choice = input("Enter your choice (#): ")
        if choice == "1":
            new_username = input("Enter new username: ")
            edit(["E", "-usr", new_username])
        elif choice == "2":
            new_password = input("Enter new password: ")
            edit(["E", "-pwd", new_password])
        elif choice == "3":
            new_bio = input("Enter new bio: ")
            if new_bio.strip() == "":
                print("ERROR")
                continue
            edit(["E", "-bio", new_bio])
            post_bio = input("Publish bio online? (y/n): ")
            if post_bio == "y":
                if current_profile is not None and current_file is not None:
                    try:
                        current_profile.load_profile(current_file)
                    except (DsuProfileError, DsuFileError):
                        print("ERROR")
                        return
                    if current_profile.dsuserver is not None:
                        if not ds_client.send(current_profile.dsuserver,
                                              DSP_port,
                                              current_profile.username,
                                              current_profile.password,
                                              "Updating bio",
                                              new_bio):
                            print("Failed to post to DSP server.")
                    else:
                        print("No DSP server associated with this profile.")
                else:
                    print("ERROR")     

        elif choice == "4":
            new_post = input("Enter new post: ")
            edit(["E", "-addpost", new_post])
            online_post = input("Would you like to post this to your DSP account? (y/n): ")
            if online_post == "y":
                if current_profile is not None and current_file is not None:
                    try:
                        current_profile.load_profile(current_file)
                    except (DsuProfileError, DsuFileError):
                        print("ERROR")
                        return
                    if current_profile.dsuserver is not None:
                        if not ds_client.send(current_profile.dsuserver,
                                              DSP_port,
                                              current_profile.username,
                                              current_profile.password,
                                              "Updating bio",
                                              new_post):
                            print("Failed to post to DSP server.")
                    else:
                        print("No DSP server associated with this profile.")
                else:
                    print("ERROR")
        elif choice == "5":
            post_id = input("Enter post ID to delete: ")
            edit(["E", "-delpost", post_id])
        elif choice == "6":
            print_file(["P", "-posts"])
        elif choice == "7":
            post_id = input("Enter post ID to print: ")
            print_file(["P", "-post", post_id])
        elif choice == "8":
            print("Exiting journal. Goodbye!")
            break
        else:
            print("ERROR")


def create(line):
    global current_profile
    global current_file
    global admin_mode


    if len(line) != 4 or line[2] != "-n":
        print("ERROR")
        return

    new_line = [line[0]]
    new_line.append(" ".join(line[1:-2]))
    file_name = line[-1]
    path = Path(new_line[1])

    if len(new_line) == 2:
        if not path.exists() or not path.is_dir():
            print("ERROR")
        else:
            full_path = path / (file_name + ".dsu")

            if full_path.exists():
                open_file(["O", str(full_path)])
                return
            else:
                full_path.touch()
                print(full_path)
                if not admin_mode:
                    username = input("Username: ")
                    password = input("Password: ")
                    bio = input("Bio: ")
                else:
                    username = input()
                    password = input()
                    bio = input()
                if (' ' in username or username == ""
                        or ' ' in password or password == ""):
                    print("ERROR: Username or password cannot"
                          " contain spaces or be empty.")
                    return
                current_profile = Profile()
                current_profile.username = username
                current_profile.password = password
                current_profile.bio = bio
                server = input("DSP Server (127.0.0.1): ")
                if server.strip() == "":
                    server = "127.0.0.1"
                current_profile.dsuserver = server 
                current_file = str(full_path)
                try:
                    current_profile.save_profile(str(full_path))
                except DsuFileError:
                    print("ERROR")
    else:
        print("ERROR")


def open_file(line):
    global current_profile
    global current_file

    new_line = [line[0]]
    new_line.append(" ".join(line[1:]))
    path = Path(new_line[1])

    if len(new_line) == 2:
        if path.exists() and path.suffix == ".dsu":
            try:
                current_profile = Profile()
                current_profile.load_profile(str(path))
                current_file = str(path)
                print(current_file,
                      "Profile loaded! Username:",
                      current_profile.username,
                      "Bio:", current_profile.bio)
            except (DsuProfileError, DsuFileError):
                print("ERROR")
        else:
            print("ERROR")
    else:
        print("ERROR")


def edit(line):
    global current_profile
    global current_file
    if current_profile is None or current_file is None:
        print("ERROR")
        return

    # validate everything first before changing anything
    i = 1
    while i < len(line):
        if line[i] in ("-usr", "-pwd", "-bio", "-addpost", "-delpost"):
            if i + 1 >= len(line):
                print("ERROR")
                return
            if line[i] == "-usr" and (' ' in line[i+1] or line[i+1] == ""):
                print("ERROR")
                return
            if line[i] == "-pwd" and (' ' in line[i+1] or line[i+1] == ""):
                print("ERROR")
                return
            if line[i] == "-delpost":
                try:
                    int(line[i+1])
                except ValueError:
                    print("ERROR")
                    return
            i += 2
        else:
            print("ERROR")
            return

    # now apply all changes
    i = 1
    while i < len(line):
        if line[i] == "-usr":
            current_profile.username = line[i + 1]
            i += 2
        elif line[i] == "-pwd":
            current_profile.password = line[i + 1]
            i += 2
        elif line[i] == "-bio":
            current_profile.bio = line[i + 1]
            i += 2
        elif line[i] == "-addpost":
            if line[i + 1].strip() != "":
                current_profile.add_post(Post(line[i + 1]))
            i += 2
        elif line[i] == "-delpost":
            if not current_profile.del_post(int(line[i + 1])):
                print("ERROR")
                return
            i += 2

    try:
        current_profile.save_profile(current_file)
    except DsuFileError:
        print("ERROR")


def print_file(line):
    global current_profile
    global current_file

    if current_profile is None or current_file is None:
        print("ERROR")
        return
    try:
        current_profile.load_profile(current_file)
    except (DsuProfileError, DsuFileError):
        print("ERROR")
        return
    i = 1
    while i < len(line):
        if line[i] == "-usr":
            print("Username:", current_profile.username)
            i += 1
        elif line[i] == "-pwd":
            print("Password:", current_profile.password)
            i += 1
        elif line[i] == "-bio":
            print("Bio:", current_profile.bio)
            i += 1
        elif line[i] == "-posts":
            if i + 1 < len(line):
                print("ERROR")
                return
            posts = current_profile.get_posts()
            for id_number in range(len(posts)):
                print(f"ID {id_number}: {posts[id_number].entry}")
            i += 1
        elif line[i] == "-post":
            posts = current_profile.get_posts()
            if i + 1 < len(line):
                try:
                    index = int(line[i + 1])
                    if 0 <= index < len(posts):
                        print(posts[index].entry)
                        i += 2
                    else:
                        print("ERROR")
                        return
                except ValueError:
                    print("ERROR")
                    return
            else:
                print("ERROR")
                return
        elif line[i] == "-all":
            print("Username:", current_profile.username)
            print("Password:", current_profile.password)
            print("Bio:", current_profile.bio)
            posts = current_profile.get_posts()
            for post in posts:
                print(post.entry)
            i += 1
        else:
            print("ERROR")
            return


def delete(line):
    new_line = [line[0]]
    new_line.append(" ".join(line[1:]))
    path = Path(new_line[1])
    if len(new_line) == 2:
        if not path.exists():
            print("ERROR")
        else:
            if path.suffix == ".dsu":
                path.unlink()
                print(new_line[1], "DELETED")
            else:
                print("ERROR")
    else:
        print("ERROR")


def read(line):
    new_line = [line[0]]
    new_line.append(" ".join(line[1:]))
    path = Path(new_line[1])
    if len(new_line) == 2:
        if path.exists() and path.suffix == ".dsu":
            info = path.read_text()
            if info.strip() == "":
                print("EMPTY")
            else:
                print(info, end="")
        else:
            print("ERROR")
    else:
        print("ERROR")


if __name__ == "__main__":
    main()
