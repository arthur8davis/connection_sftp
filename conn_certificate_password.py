import paramiko
import threading


def multifactor_auth_sftp_client(host, port, username, key, password):
    # Create an SSH transport configured to the host
    transport = paramiko.Transport((host, port))
    # Negotiate an SSH2 session
    transport.connect()
    # Attempt authenticating using a private key
    transport.auth_publickey(username, key)
    # Create an event for password auth
    password_auth_event = threading.Event()
    # Create password auth handler from transport
    password_auth_handler = paramiko.auth_handler.AuthHandler(transport)
    # Set transport auth_handler to password handler
    transport.auth_handler = password_auth_handler
    # Aquire lock on transport
    transport.lock.acquire()
    # Register the password auth event with handler
    password_auth_handler.auth_event = password_auth_event
    # Set the auth handler method to 'password'
    password_auth_handler.auth_method = 'password'
    # Set auth handler username
    password_auth_handler.username = username
    # Set auth handler password
    password_auth_handler.password = password
    # Create an SSH user auth message
    userauth_message = paramiko.message.Message()
    userauth_message.add_string('ssh-userauth')
    userauth_message.rewind()
    # Make the password auth attempt
    password_auth_handler._parse_service_accept(userauth_message)
    # Release lock on transport
    transport.lock.release()
    # Wait for password auth response
    password_auth_handler.wait_for_response(password_auth_event)
    # Create an open SFTP client channel
    return transport.open_sftp_client()


username = '...'
password = '...'
file_path = '...'
pkey = paramiko.RSAKey.from_private_key_file(file_path)
sftpClient = multifactor_auth_sftp_client('...', 22, username, pkey, password)
