#!/usr/bin/python3
import random
import paramiko
import time

from aiogram import Dispatcher, Bot

from db import Database

TOKEN = ""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


class Wg_Profile:
    def get_profile(user_id, TOKEN):

        bot = Bot(token=TOKEN)
        dp = Dispatcher(bot)

        db = Database('database.db')

        host = ''
        user = ''
        secret = ''
        port = 22

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client_id = user_id
        str_client_id = str(client_id)

        client.connect(hostname=host, port=port, username=user, password=secret)
        stdin, stdout, stderr = client.exec_command('wg genkey | tee /etc/wireguard/' + str_client_id + '_privatekey | '
                                                                                                        'wg pubkey | tee /etc/wireguard/' + str_client_id + '_publickey')
        print(stdout.read().decode())

        stdin, stdout, stderr = client.exec_command("cat /etc/wireguard/" + str_client_id + "_privatekey")
        for line in stdout:
            private_key = (line.strip('\n'))
        print("private_key: " + private_key)

        stdin, stdout, stderr = client.exec_command("cat /etc/wireguard/" + str_client_id + "_publickey")
        for line in stdout:
            global publick_key
            public_key = (line.strip('\n'))
        print("publick_key: " + public_key)


        if db.get_ip_musk_4() < 256:
            ip_mask_4 = db.get_ip_musk_4() + 1
            db.set_ip_mask_4(ip_mask_4)
            ip_mask_3 = db.get_ip_musk_3()
            ip_mask = "10" + ".0" + "." + str(ip_mask_3) + "." + str(ip_mask_4)
        else:
            db.set_ip_mask_4(0)
            ip_mask_4 = db.get_ip_musk_4()
            ip_mask_3 = db.get_ip_musk_3()
            ip_mask_3 = ip_mask_3 + 1
            db.set_ip_mask_3(ip_mask_3)
            ip_mask = "10" + ".0" + "." + str(ip_mask_3) + "." + str(ip_mask_4)


        db.set_ip_mask_user(ip_mask, user_id)

        server_public_key = "XXXXXPublicKey_SERVER"

        my_file = open(str_client_id + ".conf", "w+")
        my_file.write("[Interface]\nPrivateKey = " + private_key + "\nAddress = " + ip_mask + "/32" + "\nDNS = 8.8.8.8"
                      + "\n[Peer]" + "\nPublicKey = " + server_public_key + "\nEndpoint = 88.210.12.3:51830"
                      + "\nAllowedIPs = 0.0.0.0/0\nPersistentKeepalive = 20\n\n")
        my_file.close()



        ftp_client = client.open_sftp()
        my_file = open("wg0.conf", "a+")
        user_id = str(user_id)
        my_file.write("\n###" + user_id + " \n[Peer]\nPublicKey = " +  public_key + "\nAllowedIPs = " + ip_mask + "/32\n")


        db.set_publick_key_user(user_id, public_key)






        my_file.close()
        ftp_client.close()

        ftp_client = client.open_sftp()
        ftp_client.put('wg0.conf', '/etc/wireguard/wg0.conf')
        ftp_client.put(str_client_id + '.conf', '/root/clients/' + str_client_id + '.conf')
        stdin, stdout, stderr = client.exec_command("systemctl restart wg-quick@wg0")

        ftp_client.close()
        client.close()
        stdin.close()



