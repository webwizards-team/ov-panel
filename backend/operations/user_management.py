import pexpect
import re
import os
from datetime import datetime

from logger import logger
from db import crud
from db.engine import get_db


script_path = "/root/openvpn-install.sh"


def create_user_on_server(name, expiry_date) -> bool | str:
    try:
        pexpect.spawn("chmod +x openvpn-install.sh", encoding="utf-8")
        bash = pexpect.spawn(f"bash {script_path}", encoding="utf-8", timeout=60)

        bash.expect("Option:")
        bash.sendline("1")

        bash.expect("Name:")
        bash.sendline(name)

        bash.expect(pexpect.EOF)
        return True

    except pexpect.exceptions.TIMEOUT:
        logger.error("time out when read exceeds")
        return "error"
    except Exception as e:
        logger.error(f"error when create a user on server: {e}")
        return "error"


async def delete_user_on_server(name, disable_on_db: bool = False) -> bool | str:
    try:
        pexpect.spawn("chmod +x openvpn-install.sh", encoding="utf-8")
        bash = pexpect.spawn(f"bash {script_path}", encoding="utf-8", timeout=60)

        bash.expect("Option:")
        bash.sendline("2")

        bash.expect("Client:")
        list_output = bash.before

        pattern = re.compile(r"\s*(\d+)\)\s*(.+)")
        matches = pattern.findall(list_output)

        user_number = None
        for num, user in matches:
            if user.strip() == name:
                user_number = num
                break

        if not user_number:
            logger.error(f"User '{name}' not found for delete!")
            bash.close()
            return "not_found"

        bash.sendline(user_number)

        bash.expect(r"\[y/N\]:", timeout=30)
        bash.sendline("y")

        bash.expect(pexpect.EOF)
        file_to_delete = f"/root/{name}.ovpn"
        if os.path.exists(file_to_delete):
            try:
                os.remove(file_to_delete)
            except Exception as e:
                logger.error(f"Error deleting file {file_to_delete}: {e}")
                return False
        else:
            logger.warning(f"File {file_to_delete} does not exist.")

        if disable_on_db:
            crud.change_user_status(status=False, name=name)
        return True
    except Exception as e:
        logger.error("Error in delete_user_on_server:", e)
        return False


async def check_user_expiry_date():
    """Tihs function checks users' expiration dates"""
    db = next(get_db())
    users = crud.get_all_users(db)

    try:
        for user in users:
            if user.expiry_date < datetime.now():
                delete_user_on_server(disable_on_db=True, name=user.name)
                logger.info(f"Expiration: user({user}) has been revoked from the panel")
    except Exception as e:
        logger.error(f"Error in users expiryition daily check -> {e}")
