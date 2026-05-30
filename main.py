import os
import socket
import threading
from queue import Queue

banner = """
=========================================
        SUMANTH EXPLOITS TOOLKIT
   Cybersecurity Research & Lab Utility
=========================================
"""

# Detect rockyou.txt automatically
def detect_rockyou():
    paths = [
        "/usr/share/wordlists/rockyou.txt",
        "/usr/share/wordlists/rockyou.txt.gz"
    ]

    for p in paths:
        if os.path.exists(p):
            return p

    return None


# Wordlist password check
def wordlist_check():
    usernames = input("Enter usernames (comma separated): ").split(",")
    password = input("Enter password to search: ")

    wordlist = detect_rockyou()

    if wordlist:
        print("[+] rockyou detected:", wordlist)
    else:
        wordlist = input("Enter wordlist path: ")

    try:
        with open(wordlist, "r", encoding="latin-1") as f:
            for line in f:
                p = line.strip()

                if p == password:
                    print("\n[SUCCESS] Password found")
                    for u in usernames:
                        print("Username:", u.strip(), "| Password:", p)
                    return

        print("[FAILED] Password not found")

    except:
        print("Error reading wordlist")


# Threaded port scanner
def port_scanner():

    target = input("Enter target IP: ")
    start = int(input("Start port: "))
    end = int(input("End port: "))

    queue = Queue()

    def scan():
        while not queue.empty():
            port = queue.get()

            try:
                s = socket.socket()
                s.settimeout(1)
                s.connect((target, port))
                print("[OPEN]", port)
                s.close()
            except:
                pass

            queue.task_done()

    for port in range(start, end + 1):
        queue.put(port)

    for _ in range(50):
        t = threading.Thread(target=scan)
        t.daemon = True
        t.start()

    queue.join()
    print("Scan complete")


# Wordlist info
def wordlist_info():

    wordlist = detect_rockyou()

    if wordlist:
        print("Detected:", wordlist)
    else:
        wordlist = input("Enter wordlist path: ")

    try:
        with open(wordlist, "r", encoding="latin-1") as f:
            count = sum(1 for _ in f)

        print("Total passwords:", count)

    except:
        print("Unable to read file")


# Main menu
def main():

    while True:

        os.system("clear")
        print(banner)

        print("1. Wordlist Password Check")
        print("2. Detect rockyou wordlist")
        print("3. Wordlist Info")
        print("4. Threaded Port Scanner")
        print("5. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            wordlist_check()

        elif choice == "2":
            path = detect_rockyou()

            if path:
                print("rockyou found:", path)
            else:
                print("rockyou not found")

        elif choice == "3":
            wordlist_info()

        elif choice == "4":
            port_scanner()

        elif choice == "5":
            break

        else:
            print("Invalid option")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
