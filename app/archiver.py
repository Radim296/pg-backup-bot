import io
import pyzipper
import zipfile

from app.config import Configuration


def make_archive(data: bytes, config: Configuration) -> bytes:
    """
    Compresses the given data into a ZIP archive. If a password is specified in the config,
    it uses AES encryption with LZMA compression (via pyzipper). If no password is provided,
    it uses the standard zipfile module (still with LZMA for better compression) without encryption.
    If archiving is disabled (SEND_AS_ARCHIVE is False), returns the data as-is.

    :param data: The raw SQL backup (or any) data to be archived.
    :type data: bytes
    :param config: Configuration object that contains archiver settings such as SEND_AS_ARCHIVE and PASSWORD.
    :type config: Configuration
    :return: A ZIP-archived (encrypted if password provided) version of the data, or the original data if archiving is disabled.
    :rtype: bytes
    """

    # 1. If no archiving is needed, return the original data.
    if not config.archiver.SEND_AS_ARCHIVE:
        return data

    zip_buffer = io.BytesIO()
    password = config.archiver.PASSWORD

    # 2. If password is given, use pyzipper for AES + LZMA encryption.
    if password:
        with pyzipper.AESZipFile(
            zip_buffer,
            mode='w',
            encryption=pyzipper.WZ_AES,
            compression=pyzipper.ZIP_LZMA
        ) as zf:
            # Encode the password to bytes if it's a string
            if isinstance(password, str):
                password = password.encode("utf-8")
            zf.setpassword(password)
            zf.writestr("backup.sql", data)
    else:
        # 3. No password => no encryption, but still compress with LZMA
        with zipfile.ZipFile(
            zip_buffer,
            mode='w',
            compression=zipfile.ZIP_LZMA
        ) as zf:
            zf.writestr("backup.sql", data)

    # 4. Reset the pointer and return the compressed bytes
    zip_buffer.seek(0)
    return zip_buffer.getvalue()