# -*- coding:utf-8 -*-
"""
@Author: Rossi
2016-01-24
"""
from __future__ import unicode_literals
from weiboapi.util.util import *
import binascii
import rsa


def test_base64():
    print(base64_encode("luo"))


def encrypt_password(p, st, nonce, pk, rsakv):
    """
    Encrypting the password using rsa algorithm.
    p: password 
    st: server time 
    nonce: random value 
    pk: public key 
    rsakv: rsa key value
    """
    pk = '0x' + pk
    pk = int(pk, 16)
    key = rsa.PublicKey(pk, 65537)
    msg = str(st) + '\t' + str(nonce) + '\n' + p
    psw = rsa.encrypt(bytearray(msg, 'utf-8'), key)
    psw = binascii.b2a_hex(psw)
    return psw
