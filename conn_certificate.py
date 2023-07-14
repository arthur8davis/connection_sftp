import paramiko

hostname = 'sftp.example.com'
port = 22
username = 'your_username'
private_key_path = '/path/to/private_key.ppk'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
client.connect(hostname=hostname, port=port, password=None, username=username, pkey=private_key,
               disabled_algorithms=dict(pubkeys=["rsa-sha2-512", "rsa-sha2-256"]), )
sftp = client.open_sftp()
files = sftp.listdir('/ALICORPSAASFTP')
for file_name in files:
    print(file_name)
sftp.close()
client.close()
