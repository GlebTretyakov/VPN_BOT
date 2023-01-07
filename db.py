import sqlite3
import time


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))

    def set_promo_sub(self, user_id, promo):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `promo` = ? WHERE `user_id` = ?", (promo, user_id,))

    def set_wg_profile_status(self, user_id, wg_profile):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `wg_profile` = ? WHERE `user_id` = ?",
                                       (wg_profile, user_id,))

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def set_time_sub(self, user_id, time_sub):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time_sub` = ? WHERE `user_id` = ?", (time_sub, user_id,))

    def get_time_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])
            return time_sub

    def get_wg_profile_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `wg_profile` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                wg_profile = int(row[0])
            return wg_profile

    def get_promo_sub(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `promo` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                promo_sub = int(row[0])
            return promo_sub

    def get_sub_status(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                time_sub = int(row[0])

            if time_sub > int(time.time()):
                return True
            else:
                return False

    def get_ip_musk_4(self):  # Получение из БД ip маски подсети четвертого октета
        with self.connection:
            result = self.cursor.execute("SELECT `mask_ip` FROM `mask_ip` WHERE `octet` = 4", ).fetchall()
            for row in result:
                ip_mask_4 = int(row[0])
            return ip_mask_4

    def get_ip_musk_3(self):  # Получение из БД ip маски подсети третьего октета
        with self.connection:
            result = self.cursor.execute("SELECT `mask_ip` FROM `mask_ip` WHERE `octet` = 3", ).fetchall()
            for row in result:
                ip_mask_3 = int(row[0])
            return ip_mask_3

    def set_ip_mask_4(self, ip_mask_4):
        with self.connection:
            return self.cursor.execute("UPDATE `mask_ip` SET `mask_ip` = ? WHERE `octet` = 4", (ip_mask_4,))

    def set_ip_mask_3(self, ip_mask_3):
        with self.connection:
            return self.cursor.execute("UPDATE `mask_ip` SET `mask_ip` = ? WHERE `octet` = 3", (ip_mask_3,))

    def get_publick_key_user(self,user_id):  # Получение из БД ip маски подсети четвертого октета
        with self.connection:
            result = self.cursor.execute("SELECT `publick_key_user` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                publick_key_user = str(row[0])
            return publick_key_user

    def set_publick_key_user(self, user_id, publick_key_user):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `publick_key_user` = ? WHERE `user_id` = ?", (publick_key_user, user_id,))


    def get_last_id (self):
        with self.connection:
            result = self.cursor.execute("SELECT max(id) FROM users")
        for row in result:
            get_last_id = int(row[0])
        return get_last_id

    def get_sub_status_from_user_id(self, id):
        with self.connection:
            result = self.cursor.execute("SELECT `time_sub` FROM `users` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                time_sub = int(row[0])

            if time_sub > int(time.time()):
                return True
            else:
                return False

    def get_from_id_publick_key_user(self, id):  # Получение из БД ip маски подсети четвертого октета
        with self.connection:
            result = self.cursor.execute("SELECT `publick_key_user` FROM `users` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                id_publick_key_user = str(row[0])
            return id_publick_key_user

    def get_telegram_id(self,id):
        with self.connection:
            result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                id = str(row[0])
            return id

    def get_id(self,id):
        with self.connection:
            result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                tg_id = str(row[0])
            return tg_id

    def set_ip_mask_user(self, ip_mask, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `ip_mask` = ? WHERE `user_id` = ?", (ip_mask, user_id,))

    def get_ip_mask_user_from_id(self,id):
        with self.connection:
            result = self.cursor.execute("SELECT `ip_mask` FROM `users` WHERE `id` = ?", (id,)).fetchall()
            for row in result:
                ip_mask = str(row[0])
            return ip_mask

    def set_new_old_sub_user(self,time,user_id):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `time_sub` = ? WHERE `user_id` = ?", (time, user_id,))