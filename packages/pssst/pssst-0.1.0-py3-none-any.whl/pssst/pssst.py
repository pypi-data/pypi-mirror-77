"""
PSSST client and server interfaces
"""

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives.serialization import (
    Encoding, PrivateFormat, PublicFormat, NoEncryption
    )
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

from .header import Header, CipherSuite
from .errors import (
    PSSSTUnsupportedCipher, PSSSTClientAuthFailed,
    PSSSTReplyMismatch, PSSSTNotReply, PSSSTNotRequest,
    PSSSTDecryptFailed
    )

def _DKF_SHA384(dh_param, shared_secret): # pylint: disable=invalid-name
    h384 = hashes.Hash(hashes.SHA384(), default_backend())
    h384.update(dh_param)
    h384.update(shared_secret)
    derived_bytes = h384.finalize()
    key = derived_bytes[:16]
    iv_c = derived_bytes[16:32]
    iv_s = derived_bytes[32:]
    return (key, iv_c, iv_s)

def generate_key_pair(cipher_suite=CipherSuite.X25519_AESGCM128):
    """A utility function to generate a suitable key pair for the given cipher suite

    :param cipher_suite: cipher suite for which to generate asymmetric key pair

    :raises PSSSTUnsupportedCipher: requested cipher suite is not supported.

    :return: (private_key, public_key) tuple
    """
    if cipher_suite != CipherSuite.X25519_AESGCM128:
        raise PSSSTUnsupportedCipher()

    new_private_key = X25519PrivateKey.generate()
    return (new_private_key, new_private_key.public_key())


class PSSSTClient:
    """PSSST client interface

    :param server_public_key: Public key of the target server
    :param client_private_key: Private key for client authentication, defaults to None
    :param cipher_suite: cipher suite for which to generate asymmetric key pair

    :raises PSSSTUnsupportedCipher: requested cipher suite is not supported.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, server_public_key,
                 client_private_key=None,
                 cipher_suite=CipherSuite.X25519_AESGCM128):
        """Return a new PSSSTClient"""
        if cipher_suite != CipherSuite.X25519_AESGCM128:
            raise PSSSTUnsupportedCipher()

        if isinstance(server_public_key, str):
            server_public_key = X25519PublicKey.from_public_bytes(
                bytes.fromhex(server_public_key)
                )
        self._request_hdr = Header(cipher_suite=cipher_suite,
                                   reply=False,
                                   client_auth=(client_private_key is not None))

        self._server_public = server_public_key
        self._client_private = client_private_key
        if client_private_key is not None:
            if isinstance(client_private_key, str):
                client_private_key = X25519PrivateKey.from_private_bytes(
                    bytes.fromhex(client_private_key)
                    )
            self._client_public = client_private_key.public_key()
            partial_key_bytes = client_private_key.exchange(server_public_key)
            self._client_server_pub = X25519PublicKey.from_public_bytes(partial_key_bytes)

    def pack_request(self, data):
        """Pack an outbound request

        :param data: message bytes to be encrypted
        :type data: bytes

        :returns: tuple of encrypted packet and reply handler
        """
        temp_priv_key = X25519PrivateKey.generate()
        if self._client_private:
            exchange_dh = temp_priv_key.exchange(self._client_public)
            shared_secret = temp_priv_key.exchange(self._client_server_pub)
            client_pub_bytes = self._client_public.public_bytes(encoding=Encoding.Raw,
                                                                format=PublicFormat.Raw)
            temp_private_bytes = temp_priv_key.private_bytes(encoding=Encoding.Raw,
                                                             format=PrivateFormat.Raw,
                                                             encryption_algorithm=NoEncryption())
            data = client_pub_bytes + temp_private_bytes + data
        else:
            exchange_dh = temp_priv_key.public_key().public_bytes(encoding=Encoding.Raw,
                                                                  format=PublicFormat.Raw)
            shared_secret = temp_priv_key.exchange(self._server_public)

        key, nonce_client, nonce_server = _DKF_SHA384(exchange_dh, shared_secret)

        packet = self._request_hdr.packet_bytes + exchange_dh
        cipher = AESGCM(key)

        packet += cipher.encrypt(nonce_client, data, None)

        def reply_handler(packet):
            """Unpack the reply to a request packet"""
            hdr = Header.from_packet(packet[:4])
            if not hdr.reply:
                raise PSSSTNotReply()
            if (not hdr.reply or
                    hdr.cipher_suite != self._request_hdr.cipher_suite or
                    hdr.client_auth != self._request_hdr.client_auth or
                    packet[4:36] != exchange_dh):
                raise PSSSTReplyMismatch()
            try:
                plaintext = cipher.decrypt(nonce_server, packet[36:], None)
            except InvalidTag:
                raise PSSSTDecryptFailed()
            return plaintext

        return (packet, reply_handler)

class PSSSTServer:
    """PSSST server interface

    :param server_private_key: Private key for the server
    :param cipher_suite: cipher suite for which to generate asymmetric key pair

    :raises PSSSTUnsupportedCipher: requested cipher suite is not supported.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, server_private_key, cipher_suite=CipherSuite.X25519_AESGCM128):
        """Return a new PSSST server"""
        if cipher_suite != CipherSuite.X25519_AESGCM128:
            raise PSSSTUnsupportedCipher()
        self._suite = cipher_suite
        self._server_private = server_private_key

    def unpack_request(self, packet):
        """Unpack an incoming request

        :param packet: Incoming packet to unpack
        :type packet: bytes

        :raises PSSSTUnsupportedCipher: cipher suite indicated in packet is not supported.
        :raises PSSSTNotRequest: packet is not a request packet.
        :raises PSSSTDecryptFailed: payload did not decrypt to valid and authentic data
        :raises PSSSTClientAuthFailed: client auth was present but did not match request
        :returns: tuple of unpacked data, authenticated client public key and reply handler

        """
        hdr = Header.from_packet(packet[:4])
        if hdr.reply:
            raise PSSSTNotRequest()
        if hdr.cipher_suite != self._suite:
            raise PSSSTUnsupportedCipher()
        dh_bytes = packet[4:36]
        exchange_dh = X25519PublicKey.from_public_bytes(dh_bytes)
        shared_secret = self._server_private.exchange(exchange_dh)

        key, nonce_client, nonce_server = _DKF_SHA384(dh_bytes, shared_secret)

        cipher = AESGCM(key)

        try:
            plaintext = cipher.decrypt(nonce_client, packet[36:], None)
        except InvalidTag:
            raise PSSSTDecryptFailed()

        if hdr.client_auth:
            client_public_key = X25519PublicKey.from_public_bytes(plaintext[:32])
            temp_privte_key = X25519PrivateKey.from_private_bytes(plaintext[32:64])
            auth_dh = temp_privte_key.exchange(client_public_key)
            if auth_dh != exchange_dh.public_bytes(encoding=Encoding.Raw, format=PublicFormat.Raw):
                raise PSSSTClientAuthFailed()
            plaintext = plaintext[64:]
        else:
            client_public_key = None

        def reply_handler(data):
            """Pack a reply to the request"""
            reply_hdr = Header(reply=True,
                               client_auth=hdr.client_auth,
                               cipher_suite=hdr.cipher_suite)
            return reply_hdr.packet_bytes + packet[4:36] + cipher.encrypt(nonce_server, data, None)

        return (plaintext, client_public_key, reply_handler)
